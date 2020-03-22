import re, string
import numpy as np
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize.toktok import ToktokTokenizer

text = "Algunas de estas palabras deben ser quitadas"

def get_keywords(text):
    text_without_punct = re.sub('[%s]' % re.escape(string.punctuation), ' ', text)
    toktok = ToktokTokenizer()
    texto_tokenized = toktok.tokenize(text_without_punct.lower())

    keywords = [word for word in texto_tokenized if word not in stopwords.words('spanish')]

    return keywords
