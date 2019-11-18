from typing import List, Dict, Any
import argparse
import glob
import json
import os
import re


def return_annotated_text(morphs: List[str], iob_labels: List[str]) -> List[str]:
    """

    Args:
        morphs (List[str]): morphemes in a sentence
        iob_labels ([type]): labels formatted iob2 for a sentence

    Returns:
        List[str]: annotated morphemes
    """

    annotated_text = []
    for morph, label in zip(morphs, iob_labels):
        tmp_text = morph.split('\t')
        tmp_text[-1] = label
        tmp_text = '\t'.join(tmp_text)
        annotated_text.append(tmp_text)

    return annotated_text


def return_iob_labels(lengths: List[int], labels: List[List[Any]]) -> List[str]:
    """

    Args:
        lengths (List[int]): list of morph lengths in a morphs
        labels (List[List[Any]]): list of labels for morphs

    Returns:
        List[str]: labels for a morphs
    """

    iob_labels = []
    index = 0
    begin_flag = False
    labels.sort(key=lambda x: x[0])
    for length in lengths:
        if len(labels) > 0 \
            and labels[0][0] <= index \
                and labels[0][1] > index:
            if begin_flag:
                iob_labels.append('I-' + labels[0][2])
            else:
                iob_labels.append('B-' + labels[0][2])
                begin_flag = True
        else:
            iob_labels.append('O')
        index += length + 1
        if len(labels) > 0 and labels[0][1] <= index:
            labels = labels[1:]
            begin_flag = False
    return iob_labels


def reshape_json(json_file: str) -> Dict[str, Any]:
    """

    Args:
        json_file (str): json file formatted doccano output

    Returns:
        Dict[str, Any]: json contents of labeling result by doccano
    """

    with open(json_file, 'r', encoding='utf-8') as f:
        content = '['
        content += ''.join(
            [re.sub(r'}\n', '},\n', line)
                for line in f.readlines()]
        )[:-2] + ']'
    json_contents = json.loads(content)
    return json_contents


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Parse doccano export and parsed \
            text to parsed text and labels.'
    )
    parser.add_argument('infile', nargs=1, type=argparse.FileType('r'),
                        help='a file path of doccano export')
    parser.add_argument('indir', nargs=1, type=str,
                        help='a directory path of parsed text')
    parser.add_argument('outdir', nargs=1, type=str,
                        help='a directory path of this program\'s result')
    args = parser.parse_args()
    os.makedirs(args.outdir, exist_ok=True)

    json_contents = reshape_json(args.infile)

    files = glob.glob('{}/*.txt'.format(args.indir))
    json_list = [json_content['text'] for json_content in json_contents]

    for fname in files:
        with open(fname, 'r', encoding='utf-8') as f:
            parsed_morphs = f.readlines()
        morphs = [s.split('\t')[0] for s in parsed_morphs]
        synopsis_morphs = ' '.join(morphs)

        # make an annotated string
        morph_lengths = [len(morph) for morph in morphs]
        idx = json_list.index(synopsis_morphs)
        iob_labels = return_iob_labels(
            morph_lengths, json_contents[idx]['labels']
        )
        annotated_text = return_annotated_text(parsed_morphs, iob_labels)

        # create an annotated text
        target_file = '{}/{}'.format(
            args.outdir, fname.replace(args.indir, '')
        )
        with open(target_file, 'w') as f:
            f.write('\n'.join(annotated_text))
