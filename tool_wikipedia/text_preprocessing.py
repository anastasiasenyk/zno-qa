import spacy
import noun_phrase_ua

uk_nlp = spacy.load("uk_core_news_sm")
nlp = noun_phrase_ua.NLP()

def normalize_to_nominative(phrase):
    doc = uk_nlp(phrase)
    normalized_tokens = []

    for token in doc:

        if token.pos_ == "PROPN" and not token.dep_ == "nmod":
            normalized_tokens.append(token.lemma_)
        elif token.pos_ == "NOUN" and token.dep_ == "ROOT":
            normalized_tokens.append(token.lemma_)
        else:
            normalized_tokens.append(token.text)

    return " ".join(normalized_tokens)

def summary_processing(summary_data):
    noun_chunks = []
    for entity_group in summary_data["entities"]:
        words = []
        for token_position in entity_group:
            word = summary_data["tokens"][token_position]["word"]
            words.append(word)
        phrase = " ".join(words)
        noun_chunks.append(normalize_to_nominative(phrase))
    return noun_chunks

def noun_chunks_extraction(query):
    summary = nlp.extract_entities(query)
    return summary_processing(summary)

def entities_extraction(query):
    return [ent.lemma_ for ent in uk_nlp(query).ents]

def keywords_extraction(query):
    keywords = set(entities_extraction(query))
    return list(keywords)
