# distutils: language = c++
import numpy # Sometime we have a fail to import numpy compilation error if we don't import numpy
import spacy


cpdef list[str] cython_sentence_tok(str text):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    sentences = [sent for sent in doc.sents]

    return sentences

cpdef list[str] cython_pos_tag(str text):
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

    return pos_tags