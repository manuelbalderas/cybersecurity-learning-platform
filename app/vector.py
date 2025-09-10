from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
import os
import json

input_file = './datasets/nist_scraped_glossary.jsonl'
embeddings = OllamaEmbeddings(model="mxbai-embed-large")


db_location = "./chrome_langchain_db"
add_documents = not os.path.exists(db_location)

vectorstore = Chroma(
    collection_name='cybersecurity_terminology',
    persist_directory=db_location,
    embedding_function=embeddings
)

if add_documents:
    documents = []
    ids = []

    with open(input_file, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f):
            if line.strip():
                record = json.loads(line)
                document = Document(
                    page_content = record['term'] + ' is ' + record['definition'],
                    metadata = {'term': record['term'], "link": record['link']},
                    id = str(i)
                )
            ids.append(str(i))
            documents.append(document)

    vectorstore.add_documents(documents=documents, ids=ids)
    
retriver = vectorstore.as_retriever(
    search_kwargs={
        "k": 5,
    }
)