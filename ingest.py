import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings


# ---------------- CONFIG ----------------
DATA_DIR = "data"
DB_DIR = "faiss_db"
EMBED_MODEL = "intfloat/multilingual-e5-base"


# ---------------- LOAD DOCUMENTS ----------------
print("📂 Scanning data directory recursively...")

documents = []
pdf_count = 0

for root, _, files in os.walk(DATA_DIR):
    for file in files:
        if file.lower().endswith(".pdf"):
            pdf_count += 1
            path = os.path.join(root, file)
            print(f"📖 Loading PDF: {path}")
            loader = PyPDFLoader(path)
            documents.extend(loader.load())

print(f"📄 Total PDFs found: {pdf_count}")
print(f"📚 Total documents loaded: {len(documents)}")

if not documents:
    raise ValueError(
        "❌ No text extracted from PDFs.\n"
        "Possible reasons:\n"
        "1️⃣ PDFs are scanned images (no selectable text)\n"
        "2️⃣ PDFs are corrupted\n"
        "3️⃣ Wrong data folder\n"
    )


# ---------------- SPLIT TEXT ----------------
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

chunks = text_splitter.split_documents(documents)
print(f"✂️ Text chunks created: {len(chunks)}")

if not chunks:
    raise ValueError("❌ No chunks created after splitting.")


# ---------------- EMBEDDINGS ----------------
print("🧠 Loading embedding model...")
embeddings = HuggingFaceEmbeddings(model_name=EMBED_MODEL)


# ---------------- BUILD FAISS ----------------
print("📦 Building FAISS index...")

db = FAISS.from_documents(chunks, embeddings)
os.makedirs(DB_DIR, exist_ok=True)
db.save_local(DB_DIR)

print("✅ FAISS index built successfully!")
print(f"📁 Saved to: {DB_DIR}/")
