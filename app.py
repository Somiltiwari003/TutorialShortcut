import os

# This project only needs PyTorch. Stop transformers/sentence-transformers from
# importing TensorFlow, which breaks when its protobuf version is mismatched.
os.environ["USE_TF"] = "0"
os.environ["TRANSFORMERS_NO_TF"] = "1"

import re
from urllib.parse import urlparse, parse_qs

import streamlit as st
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_huggingface import (
    ChatHuggingFace,
    HuggingFaceEmbeddings,
    HuggingFaceEndpoint,
)
from langchain_text_splitters import RecursiveCharacterTextSplitter
from youtube_transcript_api import (
    NoTranscriptFound,
    TranscriptsDisabled,
    VideoUnavailable,
    YouTubeTranscriptApi,
)

load_dotenv()

st.set_page_config(page_title="Video Q&A", layout="centered", initial_sidebar_state="collapsed")

st.markdown(
    """
    <style>
        #MainMenu, footer, header [data-testid="stToolbar"] {visibility: hidden;}
        .block-container {max-width: 680px; padding-top: 4rem; padding-bottom: 4rem;}
        h1 {font-weight: 600; letter-spacing: -0.02em; margin-bottom: 0.25rem;}
        .subtitle {opacity: 0.6; margin-bottom: 2.5rem; font-size: 0.95rem;}
        .status {opacity: 0.6; font-size: 0.85rem; margin: 0.5rem 0 2rem 0;}
        .answer {
            border-left: 2px solid currentColor;
            padding: 0.25rem 0 0.25rem 1rem;
            margin: 1.5rem 0;
            line-height: 1.65;
        }
        .stButton > button {border-radius: 4px; font-weight: 500;}
        .stTextInput input {border-radius: 4px;}
        hr {opacity: 0.15;}
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------- helpers ----------

VIDEO_ID_RE = re.compile(r"^[A-Za-z0-9_-]{11}$")


def extract_video_id(url: str):
    """Return the 11-char YouTube video id from a url, or None."""
    url = url.strip()
    if VIDEO_ID_RE.match(url):  # bare id pasted
        return url

    parsed = urlparse(url if "://" in url else f"https://{url}")
    host = (parsed.hostname or "").lower().removeprefix("www.").removeprefix("m.")

    candidate = None
    if host == "youtu.be":
        candidate = parsed.path.lstrip("/").split("/")[0]
    elif host in ("youtube.com", "music.youtube.com", "youtube-nocookie.com"):
        if parsed.path == "/watch":
            candidate = parse_qs(parsed.query).get("v", [None])[0]
        else:
            parts = [p for p in parsed.path.split("/") if p]
            if len(parts) >= 2 and parts[0] in ("embed", "shorts", "live", "v"):
                candidate = parts[1]

    if candidate and VIDEO_ID_RE.match(candidate):
        return candidate
    return None


def fetch_transcript(video_id: str) -> str:
    """Works with both the old (<1.0) and new (>=1.0) youtube-transcript-api."""
    langs = ["en", "en-US", "en-GB"]
    if hasattr(YouTubeTranscriptApi, "fetch"):
        snippets = YouTubeTranscriptApi().fetch(video_id, languages=langs)
        texts = [s.text for s in snippets]
    else:
        texts = [c["text"] for c in YouTubeTranscriptApi.get_transcript(video_id, languages=langs)]
    # join with spaces, otherwise words from adjacent chunks get glued together
    return re.sub(r"\s+", " ", " ".join(texts)).strip()


@st.cache_resource(show_spinner=False)
def get_embeddings():
    return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")


@st.cache_resource(show_spinner=False)
def get_model():
    llm = HuggingFaceEndpoint(
        repo_id="meta-llama/Llama-3.1-8B-Instruct",
        task="text-generation",
        temperature=0.2,
        max_new_tokens=512,
    )
    return ChatHuggingFace(llm=llm)


@st.cache_resource(show_spinner=False)
def build_index(video_id: str):
    """Fetch transcript, chunk it, embed it. Cached per video."""
    transcript = fetch_transcript(video_id)
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.create_documents([transcript])
    store = FAISS.from_documents(chunks, get_embeddings())
    return store, len(chunks), len(transcript.split())


PROMPT = PromptTemplate(
    template=(
        "You are a helpful assistant.\n"
        "Answer ONLY from the provided transcript context.\n"
        "If the context is insufficient, just say you don't know.\n\n"
        "Context:\n{context}\n\n"
        "Question: {question}"
    ),
    input_variables=["context", "question"],
)


def answer_question(store, question: str):
    retriever = store.as_retriever(search_type="mmr", search_kwargs={"k": 4, "fetch_k": 20})
    docs = retriever.invoke(question)
    context = "\n\n".join(d.page_content for d in docs)
    chain = PROMPT | get_model() | StrOutputParser()
    return chain.invoke({"context": context, "question": question}), docs


# ---------- ui ----------

st.title("Video Q&A")
st.markdown(
    '<div class="subtitle">Paste a YouTube link, then ask questions about what is said in the video.</div>',
    unsafe_allow_html=True,
)

url = st.text_input("YouTube link", placeholder="https://www.youtube.com/watch?v=...", label_visibility="collapsed")
load_clicked = st.button("Load video")

if load_clicked:
    video_id = extract_video_id(url)
    if not video_id:
        st.error("That does not look like a valid YouTube link. Check the URL and try again.")
    else:
        try:
            with st.spinner("Fetching transcript and building index"):
                store, n_chunks, n_words = build_index(video_id)
            st.session_state["video"] = {
                "id": video_id,
                "store": store,
                "chunks": n_chunks,
                "words": n_words,
            }
            st.session_state.pop("last", None)
        except TranscriptsDisabled:
            st.error("This video has transcripts disabled.")
        except NoTranscriptFound:
            st.error("No English transcript found for this video.")
        except VideoUnavailable:
            st.error("This video is unavailable.")
        except Exception as e:
            st.error(f"Failed while building the index ({type(e).__name__}): {e}")

video = st.session_state.get("video")

if video:
    st.markdown(
        f'<div class="status">Loaded {video["id"]} &nbsp;|&nbsp; {video["words"]:,} words &nbsp;|&nbsp; {video["chunks"]} chunks</div>',
        unsafe_allow_html=True,
    )

    with st.form("ask", border=False):
        question = st.text_input("Question", placeholder="Ask something about the video", label_visibility="collapsed")
        asked = st.form_submit_button("Ask")

    if asked:
        if not question.strip():
            st.warning("Enter a question first.")
        else:
            try:
                with st.spinner("Thinking"):
                    answer, docs = answer_question(video["store"], question.strip())
                st.session_state["last"] = {"q": question.strip(), "a": answer, "docs": docs}
            except Exception as e:
                st.error(f"Could not generate an answer: {e}")

    last = st.session_state.get("last")
    if last:
        st.markdown(f"**{last['q']}**")
        st.markdown(f'<div class="answer">{last["a"]}</div>', unsafe_allow_html=True)
        with st.expander("Transcript passages used"):
            for i, d in enumerate(last["docs"], 1):
                st.caption(f"Passage {i}")
                st.write(d.page_content)