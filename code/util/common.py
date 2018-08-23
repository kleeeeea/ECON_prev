from multiprocessing import Pool
import errno
import itertools
import os
import concurrent.futures
import multiprocessing
import subprocess
from collections import defaultdict
from random import choice
from string import ascii_uppercase
from collections import Counter
import re
import logging
from unidecode import unidecode


RE_LINEBREAK = re.compile('\r|\n')

FIELD_SEPARATER = '|'


def head_file(file, N=10):
    try:
        with open(file) as myfile:
            head = [next(myfile) for x in xrange(N)]
        return head
    except Exception, e:
        print e


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def batch_iter(iter, total=None, batch_size=2000):
    l = next(iter)
    ls = []

    while l:
        ls.append(l)

        if len(ls) >= batch_size:
            yield ls
            ls = []
        l = next(iter, '')

    if ls:
        yield ls


def make_parentdir(path):
    mkdir_p(os.path.dirname(path))

DATASETS = ['machine_learning', 'pubmed', 'database']

DEFAULT_LOGGER_FILE = './log1/default.log'


def getLogger(name='jobs', will_add_time_to_name=False, trim_to_base_path=True):
    if trim_to_base_path:
        name = os.path.basename(name)
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s ::: %(name)s ::: %(levelname)s ::: %(message)s')

    fh = logging.FileHandler(os.path.join(os.path.dirname(DEFAULT_LOGGER_FILE), name), mode='a')
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    sh = logging.StreamHandler()
    sh.setLevel(logging.DEBUG)

    logger.addHandler(fh)
    logger.addHandler(sh)

    return logger


def flatten(listOfLists):
    return [item for sublist in listOfLists for item in sublist]


def get_line_count(inFile):
    count = -1
    for count, line in enumerate(open(inFile, 'r')):
        pass
    count += 1
    return count


def process_by_line(input_file, output_file, func, print_progress=False):
    with open(output_file, 'w') as f_w:
        for line in open(input_file):
            line_o = func(line)
            if print_progress:
                print line_o
            f_w.write(line_o.strip() + '\n')


def process_by_line_batch(input_file, output_file, func, print_progress=False, batch_size=32):
    pool = Pool(processes=128)
    with open(output_file, 'w') as f_w:
        for lines in batch_iter(open(input_file), batch_size=batch_size):
            line_o_list = pool.map(func, lines)
            if print_progress:
                print line_o_list
            line_o_list_str = [line_o.strip() + '\n' for line_o in line_o_list]
            f_w.write(''.join(line_o_list_str))


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
