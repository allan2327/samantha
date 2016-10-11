
from collections import namedtuple

EvaluatedModule = namedtuple('EvaluatedModule', ['score', 'module'])


class Brain:
    
    def __init__(self, listener=None, speaker=None, modules=None):
        self.listener = listener
        self.speaker = speaker
        self.modules = modules or []
        self.in_context_module = None
        print("Starting")

    def _preprocess_sentence(self, sentence):
        return sentence

    def _select_module(self, preprocessed_sentence):
        evaluated_modules = []
        for module in self.modules:
            score = module.evaluate(preprocessed_sentence)
            evaluated_modules.append(EvaluatedModule(score, module))
        
        if self.in_context_module:
            score = self.in_context_module.evaluate_with_context(preprocessed_sentence)
            evaluated_modules.append(EvaluatedModule(score*2, self.in_context_module)) # TODO magic number
        
        evaluated_modules.sort(key=lambda x: x.score)
        evaluated_modules.reverse()
        selected_module = evaluated_modules[0]
        return selected_module.module, selected_module.score

    def _act(self, module, preprocess_sentence):
        response = module.act(preprocess_sentence)
        if response:
            speaker.say(response)

    def run(self):
        while True:
            sentence = self.listener.listen()
            preprocessed_sentence = self._preprocess_sentence(sentence)
            module, score = self._select_module(preprocessed_sentence)
            
            if score < 0.4: # TODO magic number
                self.speaker.speak("Sorry, I don't understand what you mean.")
                continue
            
            self.in_context_module = module
            response = module.act(preprocessed_sentence)
            if response:
                self.speaker.speak(response)
            

        
