import spacy

nlp = spacy.load("uk_core_news_sm")

def divide_into_sentences(text: str):
    doc = nlp(text)
    sentences = [sentence.replace("..", "-").replace("/", "-") for sentence in sentences]
    return sentences