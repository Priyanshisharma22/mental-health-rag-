import torch
from langchain_huggingface import HuggingFaceEmbeddings

device = "cuda" if torch.cuda.is_available() else "cpu"

embeddings = HuggingFaceEmbeddings(
    model_name="intfloat/multilingual-e5-base",
    model_kwargs={"device": device}
)
