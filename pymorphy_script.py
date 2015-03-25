# -*- coding: utf-8 -*-
import string
import pymorphy2

TEST       = "test.txt"
GOLD       = "out_gold.txt"
GIVENGOLD  = "GoldStandard.txt"

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
            #print(line)
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
        pos  = l[0]         
        return "{}\t{}\n".format(token,pos) 
    

def first_1k(gold):
    with open(gold, encoding='utf-8') as infile:
        infile.readline()
        for i in range(0,15):
            line = infile.readline()
            elems = line.split('\t')
            word  = elems[0]
            lemma = elems[1]
            guess = morph.parse(word)[0].normal_form
            print("{}\t\"{}\"\t{}".format(word,lemma,guess))
           
def left_ambig(gold):
    left   = 0.0
    whole = 0.0
    
    with open(gold, encoding='utf-8') as infile:
        infile.readline()
        for i in range(0,1000):
            elems = infile.readline().split('\t')
            word = elems[0]
            tags = "%s" % morph.parse(elems[0])[0].tag
            if tags =="":
                print(lemma)
            else:
                pass
    
left_ambig(GIVENGOLD)

def lex_accuracy(gold):
    pos   = 0.0
    whole = 0.0
     
    with open(gold, encoding='utf-8') as infile:
        infile.readline()
        for i in range(0,1000):
            elems = infile.readline().split('\t')    

            lemma = elems[1]
            guess = morph.parse(elems[0])[0].normal_form    
            if (lemma == guess) and lemma !="":
                pos += 1
            else:
                pass    
            whole +=1
                
    return pos/whole
                
print("lex acc %s" % lex_accuracy(GIVENGOLD))

def postag_accuracy(gold):
    pos   = 0.0
    whole = 0.0
     
    with open(gold, encoding='utf-8') as infile:
        infile.readline()
        for i in range(0,1000):
            elems = infile.readline().split('\t')    

            postag = elems[2]
            tags = "%s" % morph.parse(elems[0])[0].tag
            guess = tags.split(',',1)[0]
            if compare(postag,guess):
                pos += 1
            else:
                pass    
            whole +=1
                
    return pos/whole

def compare(postag,guess):
    if (postag == guess) or postag =="":
        return True
    elif (postag == "S") and (guess == "NOUN"):
        return True
    elif (postag == "A") and (guess == "ADJF" or guess == "ADJS"):
        return True
    elif (postag == "V") and (guess == "VERB" or guess == "INFN" or guess == "PRTS"):
        return True
    elif (postag == "ADV") and (guess == "ADVB"):
        return True
    elif (postag == "SPRO") and (guess == "NPRO"):
        return True
    
    else:
        return False

print("pos tag acc %s" %  postag_accuracy(GIVENGOLD))


#-------------------------------------  
#text = u"Кто-нибудь позвоните Ёжи зачем-либо щекотно-с кому-то"
#tokens = text.split()
#print("pymorphy output: %s" % lemmatize(tokens))
    
#token = "стали"
#strtag = "%s" % morph.parse(token)[0].tag
#print(strtag.split(',',1))
#-------------------------------------
    
prepare_gold()
    
#-------------------------------------
