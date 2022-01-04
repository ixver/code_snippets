
import os, sys
import pandas as pd
import numpy as np
import spacy

from os import listdir
from os.path import isfile, join
from pathlib import Path


# np settings
np.set_printoptions(threshold=sys.maxsize)
np.set_printoptions(precision=2)
np.set_printoptions(edgeitems=30)
np.set_printoptions(linewidth=1100)
np.set_printoptions(formatter=dict(float=lambda x: "%.3g" % x))
np.set_printoptions(suppress=True)

# pd settings
pd.set_option('display.width', 320)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', 200)

sys.path.append(os.path.join(os.path.dirname(__file__), '../_elements/'))

from xos import *
from xpk import *

states = {
    'general': {
        'save_path': os.environ['LIT_SAVE_PATH'],
        'conversionQueue_path': os.environ['LIT_CONVERTQUEUE_PATH'],
    },
    'current': {
        'sourceName': None,
    },
}

''' CONVERTS TEXTS INTO MANY SEPARATE ATTRIBUTES ARRAYS/LAYERS TO BE HANDLED LATER (TAKEN FROM A QUEUE PATH AND SAVED INTO A SAVE PATH)  '''

def vstack_charsRows(_vals, _row):
    if (_vals is None):
        _vals = np.char.array(_row).copy()
    else:
        _vals = np.vstack((_vals, np.char.array(_row))).copy()
    return _vals

def set_nlp(model):
    try:
        nlp = spacy.load(model)
    except:
        spacy.cli.download(model)
        nlp = spacy.load(model)#
    return nlp

def set_doc(nlp, loc):
    with open (loc, "r", encoding='utf-8') as f:
        textblock = f.read()
    doc = nlp(textblock)
    return doc

def get_valNotList(_val):

    if (isinstance(_val, list)):
        if (len(list(_val))>0):
            _val = list(_val)[0]
            _val = get_valNotList(_val)
        else:
            _val = ''

    return _val

def set_filesQueue(states):

    # get list of text files in folder
    conversionQueue_path = states['general']['conversionQueue_path']

    states['current']['conversionQueue'] = [str(conversionQueue_path+f) for f in listdir(conversionQueue_path) if (isfile(join(conversionQueue_path, f)) and ('.txt' in f))]

    return states

def set_literatureData(states, doc):

    def set_textScalesIndices(tokenCurrent, wordInSentence, sentenceInWhole):

        isAfterFirst = tokenCurrent.i != 0
        if (isAfterFirst):

            # if sentence new
            condx = tokenCurrent.is_sent_start
            if (condx):

                wordInSentence = 0
                sentenceInWhole += 1

            else:

                wordInSentence += 1

        return [wordInSentence, sentenceInWhole]

    # initialize

    print ('\n. setting text data')

    # set indices
    tokensTotal = len(doc)

    # words attirbutes
    literature_keysvals = {
        'verbatimWords': [],
        'lemmaWords': [],
        'stemWords': [],

        'wordTypeCourse': [],
        'wordTypeFine': [],
        'syntaxType': [],

        'definiteType': [],
        'pronounType': [],
        'verbformType': [],
        'tenseType': [],
        'povType': [],
        'namedentityType': [],

        'isComplementary': [],
        'isPunct': [],
        'isSpace': [],
        'isNum': [],
        'isAlph': [],

        'isLowercase': [],
        'isUppercase': [],
        'isTitled': [],
        'isQuote': [],
        'isCurrency': [],
        'isUrlLike': [],
        'isEmailLike': [],

        'isPoss': [],
        'isPlural': [],

        'wordInSentence': [],
        # 'wordInWhole': [],
        # 'sentenceInParagraph': [],
        'sentenceInWhole': [],
        # 'paragraphInWhole': [],
    }

    print('\n\t. of {} total words |'.format(tokensTotal), end=' ')
    wordInSentence, wordInWhole, sentenceInParagraph, sentenceInWhole, paragraphInWhole = [0, 0, 0, 0, 0]
    for _i in range(tokensTotal):

        # print doc-token place
        if (_i % 16 ==0):
            print('\n\t\t', end=' ')
        print('{}'.format(_i+1), end=' ')

        tokenCurrent = doc[_i]

        wordInSentence, sentenceInWhole = set_textScalesIndices(tokenCurrent, wordInSentence, sentenceInWhole)

        literature_keysvals['verbatimWords'].append(get_valNotList(tokenCurrent.text))
        literature_keysvals['lemmaWords'].append(get_valNotList(tokenCurrent.lemma_))
        literature_keysvals['stemWords'].append(get_valNotList(tokenCurrent.head.text))

        literature_keysvals['wordTypeCourse'].append(get_valNotList(tokenCurrent.pos_))
        literature_keysvals['wordTypeFine'].append(get_valNotList(tokenCurrent.tag_))
        literature_keysvals['syntaxType'].append(get_valNotList(tokenCurrent.dep_))

        literature_keysvals['definiteType'].append(get_valNotList(tokenCurrent.morph.get('Definite')))
        literature_keysvals['pronounType'].append(get_valNotList(tokenCurrent.morph.get('PronType')))
        literature_keysvals['verbformType'].append(get_valNotList(tokenCurrent.morph.get('VerbForm')))
        literature_keysvals['tenseType'].append(get_valNotList(tokenCurrent.morph.get('Tense')))
        literature_keysvals['povType'].append(get_valNotList(tokenCurrent.morph.get('Person')))
        literature_keysvals['namedentityType'].append(get_valNotList(tokenCurrent.ent_type_))

        literature_keysvals['isComplementary'].append(get_valNotList(tokenCurrent.is_stop))
        literature_keysvals['isPunct'].append(get_valNotList(tokenCurrent.is_punct))
        literature_keysvals['isSpace'].append(get_valNotList(tokenCurrent.is_space))
        literature_keysvals['isNum'].append(get_valNotList(tokenCurrent.is_digit))
        literature_keysvals['isAlph'].append(get_valNotList(tokenCurrent.is_alpha))

        literature_keysvals['isLowercase'].append(get_valNotList(tokenCurrent.is_lower))
        literature_keysvals['isUppercase'].append(get_valNotList(tokenCurrent.is_upper))
        literature_keysvals['isTitled'].append(get_valNotList(tokenCurrent.is_title))
        literature_keysvals['isQuote'].append(get_valNotList(tokenCurrent.is_quote))
        literature_keysvals['isCurrency'].append(get_valNotList(tokenCurrent.is_currency))
        literature_keysvals['isUrlLike'].append(get_valNotList(tokenCurrent.like_url))
        literature_keysvals['isEmailLike'].append(get_valNotList(tokenCurrent.like_email))

        literature_keysvals['isPoss'].append(get_valNotList(tokenCurrent.morph.get('Poss')))
        literature_keysvals['isPlural'].append(get_valNotList(tokenCurrent.morph.get('Number')))

        literature_keysvals['wordInSentence'].append(wordInSentence)
        # literature_keysvals['wordInWhole'].append(sentenceInWhole)
        # literature_keysvals['sentenceInParagraph'].append(sentenceInWhole)
        literature_keysvals['sentenceInWhole'].append(sentenceInWhole)
        # literature_keysvals['paragraphInWhole'].append(sentenceInWhole)

    print('| done')

    return literature_keysvals

def x(states):

    '''
        reference:
    '''

    # initialize nlp
    nlp = set_nlp("en_core_web_lg")

    # set states
    states = set_filesQueue(states)
    conversionQueue = states['current']['conversionQueue']

    # loop files
    for _path in conversionQueue:

        # set source name (name of literature)
        # initialize nlp doc
        states['current']['sourceName'] = str(Path(_path).stem)
        sourcesFolder_path = states['general']['save_path']
        sourceName = states['current']['sourceName']
        doc = set_doc(nlp, _path)

        # set/save types' data
        literature_keysvals = set_literatureData(states, doc)

        # save domain df
        save_pk(literature_keysvals, '{}{}_keysvals.pk'.format(sourcesFolder_path, sourceName))
        print('\n. file has been saved')

    return states

