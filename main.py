import streamlit as st
import pandas as pd

from tools.search_youtube import search_youtube
from tools.transform_search_result import transform

def init_page():
    st.set_page_config(
        page_title="Summarize youtube movie"
    )
    st.header("Search Youtube")

# 検索結果の並び順
def set_sidebar_search_order():
    order_candidates = ("1: 関連性の高い順", "2: 作成日の新しい順", "3: 評価の高い順", "4: 閲覧数の多い順")
    order = st.sidebar.selectbox("Choose order:", order_candidates)

    if "order" not in st.session_state:
        st.session_state.order = ""
        st.session_state.prev_order = ""
    st.session_state.prev_order = st.session_state.order

    if "2:" in order:
        st.session_state.order = "date"
    elif "3:" in order:
        st.session_state.order = "rating"
    elif "4:" in order:
        st.session_state.order = "viewCount"
    else:
        st.session_state.order = "relevance"

# 動画選択
def set_sidebar_movie_choice():
    if "movies" in st.session_state:
        titles = [m["title"] for m in st.session_state.movies]
        title = st.sidebar.selectbox("Choose a movie:", titles)
        movie = [m for m in st.session_state.movies if m["title"] == title][0]
        st.session_state.selected_movie = movie

def path_to_image_html(path):
    return f'<img src="data:image/jpeg;base64,{path}" />'

def set_content():
    with st.spinner("Fetching content..."):
        if query := st.text_input("Searc word", key="input"):
            movies = []
            if (
                ("prev_query" not in st.session_state)
                or (query != st.session_state.prev_query)
                or (st.session_state.order != st.session_state.prev_order)
            ):
                results = search_youtube(query, st.session_state.order)
                movies = transform(results)
                st.session_state.movies = movies
                st.session_state.prev_query = query
            else:
                movies = st.session_state.movies

            # 結果表にサムネイル画像もいれたいので、pandasのto_html()を使う
            df = pd.DataFrame(movies)
            st.markdown(
                df.to_html(
                    escape=False,
                    formatters={"image": lambda x: f'<img src="data:image/jpeg;base64,{x}" />'}
                ),
                unsafe_allow_html=True
            )

def main():
    init_page()
    set_sidebar_search_order()
    set_content()
    set_sidebar_movie_choice()

if __name__ == "__main__":
    main()