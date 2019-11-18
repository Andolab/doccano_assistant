# doccano_assistant

These scripts provide supports to annotator using [doccano](https://github.com/chakki-works/doccano) (open source text annotation tool)

※ These scripts only support annotation of sequence labeling task format (Part of Speech Tagging, Named Entity Recognition, etc...)

## Usage

1. The sentences of annotating target are tokenized using morphological analysis. (Option)
2. Convert tokenized sentences to format of doccano input. (Option)

   ```shell
   python mecab2doccano.py dir_path_having_tokenized_sentences output_file_path
   ```

3. Let's annotate using doccano!!

4. Export annotation result from doccano (.json)

5. Execute following command (convert doccano format to conll format)

```shell
python doccano2mecab.py *.json(from 4.) dir_path_having_tokenized_sentences output_path
```

```shell
 $ python doccano2mecab.py --help
 usage: doccano2mecab.py [-h] infile indir outdir
 Parse doccano export and parsed text to parsed text and labels.

 positional arguments:
 infile a file path of doccano export
 indir a folder path of parsed text
 outdir a folder path of this program\'s result

 optional arguments:
 -h, --help show this help message and exit
```
