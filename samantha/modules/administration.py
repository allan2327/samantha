
from samantha.baseclasses import ModuleBase
import sys

class Administration(ModuleBase):

    def evaluate(self, preprocessed_sentence):
        if "shutdown" in preprocessed_sentence:
            return 1.0
        return 0.0

    def evaluate_with_context(self, preprocessed_sentence):
        return self.evaluate(preprocessed_sentence)

    def act(self, preprocessed_sentence):
        if "shutdown" in preprocessed_sentence:
            sys.exit()
