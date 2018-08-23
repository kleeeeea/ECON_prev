import re
import logging
from unidecode import unidecode
from textblob import TextBlob


def display_concept(w):
    # return w
    return re.sub(r'</?c>', '', w)


re_nonASCII = re.compile(r'[^\x00-\x7F]+')


def removeNonASCII(doc, replaceWithSpace=True, willCondenseSpace=True, soft=True):
    if soft:
        if type(doc) is str:
            doc = doc.decode('utf-8')
        return unidecode(doc)

    if replaceWithSpace:
        doc = re.sub(r'[^\x00-\x7F]+', ' ', doc)
    else:
        doc = re.sub(r'[^\x00-\x7F]+', '', doc)

    if willCondenseSpace:
        doc = condenseSpace(doc)
    # doc = ''.join(i for i in text if ord(i)<128)
    return doc

re_nonLetter = re.compile('[^a-zA-Z]')


def condenseSpace(s):
    return re.sub('([\s])+', '\g<1>', s)


re_line_break = re.compile('\r|\n')


def toOneLine(s, willCondenseSpace=True, willRemoveNonASCII=False):
    s = re_line_break.sub(' ', s)
    if willCondenseSpace:
        s = condenseSpace(s)
    return s


def removeNonLetter(doc, replaceWithSpace=False):
    if replaceWithSpace:
        doc = re.sub(re_nonLetter, ' ', doc)
    else:
        doc = re.sub(re_nonLetter, '', doc)
    # doc = ''.join(i for i in text if ord(i)<128)
    return doc


nonAlphaNumericPunctuation = re.compile(r'[^\w,;:-\[\]]')  #


def tokenize(line, return_str=True):
    para = TextBlob(line)
    sentences_tokenized_list = []
    for sentence in para.sentences:
        if len(sentence.tokens) > 0:
            tokens_as_str_midSentence = ' '.join(sentence.tokens[:-1])
            # remove everything except alphanumeric
            tokens_as_str_midSentence = re.sub(
                nonAlphaNumericPunctuation, ' ', tokens_as_str_midSentence)
            tokens_as_str_midSentence = re.sub(
                ' +', ' ', tokens_as_str_midSentence).strip()
            tokens_as_str = ' '.join(
                [tokens_as_str_midSentence, sentence.tokens[-1]])

            if tokens_as_str:
                sentences_tokenized_list.append(tokens_as_str)

    if return_str:
        return ' '.join(sentences_tokenized_list)

    return sentences_tokenized_list
