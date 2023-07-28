from spacy_cython import cython_sentence_tok, cython_pos_tag
import spacy
import time
from datasets import load_dataset


def simple_sentence_tokenization():
    dataset = load_dataset("alturing/gutenberg-texts")
    dataset = dataset["train"]
    text = dataset[0]["text"]
    start = time.time()
    sentences = cython_sentence_tok(text)
    print(time.time() - start)
    # 21.640190839767456


def simple_pos_tag():
    dataset = load_dataset("alturing/gutenberg-texts")
    dataset = dataset["train"]
    text = dataset[0]["text"]
    start = time.time()
    pos_tags = cython_pos_tag(text)
    print(time.time() - start)
    # print(pos_tags)
    # 21.785778999328613


if __name__ == "__main__":
    # simple_sentence_tokenization()
    simple_pos_tag()
