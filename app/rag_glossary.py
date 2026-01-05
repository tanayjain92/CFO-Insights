from .config import rag_glossary_path
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

# Only build once per process run
GLOSSARY_RETRIEVER = None

def load_glossary_docs():
    loader = TextLoader(str(rag_glossary_path), encoding="utf-8")
    docs = loader.load()
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100,
        add_start_index=True,
    )
    split_docs = splitter.split_documents(docs)
    return split_docs

# Chromadb vector store + embeddings    (# no similiraity threshold, not needed here)
def vector_store(persist_directory = None):
    docs = load_glossary_docs()
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = Chroma.from_documents(
        documents=docs,
        embedding=embeddings,
        collection_name="apple_finance_glossary",
        persist_directory=persist_directory,
    )
    return vectorstore

# Retriever
def get_glossary_retriever(persist_directory = None):
    global GLOSSARY_RETRIEVER
    if GLOSSARY_RETRIEVER is None:
        vs = vector_store(persist_directory=persist_directory)
        GLOSSARY_RETRIEVER = vs.as_retriever(search_kwargs={"k": 3})
    return GLOSSARY_RETRIEVER