
from samantha.baseclasses import ModuleBase

class TimeAndDate(ModuleBase):
    
    def evaluate(self, processed_sentence, context):
        root = preprocessed_sentence.sents.next().root
        
        if root.lemma_ != 'be':
            for 
    
    
    
    def get_time(self, context):
        return "You want the time", {}
        
        
    def get_date(self, context):
        return "You want the date", {}
        
        
        
        
        
def search_token(token_list, lemma= recursive = False):
    