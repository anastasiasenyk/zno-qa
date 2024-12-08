import spacy

nlp = spacy.load("uk_core_news_sm")

def divide_into_sentences(text: str):
    doc = nlp(text)
    sentences = [sent.text.strip().replace("..", "-").replace("/", "-") for sent in doc.sents]
    return sentences