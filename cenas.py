
from spacy.tokens.token import Token
import spacy

parser = spacy.load('en')

doc = parser(u"There are bananas on the table")

def print_sentence_tree(doc):
    def get_depth(t, depth=0):
        result = {}
        result[t.idx] = depth
        for c in t.children:
            result.update(get_depth(c, depth+1))
        return result

    for root in doc:
        if root.dep_ == "ROOT":
            break

    depths = get_depth(root)
    for t in doc:
        print(' '.join(('   ' * depths[t.idx], t.orth_, t.lemma_, t.pos_, t.tag_, t.dep_)))


print_sentence_tree(doc)
print('')

ss = [
    u"What day is it?",
    u"How many time until eight?",
    u"What day of the week is it?",
    u"What day of the week is December fifth?",
    u"When is the next holiday?",
    u"What day of the week was twenty fourth of April nineteen eighty six?",
    u"What time is it?",
    u"What is the time?",
    u"What day is it?",
    u"What is the day?"
]

for s in ss:
    print("## " + s)
    print_sentence_tree(parser(s))
    print('')

