# Youtube動画を要約するアプリ

任意のワードでYoutube動画を検索し、選択した動画を要約する

## インストール
```shell
$ pip install -r requirements.txt
```

## 実行
```shell
export GOOGLE_API_KEY="hogehogehoge"  # YouTube Data APIとGenerative Language APIを有効にしたAPIキーを指定
streamlit run main.py
```