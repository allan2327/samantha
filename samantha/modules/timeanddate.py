
import arrow

from samantha.baseclasses import ModuleBase
from samantha.nlputils import search_token


class TimeAndDate(ModuleBase):
    
    def evaluate(self, preprocessed_sentence, context):
        root = next(preprocessed_sentence.sents).root
        
        if root.lemma_ == 'be':
            if search_token(root.lefts, lemma="time", pos="NOUN"):
                if search_token(root.rights, lemma="it", pos="PRON"):
                    # "What day is it?"
                    return 1.0, self.get_time
                else:
                    # maybe handle alternatives to "it"
                    pass
            if search_token(root.rights, lemma="time", pos="NOUN"):
                # "What is the time."
                return 1.0, self.get_time

        return 0.0, None    
    

    def evaluate_with_context(self, preprocessed_sentence, context):
        return self.evaluate(preprocessed_sentence, context)

    
    def get_time(self, context):
        time = arrow.now()
        s = "It's {} hours and {} minutes".format(time.hour, time.minute)
        return s, {}
        
        
    def get_date(self, context):
        return "You want the date", {}
        
    def get_day_of_the_week(self, context):
        return "You want the day of the week", {}
        
        