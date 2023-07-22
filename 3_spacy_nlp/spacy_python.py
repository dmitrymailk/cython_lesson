import spacy
from datasets import load_dataset
import time


def simple_sentence_tokenization():
    dataset = load_dataset("alturing/gutenberg-texts")
    dataset = dataset["train"]
    text = dataset[0]["text"]
    start = time.time()
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    sentences = [sent for sent in doc.sents]
    print(time.time() - start)
    # 21.70147180557251


def simple_pos_tag():
    dataset = load_dataset("alturing/gutenberg-texts")
    dataset = dataset["train"]
    text = dataset[0]["text"]
    start = time.time()
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    pos_tags = []
    for token in doc:
        pos_tags.append(
            {
                "token": token.text,
                "pos_tag": token.tag_,
            }
        )
    print(time.time() - start)
    # print(pos_tags)
    # 21.87799096107483


if __name__ == "__main__":
    # simple_sentence_tokenization()
    simple_pos_tag()
