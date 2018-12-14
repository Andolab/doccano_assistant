from typing import List, Dict
import sys
import glob
import csv
import MeCab
import tqdm


m = MeCab.Tagger('-Owakati')


def char2mecab(pair: Dict[str, List[str]]) -> Dict[str, List[str]]:
    """
    chars in text to words in text
    :param pair: ex.) {'text': ['白', 'い', '恋', '人'], 'label': ['B-PRO', 'I-PRO', 'I-PRO', 'I-PRO']}
    :return: ex.) {'text': ['白い', '恋人'], 'label': ['B-PRO', 'I-PRO']}
    """

    new_pair = {}
    text = ''.join(pair['text'])
    label = pair['label']
    parsed_text = (m.parse(text)).split(' ')[:-1]
    label_to_morphs = []
    new_pair['text'] = parsed_text
    for morph in parsed_text:
        label_to_morphs.append(label.pop(0))
        for _ in range(len(morph) - 1):
            label.pop(0)

    new_pair['label'] = label_to_morphs

    return new_pair


def return_annotated_sentences(sentences: List[str], morphs: List[List[str]], labels: List[List[str]]) -> str:
    """
    return sentence annotated in IOB2 labeling scheme
    :param sentences: [sentence_0, sentence_1, ... sentence_n] (unannotated data)
    :param morphs: [[morph], [morph], ... [morph]] (morphs annotated in doccano)
    :param labels: [[label], [label], ... [label]] (labels annotated in doccano.
                                                    This param's indexes corresponds to morph)
    :return: morphs in sentences annotated in IOB2 labeling scheme (mecab format)
             referred char in sentences annotated in IOB2 labeling format (doccano format)
    """

    annotated_sentences = []

    for sentence in sentences:
        morph_words = [morph.split('\t')[0] for morph in sentence.split('\n')]
        morph_others = [morph.split('\t')[1:-2] for morph in sentence.split('\n')]
        # words_ignored_symbolは開発者の用意した実験データにのみ必要
        words_ignored_symbol = [morph.split('\t')[0] for morph in sentence.split('\n')
                                if len(morph.split('\t')) > 1]

        # if morphs annotated in doccano have unannotated morph
        if morph_words in morphs:
            # annotate to unannotated morph
            idx = morphs.index(morph_words)
            annotated_sentences.append('\n'.join(
                [word + '\t' + '\t'.join(other) + '\t' + label for word, other, label
                 in zip(morph_words, morph_others, labels[idx])]
            ))
            morphs.pop(idx)
            labels.pop(idx)

        # 以下の処理は通常のラベル付けの場合は関係ない
        # 開発者の用意した実験データにのみ必要な処理
        elif len(morph_words) == 1:
            annotated_sentences.append(morph_words[0])
        elif morph_words not in morphs and \
                words_ignored_symbol in morphs:
            idx = morphs.index(words_ignored_symbol)
            k = 0
            sentence = ''
            for word in morph_words:
                if '[url]' == word or '[/url]' == word:
                    sentence += word + '\n'
                else:
                    sentence += word + "\t" + '\t'.join(morph_others[k]) + \
                        '\t' + labels[idx][k] + '\n'
                    k += 1
            annotated_sentences.append(sentence)
            morphs.pop(idx)
            labels.pop(idx)

    return '\n'.join(annotated_sentences)


def doccano2mecab(targetfile_path: str, old_dir_path: str, new_dir_path: str) -> None:
    """
    replace doccano labeling format to mecab labeling format
    :param targetfile_path: path of file containing text labeled in doccano format
    :param old_dir_path: path of file containing text in mecab format
    :param new_dir_path: path of new files containing text labeled in mecab format
    """

    # loading doccano format file
    with open(targetfile_path, 'r') as f:
        reader = csv.reader(f)

        texts = []
        chars = []
        for row in reader:
            if row[1] == ' ':
                text = [char[0] for char in chars]
                label = [char[1] for char in chars]
                texts.append({'text': text, 'label': label})
                chars = []
            else:
                chars.append(row[1:])

    # converte doccano format to morph format
    label_to_morphs = [char2mecab(text) for text in texts]
    doccano_morphs = [dic['text'] for dic in label_to_morphs]
    doccano_labels = [dic['label'] for dic in label_to_morphs]

    # annotate unannotated data
    for fname in tqdm.tqdm(glob.glob(old_dir_path + '/*')):
        with open(fname, 'r') as f:
            ftext = f.read().split('\n\n')
            annotated_text = return_annotated_sentences(ftext, doccano_morphs, doccano_labels)
        new_fname = fname[fname.rfind('/') + 1:]
        with open(new_dir_path + new_fname, 'w') as f:
            f.write(annotated_text)


if __name__ == '__main__':
    targetfile_path = sys.argv[1]
    old_dir_path = sys.argv[2]
    new_dir_path = sys.argv[3]
    doccano2mecab(targetfile_path, old_dir_path, new_dir_path)
