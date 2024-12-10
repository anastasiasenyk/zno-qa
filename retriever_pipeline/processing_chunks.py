
import re
from collections import Counter

import spacy
import nltk
from nltk import ngrams
from nltk.tokenize import word_tokenize

# curl -O https://raw.githubusercontent.com/amakukha/stemmers_ukrainian/master/src/tree_stem.py
from retriever_pipeline.tree_stem import stem_word

nltk.download('punkt_tab')


nlp = spacy.load('uk_core_news_sm', disable=['parser', 'ner'])
ALPH = set("абвгґдеєжзиіїйклмнопрстуфхцчшщьюя'-")
CLEAN_PATTERN = re.compile(r"[^a-zA-Zа-яА-Яʼ-]")


def contains_only_alph(s):
    """Check if a string contains only alphabetic characters from ALPH."""
    return all(char in ALPH for char in s)


def generate_ngrams(text: str, n: int) -> list[str]:
    """Generate a list of n-grams from the input text."""
    tokens = word_tokenize(stemmer(text.lower()))
    return list(ngrams(tokens, n))


def clean_words(text: str):
    """Remove unwanted characters from text using CLEAN_PATTERN."""
    return CLEAN_PATTERN.sub("", text)


def stemmer(text: str):
    """Stem and clean words in the input text, preserving non-alphabetic tokens."""
    text_list = text.split()
    return " ".join(
        stem_word(clean_words(word)) if contains_only_alph(clean_words(word)) else word
        for word in text_list
    )


def search_by_ngrams(chunks: list, query: str, n: int = 1, top_k: int = 3) -> list:
    """Find the top-k most relevant chunks by matching n-grams from the query."""
    query_ngrams = set(generate_ngrams(query, n))

    chunk_scores = []

    for chunk in chunks:
        chunk_ngrams = generate_ngrams(chunk.page_content, n)
        chunk_counts = Counter(chunk_ngrams)
        chunk_ngrams = set(chunk_ngrams)

        presence_score = sum(1 for ng in query_ngrams if ng in chunk_ngrams)
        intersection_size = sum(chunk_counts[ng] for ng in query_ngrams)

        if intersection_size > 0:
            chunk_scores.append((chunk.page_content, presence_score, intersection_size))

    chunk_scores.sort(key=lambda x: (x[1], x[2]), reverse=True)
    chunk_scores = [item[0] for item in chunk_scores]
    return chunk_scores[:top_k]
