
import arrow

from samantha.baseclasses import ModuleBase
from samantha.nlputils import search_token


class TimeAndDate(ModuleBase):
    
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
    
    def _get_time(self, context, data):
        time = arrow.now()
        s = "It's {} hours and {} minutes".format(time.hour, time.minute)
        return s, {}   
        
    def _get_date(self, context, data):
        return "You want the date", {}
        
    def _get_day_of_the_week(self, context, data):
        return "You want the day of the week", {}
        
        