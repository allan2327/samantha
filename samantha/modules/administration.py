
from functools import partial
from samantha.baseclasses import ModuleBase
import sys

class Administration(ModuleBase):

    def evaluate(self, preprocessed_sentence, context):
        if len(preprocessed_sentence) > 1:
            return 0.0, None
        
        root = preprocessed_sentence.sents.next().root
        if root.orth_ == "shutdown":
            return 1.0, self.shutdown
        return 0.0, None

    def evaluate_with_context(self, preprocessed_sentence, context):
        return self.evaluate(preprocessed_sentence, context)

            
    def shutdown(self, context):
        sys.exit()