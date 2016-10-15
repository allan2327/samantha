
from textblob import TextBlob, WordList, Word
from textblob.blob import _penn_to_wordnet
from textblob.compat import unicode
from textblob.utils import PUNCTUATION_REGEX
from textblob.tokenizers import word_tokenize
from textblob.decorators import cached_property



class WordExtended(Word):

    def __init__(self, string, pos_tag=None, chunk=None, preposition=None):
        super(WordExtended, self).__init__(string, pos_tag)
        self.chunk = chunk
        self.preposition = preposition

    def __repr__(self):
        return "{0} {1} {2} {3}".format(self.string, self.pos_tag, self.chunk, self.preposition)


class WordListExtended(WordList):
    
    def __init__(self, collection):
        """ collection is a list of (Word, tag), that come from a WordBlob.pos_tags"""
        
        self._collection = [w[0] for w in collection]
        super(WordList, self).__init__(self._collection)


class TextBlobExtended(TextBlob):
    
    @cached_property
    def words(self):
        """ ensures every words has an associated pos tag """
        return WordListExtended(self.pos_tags)

    @cached_property
    def pos_tags(self):
        return [(WordExtended(word, pos_tag=t), unicode(t))
                for word, t in self.pos_tagger.tag(self.raw)
                if not PUNCTUATION_REGEX.match(unicode(t))]
        
    @cached_property
    def pos_tags_with_punctuation(self):
        return [(WordExtended(word, pos_tag=t), unicode(t))
                for word, t in self.pos_tagger.tag(self.raw)]
                
    @cached_property
    def tokens(self):
        return WordListExtended(self.pos_tags_with_punctuation)
        
    # TODO 
    # def parse(self):
    #    stuff
    
    