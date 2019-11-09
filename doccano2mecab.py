import sys
import json
import re
import glob  # フォルダの中のpathを取ってこれるやつ


def return_annotated_text(file_sentence, json_labels):
    annotated_text = []
    for f, j in zip(file_sentence, json_labels):
        tmp_text = f.split("\t")
        tmp_text[-1] = j
        tmp_text = "\t".join(tmp_text)
        annotated_text.append(tmp_text)
    return annotated_text

def return_json_labels(length, j_labels:list):
    IOB_labels = []
    index = 0
    flag = False
    j_labels.sort(key=lambda x:x[0])
    # while index < sum(length) + len(length) - 1:
    for l in length:
        if len(j_labels) > 0 and j_labels[0][0] <= index and j_labels[0][1] > index:
            if flag:
                IOB_labels.append("I-" + j_labels[0][2])
            else:
                IOB_labels.append("B-" + j_labels[0][2])
                flag = True
        else:
            IOB_labels.append("O")
        index += l + 1
        if len(j_labels) > 0 and j_labels[0][1] <= index:
            j_labels = j_labels[1:]
            flag = False
        print(index)
    return IOB_labels

def reshape_json(json_file):
    with open(json_file, 'r', encoding="utf-8") as f:
        # reader = f.readlines()
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
            mecab_sentence = f.readlines()
        morphs = [i.split("\t")[0] for i in mecab_sentence]
        file_sentence = " ".join(morphs)
        mecab_length = [len(morph) for morph in morphs]
        i = json_list.index(file_sentence)
        json_labels = return_json_labels(mecab_length, json_contents[i]["labels"])
        # print(json_labels)
        annotated_text = return_annotated_text(mecab_sentence, json_labels)
        with open("{}/".format(new_dir_path) + file_name.replace(old_dir_path, ""), "w") as f:
            f.write("\n".join(annotated_text))