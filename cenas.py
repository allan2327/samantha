
from spacy.tokens.token import Token
import spacy

parser = spacy.load('en')

doc = parser("There are bananas on the table")

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
        print('   ' * depths[t.idx], t.orth_, t.tag_, t.pos_, t.dep_)


print_sentence_tree(doc)
print('')

ss = [
    "What day is it?",
    "How many time until eight?",
    "What day of the week is it?",
    "What day of the week is December fifth?",
    "When is the next holiday?",
    "What day of the week was twenty fourth of April nineteen eighty six?",
    "What time is it?",
    "What is the time?",
    "What day is it?",
    "What is the day?"
]

for s in ss:
    print("## " + s)
    print_sentence_tree(parser(s))
    print('')


def get_action(token, rule):
    for rule_child for rule.children:
        result = rule_child.evaluate(token)
        if result.action:
            return result

def evaluate_rule(rule, token);
    result = rule.evaluate(token)
    if result:
        return result
    for child_rule in rule.children:
        evaluate_rule(child_rule, token)