
import sys
from functools import partial

from samantha.baseclasses import ModuleBase


class Administration(ModuleBase):

    def evaluate(self, preprocessed_sentence, context):
        rules = self.grammar.find_matching_rules(preprocessed_sentence)
        if rules:
            return 1.0, rules[0].action
        return 0.0, None

    def evaluate_with_context(self, preprocessed_sentence, context):
        return self.evaluate(preprocessed_sentence, context)
        
    def execute(self, action, context, data):
        method = getattr(self, '_' + action)
        return method(context, data)

    def _shutdown(self, context, data):
        sys.exit()
