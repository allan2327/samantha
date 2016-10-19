import re
import textblob
from textblob import TextBlob

from samantha.nlputils import TextBlobExtended, WordExtended


s1 = "Sometimes I can't see crows buzzing around the tree trunks in my iron-clad yellowed pajamas and boots." #" Don't' fish a fish."
s2 = "I look at the trees dancing."
s3 = "Python is a high-level programming language."
s4 = "What day of the week is December fifth"


ss = [s1, s2, s3, s4]

ss = [
    "What time is it?",
    "What day is it?",
    "How many time until eight?",
    "What day of the week is it?",
    "What day of the week is December fifth?",
    "When is the next holiday?",
    "What day of the week was twenty fourth of April nineteen eighty six?"
]

for s in ss:
    a = TextBlobExtended(s)
    a.relations
    print(a)
    for w in a._words:
        print(repr(w))
    print('')
    
    
    
a = TextBlob("I like to ride my bycicle. Specially in the summer. Tomorrow I can't swim.")




