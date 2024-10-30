import traceback
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
# Youtube用ライブラリ（Documents Loader）を追加
from langchain_community.document_loaders import YoutubeLoader

SUMMARIZE_PROMPT = """
# Instruction
You are very good at summarizing long sentences and can generate excellent summary statements.
Please summarize the following content in {chara_num} words in a clear and concise manner.

# Content
{content}

# Restriction
Answer in Japanese
"""

YOUTUBE_URL = "https://www.youtube.com/watch?v="

def get_chain():
    llm = st.session_state.model
    prompt = ChatPromptTemplate.from_messages([
        ("user", SUMMARIZE_PROMPT)
    ])
    output_parser = StrOutputParser()
    return prompt | llm | output_parser

def get_content():
    """
    Document:
        - page_content: str
        - metadata: dict
            - source: str
            - title: str
            - description: Optional[str]
            - view_count: int
            - thumbnail_url: Optional[str]
            - publish_data: str
            - length: int
            - author: str
    """
    if movie := st.session_state.selected_movie:
        # 字幕（transcript）を取得して要約に利用する
        with st.spinner("Fetching content..."):
            loader = YoutubeLoader.from_youtube_url(
                f"{YOUTUBE_URL}{movie["id"]}",
                # add_video_info=True,  # タイトルや再生数も取得できる, pytubeのインストールが必要
                add_video_info=False,
                language=["en", "ja"]  # 英語 -> 日本語の優先順位で字幕を取得
            )
            try:
                res = loader.load()
                if res:
                    content = res[0].page_content
                    # title = res[0].metadata["title"]
                    title = movie["title"]
                    return f"Title: {title}\n\n{content}"
                else:
                    return None
            except:
                st.write(traceback.format_exc())
                return None


def init_page():
    st.set_page_config(
        page_title="Summarize youtube movie"
    )
    st.header("Summarize Youtube")

def set_sidebar():
    # 何文字程度に要約したいか
    chara_num_candidates = ("500", "700", "1000")
    chara_num = st.sidebar.selectbox("Choose the number of characters:", chara_num_candidates)
    match chara_num:
        case "700":
            st.session_state.chara_num = 700
        case "1000":
            st.session_state.chara_num = 1000
        case _:
            st.session_state.chara_num = 500

    # LLMモデルの選択
    models = ("Gemini 1.5 Pro", "Gemini 1.5 Flash")
    model = st.sidebar.selectbox("Choose a model:", models)
    if model == "Gemini 1.5 Pro":
        st.session_state.model = ChatGoogleGenerativeAI(
            temperature=0,
            model="gemini-1.5-pro-latest"
        )
    else:
        st.session_state.model = ChatGoogleGenerativeAI(
            temperature=0,
            model="gemini-1.5-flash-latest"
        )

def set_content():
    chain = get_chain()

    if content := get_content():
        movie = st.session_state.selected_movie
        if chara_num := st.session_state.chara_num:
            st.markdown(f"## {movie["title"]}")
            st.markdown(movie["description"])
            st.markdown("---")
            st.markdown("## Summary")
            st.write_stream(chain.stream({"content": content, "chara_num": chara_num}))

def main():
    init_page()
    if "selected_movie" in st.session_state:
        set_sidebar()
        set_content()
    else:
        st.write("Select a movie on <main> page first.")

if __name__ == "__main__":
    main()