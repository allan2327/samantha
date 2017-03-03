
from collections import namedtuple, defaultdict
import spacy


EvaluatedModule = namedtuple('EvaluatedModule', ['score', 'module', 'action'])


class Brain(object):
    
    def __init__(self, modules=None):
        print("Starting")
        self.modules = modules or []
        self.last_module = None
        self.context = defaultdict(dict)
        print("Loading NLP modules...")
        self.parser = spacy.load("en")
        print("NLP modules loaded.")

        
    @staticmethod
    def none_f():
        return None
        

    def _preprocess_sentence(self, sentence):
        preprocessed_sentence = self.parser(sentence)
        # debug
        print()
        print(self._get_printable_sentence_tree(preprocessed_sentence))
        # debug end
        return preprocessed_sentence

        
    def _select_module(self, preprocessed_sentence):
        evaluated_modules = []
        for module in self.modules:
            score, action = module.evaluate(preprocessed_sentence, self.context[module.name])
            if module == self.last_module:
                score = score * 2   # TODO magic number
            evaluated_modules.append(EvaluatedModule(score, module, action))
            
        evaluated_modules.sort(key=lambda x: x.score)
        selected_module = evaluated_modules[-1]
        return selected_module.score, selected_module.module, selected_module.action
        
        
    def _act(self, module, action):
        module_name = module.name
        print(self.last_module)
        if module != self.last_module:
            if self.last_module:
                self.context.pop(self.last_module.name, None)    # delete entry
        response, self.context[module_name] = module.execute(action, self.context[module_name], None)
        self.last_module = module
        return response, self.context

            
    def _get_printable_sentence_tree(self, doc):
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
        s = ''
        for t in doc:
            s = s + ' '.join(('   ' * depths[t.idx], t.orth_, t.lemma_, t.pos_, t.tag_, t.dep_)) + '\n'
        return s

    def handle(self, sentence):
        preprocessed_sentence = self._preprocess_sentence(sentence)
        score, module, action = self._select_module(preprocessed_sentence)
        
        if not action or score < 0.4: # TODO magic number
            return "Sorry, I don't understand what you mean.", self.context
        return self._act(module, action)



    
