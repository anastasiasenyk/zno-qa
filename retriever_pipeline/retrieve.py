import re

from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

from retriever_pipeline.chunking import load_chunks_from_file, load_documents, split_into_chunks, clean_chunks, save_chunks_to_file
from retriever_pipeline.processing_chunks import search_by_ngrams

template = """
Вам буде надано питання або твердження. Ваше завдання — створити три різні варіації ключових слів (по 1–3 слова кожне), які будуть ефективними для отримання відповідної інформації з баз даних або пошукових систем.

- Ключові слова повинні бути релевантними і лаконічними, відображаючи основні концепти питання.
- Кожна варіація ключових слів може містити 1, 2 або 3 слова.
- Ключові слова повинні відображати різні комбінації основних елементів питання.
- Комбінації із ключовими словами повинні знаходитись у різних рядках та бути виділиними в лапки.


**Приклад:**

**Питання:**
«Рядовичами» в Київській Русі називали

**Відповідь:**
"рядовичі Київська Русь"
"рядовичі русь"
"рядовичі"


**Питання:**
На українських землях, включених до складу Литовської держави, за князя Ольгерда (1345 — 1377 рр.)

**Відповідь:**
"Литовська держава Ольгерд"
"Ольгерд"

---

**Питання:**
{question}

**Відповідь:**
"""


def retrieve_chunks(filepath, query, num_chunks_to_retrieve=3):
    """
    Retrieve the most relevant chunks from a file based on a query.

    Args:
        filepath (str): Path to the file containing pre-processed chunks.
        query (str): The search query to match chunks against.
        num_chunks_to_retrieve (int): Number of top relevant chunks to retrieve.

    Returns:
        list: A list of the top matching chunks.
    """
    chunks = load_chunks_from_file(filepath)
    result = search_by_ngrams(chunks, query, top_k=num_chunks_to_retrieve)
    return result


def preprocess_documents(documents_path, save_path, chunk_size=256, chunk_overlap=50):
    """
    Load documents, split them into chunks, clean them, and save to a file.

    Args:
        documents_path (str): Path to the documents to be loaded.
        save_path (str): Path to save the processed chunks.
        chunk_size (int): Size of each chunk in characters.
        chunk_overlap (int): Number of overlapping characters between chunks.

    Returns:
        None
    """
    # Load documents
    docs = load_documents(documents_path)
    # Split into chunks
    chunks = split_into_chunks(docs, chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    cleaned_chunks = clean_chunks(chunks)

    # Save cleaned chunks to a file
    save_chunks_to_file(cleaned_chunks, save_path)
    print(f'Chunks processed and saved. Total chunks: {len(cleaned_chunks)}')


def retrieve_relevant_chunks(filepath, model, query, num_chunks_to_retrieve=1):
    """
    Retrieve relevant chunks from a file by querying a language model for keywords.

    Args:
        filepath (str): Path to the file containing pre-processed chunks.
        model (LLM): Language model to generate keywords for searching.
        query (str): User query or prompt to guide the search.
        num_chunks_to_retrieve (int): Number of chunks to retrieve for each keyword.

    Returns:
        list: A list of chunks relevant to the query.
    """
    # Create prompt and chain
    prompt = PromptTemplate.from_template(template)
    llm_chain = LLMChain(prompt=prompt, llm=model)

    # Generate keywords from the query
    answers = llm_chain.invoke({"question": query})['text']
    keywords = re.findall(r'"([^"]*)"', answers)

    # Search for relevant chunks using the generated keywords
    results = []
    for keyword in keywords:
        keyword = keyword.lower()
        relevant_chunks = retrieve_chunks(filepath=filepath, query=keyword, num_chunks_to_retrieve=num_chunks_to_retrieve)
        results.extend(relevant_chunks)

    return results


if __name__ == '__main__':
    filepath = 'naive_chunks.pkl'
    query = 'Де проживала катерина із твору шевченка?'
    num_chunks_to_retrieve = 1

    from langchain_anthropic import ChatAnthropic
    model = ChatAnthropic(model="claude-3-5-sonnet-20240620", temperature=0.1)

    prompt = PromptTemplate.from_template(template)
    llm_chain = LLMChain(prompt=prompt, llm=model)

    answers = llm_chain.invoke({"question": query})['text']
    matches = re.findall(r'"([^"]*)"', answers)

    results = []
    for match in matches:
        match = match.lower()
        relevant_chunks = retrieve_chunks(filepath=filepath, query=match, num_chunks_to_retrieve=num_chunks_to_retrieve)
        results.extend(relevant_chunks)

    for i in results:
        print('-----')
        print(i)


