# doccano_assistant
[doccano](https://github.com/chakki-works/doccano) (open source text annotation tool) を使うときのサポートを行うスクリプト群置き場

## Usage

- mecabで形態素解析された文からdoccanoでアノテーションを行う前の前処理をする場合

```shell
python mecab2doccano.py テキストファイルが置かれたディレクトリ 前処理後のテキストを保存するファイル名
```

- doccanoを起動させる場合

```shell
git clone https://github.com/chakki-works/doccano
cp Dockerfile doccano/
cd doccano/
docker build . -t doccano_container:0.1
docker run -it -p 8000:8000 doccano_container:0.1
# その後，ブラウザでlocalhost:8000に接続
```

- doccanoのユーザを追加する場合
```shell
docker run -it doccano_container:0.1 sh
# コンテナへアクセス後
echo "from django.contrib.auth.models import User; User.objects.create_user('ユーザ名', 'メールアドレス', 'パスワード')" | python manage.py shell
```