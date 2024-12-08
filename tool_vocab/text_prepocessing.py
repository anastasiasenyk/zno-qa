import spacy
import re

nlp = spacy.load("uk_core_news_sm")

def normalize_words(query):
    doc = nlp(query)
    normalized_words = [
        token.lemma_
        for token in doc
        if re.match(r"^[\w’']+$", token.text)
    ]    
    return normalized_words
