from typing import Dict, List
import sys
import csv
import MeCab


def char2morph(pair: Dict[str, List[str]]) -> str:
    """
    :param pair: {text: ['B', 'o', 'b', ...], label:['B-PSN', 'I-PSN', 'I-PSN', ...]}
    :return The result of morphological analysis of text by Mecab. Each morpheme has a label (ex. B-PSN)
    """

    new_pair = {}
    text = ''.join(pair['text'])
    label = pair['label']
    parsed_text = (m.parse(text).replace(',', '\t')).split('\n')[:-2]
    label_to_morphs = []
    new_pair['text'] = parsed_text
    for morph in parsed_text:
        label_to_morphs.append(label.pop(0))
        for _ in range(len(morph[:morph.find('\t')]) - 1):
            label.pop(0)

    new_pair['label'] = label_to_morphs

    sentence = [new_pair['text'][i] + '\t' + new_pair['label'][i]
                for i in range(len(new_pair['text']))]

    return '\n'.join(sentence)


if __name__ == '__main__':
    tagged_file = sys.argv[1]
    parsed_file = sys.argv[2]

    with open(tagged_file, 'r') as f:
        reader = csv.reader(f)

        texts = []
        chars = []
        start = True
        for row in reader:
            if start:
                beforenum = row[0]
                start = False
            if row[1] == ' ' or row[0] != beforenum:
                text = [char[0] for char in chars]
                label = [char[1] for char in chars]
                texts.append({'text': text, 'label': label})
                chars = []
            else:
                chars.append(row[1:])
            beforenum = row[0]

    m = MeCab.Tagger()
    m.parse('')
    sentences = [char2morph(pair) for pair in texts]

    with open(parsed_file, 'w') as f:
        f.write('\n\n'.join(sentences))
