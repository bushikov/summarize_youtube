from googleapiclient.discovery import build
import os

def search_youtube(query, order):
    """
    Return value
    [
        {
            "kind": "youtube#searchResult",
            "etag": "419fkdJf_f165ale...",
            "id": {
                "kind": "youtube#video",
                "videoId": "Cof901fei",
            },
            "snippet": {
                "puliishedAt": "2023-05-03T10:00:40Z",
                "channelId": "aeofiaOIONF14",
                "title": "あいうえお",
                "description": "かきくけこ",
                "thumbnails": {
                    "default": {
                        "url": "https://example.com",
                        "width": 120,
                        "height": 90
                    },
                    "medium": {...},
                    "high": {...}
                },
                "channelTitle": "さしすせそ",
                "liveBroadcastContent: "none",
                "publishTime": "2023-05-03T10:00:40Z"
            },
        },
        ...
    ]
    """
    youtube = build("youtube", "v3", developerKey=os.environ["GOOGLE_API_KEY"])

    # https://qiita.com/nbayashi/items/bde26cd04f08de21d552#pythonでapiの実行
    # q：検索ワードを指定
    # part：取得する動画の情報内容（https://developers.google.com/youtube/v3/getting-started?hl=ja#part）
    # order：検索結果の並び順。以下から指定
    #   date：作成日が新しい順
    #   rating：評価の高い順
    #   relevance：デフォルト。検索ワードとの関連性の高さ順
    #   title：タイトルのアルファベット順
    #   videoCount：チャンネルは、アップロードされた動画の数の多い順
    #   viewCount：閲覧数の多い順
    # type：取得するリソースのタイプを（video, channel, playlist）の中から指定
    # maxResults：取得する検索結果数。デフォルトは５，最大５０
    #
    # https://developers.google.com/youtube/v3/docs/search/list?hl=ja
    request = youtube.search().list(
        q=query,
        part="snippet",
        type="video",
        order=order,
        maxResults=25
    )

    response = request.execute()

    return response["items"]