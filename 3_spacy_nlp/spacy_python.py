import urllib.request
import spacy


def slow_loop(doc_list, word, tag):
    n_out = 0
    for doc in doc_list:
        for tok in doc:
            if tok.lower_ == word and tok.tag_ == tag:
                n_out += 1
    return n_out


def main_nlp_slow(doc_list):
    n_out = slow_loop(doc_list, "run", "NN")
    print(n_out)


if __name__ == "__main__":
    # Build a dataset of 10 parsed document extracted from the Wikitext-2 dataset
    with urllib.request.urlopen(
        "https://raw.githubusercontent.com/pytorch/examples/master/word_language_model/data/wikitext-2/valid.txt"
    ) as response:
        text = response.read()
    nlp = spacy.load("en")
    doc_list = list(nlp(text[:800000].decode("utf8")) for i in range(10))
