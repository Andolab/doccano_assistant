import sys
import glob

"""
Usage
python mecab2doccano.py targetdirectory outputtext
"""


def mecab2doccano(path: str, partition: str) -> str:
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
        words += "".join([morph.split(partition)[0] for morph in morphs]) + ' '
    return words


if __name__ == '__main__':
   mecab_format_dir = sys.argv[1]
   parsed_text_path = sys.argv[2]
   converted_text = '\n'.join(mecab2doccano(path, ',') for path in glob.glob(mecab_format_dir + '/*'))
   with open(parsed_text_path, 'w') as f:
       f.write(converted_text)