
import yaml
from attr import attrs, attrib


@attrs
class GrammarWord():
    name = attrib()
    orth = attrib()
    lemma = attrib()
    pos = attrib()
    tag = attrib()
    dep = attrib()
    
    def is_equal_to_token(self, token):
        if self.orth and self.orth != token.orth_:
            return False
        if self.lemma and self.lemma != token.lemma_:
            return False
        if self.pos and self.pos != token.pos_:
            return False
        if self.tag and self.tag != token.tag_:
            return False
        if self.dep and self.dep != token.dep_:
            return False
        return True
        
    
@attrs
class GrammarRule():
    name = attrib()
    action = attrib()
    left = attrib()
    root = attrib()
    right = attrib()


@attrs
class Grammar():
    words = attrib()
    rules = attrib()
    
    def match_grammar_words(self, words, tokens):
        if not words:
            return True
            
        def find_match(words, tokens):  
            if not words:
                return True
            if not tokens:
                return False
            if words[0].is_equal_to_token(tokens[0]):
                return find_match(words[1:], tokens[1:])
            else:
                return False
            
        for i, _ in enumerate(tokens):
            if find_match(words, tokens[i:]):
                return True
        return False
               
    def find_matching_rules(self, doc):
        for t in doc:
            if t.dep_ == 'ROOT':
                root = t
                break
        else:
            return []
    
        matches = []
        for _, rule in self.rules.items():
            if not rule.root.is_equal_to_token(root):
                continue
            if self.match_grammar_words(rule.left, doc[:root.i]) and self.match_grammar_words(rule.right, doc[root.i+1:]):
                matches.append(rule)
        return matches

        
def create_grammar(yaml_file):
    with open(yaml_file, 'r') as input:
        data = yaml.load(input)
        
    words = {}
    for k, v in data['words'].items():
        words[k] = GrammarWord(name = k, 
                               orth = v.get('orth', None), 
                               lemma = v.get('lemma', None), 
                               pos = v.get('pos', None), 
                               tag = v.get('tag', None), 
                               dep = v.get('dep', None))
    
    rules = {}
    for k, v in data['rules'].items():
        rules[k] = GrammarRule(name = k,
                               action = v.get('action'),
                               left = [words[x] for x in v.get('left', [])],
                               root = words[v.get('root')],
                               right = [words[x] for x in v.get('right', [])])
    
    return Grammar(words = words, rules = rules)