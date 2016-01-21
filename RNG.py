from nltk.corpus import wordnet as words
import random
class rng:
    def __init__(self):
        self.nouns=list(words.all_synsets('n'))
        self.adjectives=list(words.all_synsets('a'))

    def generate(self,list):
        names=list[random.randint(0,len(list)-1)].lemma_names()[0]
        names=names.replace("'","")
        names = names.replace("-","_")
        names = names.split("_")
        names=[name.title() for name in names]
        return ''.join(names)

    def getName(self):
        return self.generate(self.adjectives)+self.generate(self.nouns)
