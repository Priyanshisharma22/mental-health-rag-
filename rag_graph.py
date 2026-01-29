from langdetect import detect
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.llms import Ollama
from safety import DISCLAIMER


# ---------- Load Models ----------
llm = Ollama(model="llama3")

embeddings = HuggingFaceEmbeddings(
    model_name="intfloat/multilingual-e5-base"
)

db = FAISS.load_local(
    "faiss_db",
    embeddings,
    allow_dangerous_deserialization=True
)


# ---------- Core RAG Function ----------
def run_rag(query: str) -> dict:
    language = detect(query)

    docs = db.similarity_search(query, k=3)
    context = "\n".join(d.page_content for d in docs)

    prompt = f"""
    Answer using ONLY the context below.
    Do NOT give diagnosis or medication advice.

    Context:
    {context}

    Question:
    {query}
    """

    answer = llm.invoke(prompt)

    return {
        "answer": answer + "\n\n" + DISCLAIMER,
        "language": language
    }
