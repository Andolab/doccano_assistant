import sys
import json
import re
import glob
import argparse

parser = argparse.ArgumentParser(description='Parse doccano export and parsed text to parsed text and labels.')
parser.add_argument("infile", nargs="?", type=argparse.FileType("r"), help="a file path of doccano export", default=sys.stdin)
parser.add_argument("infolder", nargs="?", help="a folder path of parsed text", default=sys.stdin)
parser.add_argument("outfolder", nargs="?", help="a folder path of this program's result", default=sys.stdin)
args = parser.parse_args()

def return_annotated_text(file_sentence, iob_labels):
    annotated_text = []
    for f, j in zip(file_sentence, iob_labels):
        tmp_text = f.split("\t")
        tmp_text[-1] = j
        tmp_text = "\t".join(tmp_text)
        annotated_text.append(tmp_text)
    return annotated_text

def return_iob_labels(length, j_labels:list):
    iob_labels = []
    index = 0
    begin_flag = False
    j_labels.sort(key=lambda x:x[0])
    for l in length:
        if len(j_labels) > 0 \
            and j_labels[0][0] <= index \
                and j_labels[0][1] > index:
            if begin_flag:
                iob_labels.append("I-" + j_labels[0][2])
            else:
                iob_labels.append("B-" + j_labels[0][2])
                begin_flag = True
        else:
            iob_labels.append("O")
        index += l + 1
        if len(j_labels) > 0 and j_labels[0][1] <= index:
            j_labels = j_labels[1:]
            begin_flag = False
    return iob_labels

def reshape_json(json_file):
    with open(json_file, 'r', encoding="utf-8") as f:
        content = '['
        content += ''.join(
            [re.sub(r'}\n', '},\n', line)
                for line in f.readlines()]
        )[:-2] + ']'
    json_contents = json.loads(content)
    return json_contents

if __name__ == "__main__":
    targetfile_path = sys.argv[1]  # doccano
    old_dir_path = sys.argv[2]  # folder
    new_dir_path = sys.argv[3]  # new folder

    json_contents = reshape_json(targetfile_path)
    
    l = glob.glob("{}/*.txt".format(old_dir_path))
    json_list = [json_content["text"] for json_content in json_contents]
    
    for file_name in l:
        with open(file_name, "r", encoding="utf-8") as f:
            parsed_sentence = f.readlines()
        morphs = [i.split("\t")[0] for i in parsed_sentence]
        synopsis_sentence = " ".join(morphs)
        mecab_length = [len(morph) for morph in morphs]
        i = json_list.index(synopsis_sentence)
        iob_labels = return_iob_labels(mecab_length, json_contents[i]["labels"])
        annotated_text = return_annotated_text(parsed_sentence, iob_labels)
        with open("{}/".format(new_dir_path) + file_name.replace(old_dir_path, ""), "w") as f:
            f.write("\n".join(annotated_text))
