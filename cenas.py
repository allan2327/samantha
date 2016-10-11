
import textblob
from textblob import TextBlob


def penn_to_wn(tag):
    if tag in ['JJ', 'JJR', 'JJS']: # is adjective
        return 'a'
    elif tag in ['NN', 'NNS', 'NNP', 'NNPS']: # is noun
        return 'n'
    elif tag in ['RB', 'RBR', 'RBS']: # adverb
        return 'r'
    elif tag in ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']: # is verb
        return 'v'
    return None





s = "Sometimes I can't' see crows buzzing around the tree trunks in my iron-clad yellowed pajamas and boots. Don't' fish a fish."

a = TextBlob(s)

print("### tokenized")
print(a.words)
print()

print("### POS-tagged")
print(a.tags)
print()


# print("### lemmatized")
# print([x.lemmatize() for x in a.words])
# print()

# # for x in a.words:
# #     print(x, x.get_synsets())
# # print()

# print("### lemmatized with POS")
# print([x[0].lemmatize(penn_to_wn(x[1])) for x in a.tags])
# print()

# for x in a.tags:
#     print(x[0], x[0].get_synsets(penn_to_wn(x[1])))
# print()

# print("### NP-chunks")
# print(a.noun_phrases)
# print()

print("### Parse")
for x in a.parse().split(' '):
    print(x.split('/'))
print()