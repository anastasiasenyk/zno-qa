import pickle
from glob import glob
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter


def load_documents(file_pattern: str):
    """
    Load documents from text files matching the specified file pattern.
    """
    files_path = glob(file_pattern)
    docs = []
    for path in files_path:
        loader = TextLoader(path)
        doc = loader.load()
        docs.extend(doc)
    return docs


def split_into_chunks(documents, chunk_size=256, chunk_overlap=50):
    """
    Split documents into chunks using a recursive character text splitter.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n"]
    )
    return text_splitter.split_documents(documents)


def clean_chunks(naive_chunks):
    """
    Clean chunks by stripping unwanted characters and filtering short chunks.
    """
    cleaned_chunks = []
    for chunk in naive_chunks:
        chunk.page_content = chunk.page_content.strip('-').strip()
        if len(chunk.page_content) > 5:
            cleaned_chunks.append(chunk)
    return cleaned_chunks


def save_chunks_to_file(chunks, filename: str):
    """
    Save chunks to a file using pickle.
    """
    with open(filename, 'wb') as file:
        pickle.dump(chunks, file)


def load_chunks_from_file(filename: str):
    """
    Load chunks from a file saved using pickle.

    Parameters:
        filename (str): The path to the file containing the saved chunks.

    Returns:
        list: The loaded chunks.
    """
    with open(filename, 'rb') as file:
        chunks = pickle.load(file)
        return chunks


if __name__ == "__main__":
    # Load documents
    docs = load_documents('./rag_pipeline/documents_txt/*.txt')

    # Split into chunks
    naive_chunks = split_into_chunks(docs, chunk_size=256, chunk_overlap=50)

    # Clean the chunks
    naive_chunks = clean_chunks(naive_chunks)

    # Save cleaned chunks to a file
    filename = 'naive_chunks.pkl'
    save_chunks_to_file(naive_chunks, filename)
    print(f'Chunks saved with length: {len(naive_chunks)}')
