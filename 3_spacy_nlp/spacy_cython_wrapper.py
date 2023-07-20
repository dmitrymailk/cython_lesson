from spacy_cython import main_nlp_fast
import urllib.request
import spacy


if __name__ == "__main__":
    with urllib.request.urlopen(
        "https://raw.githubusercontent.com/pytorch/examples/master/word_language_model/data/wikitext-2/valid.txt"
    ) as response:
        text = response.read()
    nlp = spacy.load("en_core_web_sm")
    doc_list = list(nlp(text[:80000].decode("utf8")) for i in range(10))
    main_nlp_fast(doc_list)
