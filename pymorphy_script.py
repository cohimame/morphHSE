# -*- coding: utf-8 -*-
import string
import pymorphy2

TEST = "test.txt"
GOLD = "out_gold.txt"

pnkt = set(string.punctuation)
pnkt.remove("-")

morph = pymorphy2.MorphAnalyzer()

def split(text):
    result = text
    for p in pnkt:
        result = result.replace(p, " {} ".format(p))
    return result.split()


def lemmatize_word(w):
    return morph.parse(w)[0].normal_form

def lemmatize(tokens):
    return [lemmatize_word(t) for t in tokens]


def prepare_gold():    
    with open(TEST) as infile:
        text = infile.read()
        
    tokens = split(text)
    
    with open(GOLD, mode = "w" ,encoding='utf-8') as outfile:
        outfile.write("Wordform_GS2\tLemma_GS2\tPOS_GS2\tGram_GS2\n")
        for token in tokens:
            line = parse(token)
            print(line)
            outfile.write(line)    


def parse(token):
    parsed  = morph.parse(token)[0]
    norm = parsed.normal_form
    tags = "%s" % parsed.tag
    l  = tags.split(',',1)
    if len(l)>1:
        pos,other = l[0],l[1]
        return "{}\t{}\t{}\t{}\n".format(token,norm,pos,other)
    else:
        return "{}\n".format(token) 
    
    
  
#text = u"Кто-нибудь позвоните Ёжи зачем-либо щекотно-с кому-то"
#tokens = text.split()
#print("pymorphy output: %s" % lemmatize(tokens))
    
token = "стали"
strtag = "%s" % morph.parse(token)[0].tag
print(strtag.split(',',1))

prepare_gold()
