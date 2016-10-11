
from samantha.baseclasses import ModuleBase

class Ping(ModuleBase):

    def __init__(self):
        self.context = None

    def evaluate(self, preprocessed_sentence):
        if "ping" in preprocessed_sentence:
            return 1.0
        return 0.0

    def evaluate_with_context(self, preprocessed_sentence):
        if "pong" in preprocessed_sentence or "ping" in preprocessed_sentence:
            return 1.0
        return 0.0

    def act(self, preprocessed_sentence):
        keyword = None
        if "ping" in preprocessed_sentence:
            keyword = "ping"
        elif "pong" in preprocessed_sentence:
            keyword = "pong"
        
        if self.context:
            if self.context == keyword:
                self.context = None
                return "That not what you should say."
            else:
                self.context = keyword
                return "ping" if keyword == "pong" else "pong"
        else:
            if keyword != "ping":
                return "That's not who you start this."
            else:
                self.context = keyword
                return "pong"
        