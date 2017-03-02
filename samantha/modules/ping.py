
from functools import partial
from samantha.baseclasses import ModuleBase

class Ping(ModuleBase):

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

    def _ping(self, context, data):
        if not context or context.get("last action", None) == 'pong':
            context["last action"] = 'ping'
            return 'pong', context
        return "That not what you should say.", {}
        
    def _pong(self, context, data):
        if not context:
            return "That's not how you start this.", {}
    
        if context.get("last action", None) == 'ping':
            context["last action"] = 'pong'
            return 'ping', context
        return "That not what you should say.", {}
            
