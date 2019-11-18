import argparse
import glob
import re


def mecab2doccano(path: str, partition: str) -> str:
    """
    texts of mecab format to texts of doccano format

    Args:
        path (str): path of a file containing morphologically parsed text in mecab
        partition (str): the simbol of morph partition

    Returns:
        str: converted doccano format
    """

    with open(path, 'r') as f:
        texts = f.read().split('\n\n')
    words = ''
    for text in texts:
        morphs = text.split('\n')
        morphs = [morph for morph in morphs if len(morph.split(partition)) > 1]
        words += ' '.join([morph.split(partition)[0] for morph in morphs]) + ' ' \
            if len(morphs) > 0 else ''
    words = re.sub(r'\s+$', '', words)
    return words


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Parse texts formatted mecab -> texts formatted doccano input'
    )
    parser.add_argument('indir', nargs=1, type=str,
                        help='a directory path containing parsed texts by mecab')
    parser.add_argument('outpath', nargs=1, type=str,
                        help='a output file path')
    args = parser.parse_args()
    mecab_format_dir = args.indir + '/' \
        if args.indir[-1] != '/' else args.indir
    converted_text = '\n'.join(
        mecab2doccano(path, '\t')
        for path in glob.glob(mecab_format_dir + '*')
    )
    with open(args.outpath, 'w') as f:
        f.write(converted_text)
