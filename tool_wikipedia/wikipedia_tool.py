from langchain_community.retrievers import WikipediaRetriever
from .text_preprocessing import keywords_extraction
from sentence_transformers import SentenceTransformer, util

retriever = WikipediaRetriever(lang="uk")
embedding_model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

def get_wikipedia_context(query):
    keywords = keywords_extraction(query)
    query_embedding = embedding_model.encode(query, convert_to_tensor=True)
    context = ""

    for keyword in keywords:
        docs = retriever.invoke(keyword)
        page = docs[0]
        page_embedding = embedding_model.encode(page.page_content, convert_to_tensor=True)
        score = util.pytorch_cos_sim(query_embedding, page_embedding).item()
        if score >= 0.5:
            context += f"{keyword}: {page.page_content}\n\n"
        else:
            context += f"{keyword}: {None}\n\n"

    return context.strip()
