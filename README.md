# doccano_assistant
[doccano](https://github.com/chakki-works/doccano) (open source text annotation tool) を使うときのサポートを行うスクリプト群置き場

## Usage

### mecabで形態素解析された文からdoccanoでアノテーションを行う前の前処理をする場合

```shell
python mecab2doccano.py テキストファイルが置かれたディレクトリ 前処理後のテキストを保存するファイル名
```

### doccanoの使い方

1. dockerコンテナを立ち上げる
```shell
docker build . -t doccano_container:0.1
docker run -d -p 8000:8000 doccano_container:0.1
# コンテナidが出力される
```

2. doccanoのユーザを追加（必要な場合のみ）
```shell
docker exec -it コンテナid sh
# コンテナへアクセス後
# 以下はコマンド例．ユーザ名やパスワードは変更可能
echo "from django.contrib.auth.models import User; User.objects.create_user('username', 'mailaddress', 'password')" | python manage.py shell
```

3. localhost:8000/にアクセス

4. タグ付け頑張る!!
