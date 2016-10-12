
from textblob import TextBlob, WordList, Word
from textblob.blob import _penn_to_wordnet
from textblob.tokenizers import word_tokenize
from textblob.decorators import cached_property


class WordListExtended(WordList):
    
    def __init__(self, collection):
        """ collection is a list of (Word, tag), that come from a WordBlol.pos_tags"""
        
        self._collection = [w[0] for w in collection]
        super(WordList, self).__init__(self._collection)


class TextBlobExtended(TextBlob):
    
    @cached_property
    def words(self):
        """ ensures every words has an associated pos tag """
        return WordListExtended(self.pos_tags)
        
    @cached_property
    def pos_tags_with_punctuation(self):
        return [(Word(word, pos_tag=t), unicode(t))
                for word, t in self.pos_tagger.tag(self.raw)]
                
    @cached_property
    def tokens(self):
        return WordListExtended(self.pos_tags_with_punctuation)
        
    # TODO 
    # def parse(self):
    #    stuff
    
    