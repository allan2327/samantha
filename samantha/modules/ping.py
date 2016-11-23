
from functools import partial
from samantha.baseclasses import ModuleBase

class Ping(ModuleBase):

    def evaluate(self, preprocessed_sentence, context):
        root = next(preprocessed_sentence.sents).root
        
        if root.orth_ not in ["ping", "pong"]:
            return 0.0, None
        
        action = 0
        if context: # has context, not first use
            if root.orth_ == context["last word"]:
                if root.orth_ == "ping":
                    action = self.pong
                else:
                    action = self.ping
            else:
                action = self.bad_word
        else:
            if root.orth_ == "ping":
                action = self.pong
            else:
                action = self.bad_start
        return 1.0, action
                
        
    def evaluate_with_context(self, preprocessed_sentence, context):
        return self.evaluate(preprocessed_sentence, context)

    
    def ping(self, context):
        context["last word"] = "ping"
        return "ping", context
    
    
    def pong(self, context):
        context["last word"] = "pong"
        return "pong", context
    
    
    def bad_start(self, context):
        return "That's not how you start this.", {}
    
    
    def bad_word(self, context):
        return "That not what you should say.", {}    # resets context