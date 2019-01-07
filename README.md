# doccano_assistant
[doccano](https://github.com/chakki-works/doccano) (open source text annotation tool) を使うときのサポートを行うスクリプト群置き場

## Usage

1. mecabで形態素解析された文からdoccanoでアノテーションを行う前の前処理を行う(必要な場合のみ)

```shell
python mecab2doccano.py テキストファイルが置かれたディレクトリ 前処理後のテキストを保存するファイル名
```

2. dockerコンテナを立ち上げる

```shell
docker build . -t doccano_container:0.1
docker run -d -p 8000:8000 doccano_container:0.1
# コンテナidが出力される
```

3. doccanoのユーザを追加（必要な場合のみ）

```shell
docker exec -it コンテナid sh
# コンテナへアクセス後
# 以下はコマンド例．ユーザ名やパスワードは変更可能
echo "from django.contrib.auth.models import User; User.objects.create_user('username', 'mailaddress', 'password')" | python manage.py shell
```

4. localhost:8000/にアクセス

5. タグ付け頑張る!!

6. doccanoからタグづけしたファイルを .csv 形式でダウンロードしてくる

7. doccanoでタグづけしたテキストをダウンロードし，以下のスクリプトを走らせる

```shell
# 別々のファイルにタグ付けしたい場合に使う
python doccano2mecab.py タグづけしたテキスト(.csv) テキストファイルが置かれたディレクトリ タグづけされたファイルを置きたいディレクトリ
```

または

```shell
# 1つのファイルにタグ付けした結果を置きたい場合に使う
python doccano2parse.py タグづけしたテキスト(.csv) テキストファイル名
```
