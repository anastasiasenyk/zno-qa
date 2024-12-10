import os

from retriever_pipeline.retrieve import preprocess_documents, retrieve_relevant_chunks
from langchain_anthropic import ChatAnthropic


if __name__ == '__main__':
    # documents_history = './retriever_pipeline/documents_txt/history/*.txt'

    documents_literature = './retriever_pipeline/documents_txt/literature/*.txt'

    directory = './retriever_pipeline/data'
    chunks_file = os.path.join(directory, 'chunks.pkl')

    if not os.path.exists(directory):
        os.makedirs(directory)

    query = "Яке справжнє імʼя у Лесі Українки"

    preprocess_documents(documents_literature, chunks_file)
    model = ChatAnthropic(model="claude-3-5-sonnet-20240620", temperature=0.1)
    result = retrieve_relevant_chunks(chunks_file, model, query)

    print(result)

