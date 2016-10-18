
import textblob
from textblob import TextBlob

from samantha.nlputils import TextBlobExtended, WordExtended

s1 = "Sometimes I can't see crows buzzing around the tree trunks in my iron-clad yellowed pajamas and boots." #" Don't' fish a fish."
s2 = "I look at the trees dancing."
s3 = "Python is a high-level programming language."



while False:
    a = input('> ')
    a = TextBlobExtended(a)
    for w in a.chunks:
        print('==> {}'.format(w))


a = TextBlobExtended("I sleep in the bed.")
print(a.chunks)
print('')

w = a.words[1]
print(w)
print(w.pos_tag)
print(w.lemma)
print(w.synsets)
print(w.definitions)


