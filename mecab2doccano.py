import sys
import glob
import re


def mecab2doccano(path, partition):
    """
    texts of mecab format to texts of doccano format
    :param path : path of a file containing morphologically parsed text in mecab
    :param partition : the simbol of morph partition
    :return texts converted doccano format
    """

    with open(path, 'r') as f:
        texts = f.read().split('\n\n')
    words = ''
    for text in texts:
        morphs = text.split('\n')
        morphs = [morph for morph in morphs if len(morph.split(partition)) > 1]
        words += ' '.join([morph.split(partition)[0] for morph in morphs]) + ' ' \
            if len(morphs) > 0 else ''
    words = re.sub('\s+$', '', words)
    return words


if __name__ == '__main__':
    mecab_format_dir = sys.argv[1]
    parsed_text_path = sys.argv[2]
    converted_text = '\n'.join(mecab2doccano(path, '\t') for path in glob.glob(mecab_format_dir + '*'))
    with open(parsed_text_path, 'w') as f:
        f.write(converted_text)
