'''
Tokenizer module.
Tokenizer.tokenize("Sentence")
Input: String
Output: List(tokens)
'''

import re

abbreviations = ['Mr.', 'Mrs.', 'Dr.', 'Er.', 'Prof.'
                 'A.S.A.P.', 'E.T.A.', 'D.I.Y.', 'St.', 'Ln.', 'Ave.',
                 'A.D.', 'B.S.', 'A.M.', 'P.M.', 'C.V.', 'D.V.',
                 'et al.', 'etc.', 'e.g.', 'i.e.', 'op. cit.', 'p.a.',
                 'Ph.D.', 'p.p.', 'P.S.', 'R.I.P.', 'S.O.S', 'stat.',
                 'viz.', 'vs.', 'Rs.', 'Re.'
                 ]
reg = []
# For abbreviations
reg.append('(?:\W(?:'+'|'.join([re.escape(k) for k in abbreviations])+'))')
# For numbers like "I have_.899"
reg.append(" (?:\.[0-9]+)+")
# For numbers like "I have 12.899.I went home"
reg.append("[+-]?(?:[0-9]+[\.,])+[0-9]+")
# For url names, matches after some manipulation
reg.append("(?:http|https|ftp|sftp|ssh):\/\/(?:\w+\.)+\w+(?:/w+)*")
reg.append("(?:\w+\.)+(?:com|net|co|org|gov|edu|mil)(?:\.\w\w)?")
# For remaining dots
reg.append('\.')
# Merge all regex into one
split_pat = re.compile('('+'|'.join(reg)+')', re.IGNORECASE)

contractions = {
    "wanna": "want to",
    "gonna": "going to",

    "i'd better": "i had better",
    "i'd": "i would",
    "i'll": "i will",
    "i'm": "i am",
    "i've": "i have",
    "you'd": "you would",
    "you're": "you are",
    "you've": "you have",
    "you'll": "you will",
    "he's": "he is",
    "he'd": "he would",
    "he'll": "he will",
    "she's": "she is",
    "she'd": "she would",
    "she'll": "she will",
    "we're": "we are",
    "we'd": "we would",
    "we'll": "we will",
    "we've": "we have",
    "they're": "they are",
    "they'd": "they would",
    "they'll": "they will",
    "they've": "they have",

    "y'all": "you all",

    "can't": "can not",
    "cannot": "can not",
    "couldn't": "could not",
    "wouldn't": "would not",
    "shouldn't": "should not",

    "isn't": "is not",
    "ain't": "is not",
    "don't": "do not",
    "aren't": "are not",
    "won't": "will not",
    "weren't": "were not",
    "wasn't": "was not",
    "didn't": "did not",
    "hasn't": "has not",
    "hadn't": "had not",
    "haven't": "have not",

    "where's": "where is",
    "where'd": "where did",
    "where'll": "where will",
    "who's": "who is",
    "who'd": "who did",
    "who'll": "who will",
    "what's": "what is",
    "what'd": "what did",
    "what'll": "what will",
    "when's": "when is",
    "when'd": "when did",
    "when'll": "when will",
    "why's": "why is",
    "why'd": "why did",
    "why'll": "why will",

    "it's": "it is",
    "it'd": "it would",
    "it'll": "it will",
}
cont_esc = dict((re.escape(k), v) for k, v in contractions.items())
# Sorting the dict will enusure "I'd better' is always before "I'd"
cont_pat = re.compile("|".join(sorted(cont_esc.keys(), reverse=True)),
                      re.IGNORECASE)


# Remove redundancy
def _fix_redundancy(sentence, punctuations):
    for punc in punctuations:
        from_ = '\{}+'.format(punc)
        to_ = '{}'.format(punc)
        sentence = re.sub(from_, to_, sentence)
    return sentence


# Add spaces around some puncuations so that they are easily tokenized
# using split()
def _fix_spacing(sentence, punctuations):
    for punc in punctuations:
        from_ = '\{}'.format(punc)
        to_ = ' {} '.format(punc)
        sentence = re.sub(from_, to_, sentence)
    sentence = re.sub(' +', ' ', sentence)
    return sentence


# _fix common mistakes in ratios like 1 : 2
def _fix_ratio(sentence):
    sentence = re.sub('(?<=\D) *: *(?=\D)', ' : ', sentence)
    sentence = re.sub('(?<=\d) *: *(?=\d)', ':', sentence)
    return sentence


# _fix common mistakes in url like http : / myname.com
def _fix_url(sentence):
    sentence = re.sub(
        "(?P<a>http|https|ftp|sftp|ssh) *: *\/ *", "\g<a>://", sentence)
    return sentence


# _fix commas like a,b,c which must be a, b, c except for 1,2,3
def _fix_comma(sentence):
    # Split words like hari,shyam,kiran and leave 1,2,3
    sentence = re.sub('(?<=\d)\,(?=\D)', ' , ', sentence)
    sentence = re.sub('(?<=\D)\,(?=\d)', ' , ', sentence)
    sentence = re.sub('(?<=\D)\,(?=\D)', ' , ', sentence)
    return sentence


def _fix_contractions(sentence):
    global cont_esc
    global cont_pat
    return cont_pat.sub(lambda m: cont_esc[re.escape(m.group(0)).lower()],
                        sentence)


def _fix_dot(tokens):
    # Split using 're_all' then split the resulting list using 'space'
    # then get all the items excluding ''
    global split_pat
    sp = [el for em in split_pat.split(tokens) for el in em.split() if el]
    return sp


# Change some punctuations in standard form
def _fix_punctuations(lst):
    # Add punctuation at last if none exists.
    if lst and lst[-1] not in {'.', '?', '!'}:
        lst.append('.')
    return lst


def tokenize(sentences):
    # For punctuations without non-special cases
    common = ['!', '?', ';', '/', '|']
    redundant = ['.', ',', ':']
    spacing = ['"', '(', ')', '[', ']', '{', '}']
    sentences = sentences.lower()
    sentences = _fix_redundancy(sentences, common+redundant)
    sentences = _fix_contractions(_fix_spacing(sentences, common+spacing))
    sentences = _fix_dot(_fix_url(_fix_ratio(_fix_comma(sentences))))
    return _fix_punctuations(sentences)
