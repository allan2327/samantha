import re
import textblob
from textblob import TextBlob

from samantha.nlputils.wordblobextensions import TextBlobExtended, WordExtended


s1 = "Sometimes I can't see crows buzzing around the tree trunks in my iron-clad yellowed pajamas and boots." #" Don't' fish a fish."
s2 = "I look at the trees dancing."
s3 = "Python is a high-level programming language."
s4 = "What day of the week is December fifth"


ss = [s1, s2, s3, s4]

ss = [
    "What time is it?",
    "How many time until eight?",
    "What day is it?",
    "What day of the week is it?",
    "What day of the week is December fifth?",
    "When is the next holiday?",
    "What day of the week was twenty fourth of April nineteen eighty six?",
    "I want to wake up in five and a half hours."
]

ss = [
    "eight thousand and fifteen apples",
    "minus seven",
    "a cat",
    "thirty seven",
    "a million",
    "seven and a half",
    "five billion and three quarters",
    "four million and three hundred cakes and four dogs",
    "forty two and two half",
    "75943 and a half",
    "I like 3.5 bottles and 4 cakes"
]

for s in ss:
    a = TextBlobExtended(s)
    a.relations
    print(a)
    for w in a._words:
        print(repr(w))
    print('')
    

import sys
from samantha.nlputils.numbers import NumberService

service = NumberService()

# for s in ss:
#     try:
#         print(s)
#         print(service.parse(s))
#     except Exception:
#         print(sys.exc_info())
#     print('')


def process_numbers(s):
    a = s.split(' ')

    result = []
    current = []
    for w in a:
        if w in service.__small__ or \
                w in service.__magnitude__ or \
                w in service.__fractions__ or \
                w == "hundred":
            current.append(w)
        elif w == "and":
            continue
        elif w == "a":
            current.append(w)
        elif current:
            result.append(current)
            current = []
    else:
        if current:
            result.append(current)
            current = []
    return result


## WARNING!!

# >>> service.parse("a half")                                                                                                                                               
# 3                                                                                                                                                                         
# >>> service.parse("half")                                                                                                                                                 
# 2                                                                                                                                                                         
# >>> service.parse("seven and a half")                                                                                                                                     
# 7.5                                                                                                                                                                       
# >>> service.parse("seven a half")                                                                                                                                         
# 10                                                                                                                                                                        
# >>>    



for s in ss:
    print(s)
    processed = process_numbers(s)
    print(processed)
    a = [' '.join(n) for n in processed]
    a = [service.parse(n) for n in a]
    print(a)
    print('')

