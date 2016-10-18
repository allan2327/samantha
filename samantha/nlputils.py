
import re
from textblob import TextBlob, Word, WordList
from textblob.blob import _penn_to_wordnet
from textblob.compat import unicode
from textblob.decorators import cached_property
from textblob.tokenizers import word_tokenize
from textblob.utils import PUNCTUATION_REGEX


class WordExtended(Word):

    def __init__(self, string, pos_tag=None, chunk=None, preposition=None):
        super(WordExtended, self).__init__(string, pos_tag)
        self.chunk = chunk
        self.preposition = preposition

    # def __repr__(self):
    #     return "{0} {1} {2} {3}".format(self.string, self.pos_tag, self.chunk, self.preposition)


class WordListExtended(WordList):
    
    def __init__(self, collection):
        """ collection is a list of (Word, tag), that come from a WordBlob.pos_tags"""
        
        self._collection = [w for w in collection]
        super(WordList, self).__init__(self._collection)


class TextBlobExtended(TextBlob):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._words = None
        self._tagged = False
        self._chunked = False
        
    
    @cached_property
    def words(self):
        if not self._words:
            self.pos_tags_with_punctuation
        return WordListExtended(word for word in self._words
                                if not PUNCTUATION_REGEX.match(word.pos_tag))

    @cached_property
    def pos_tags(self):
        return [tup for tup in self.pos_tags_with_punctuation
                if not PUNCTUATION_REGEX.match(tup[1])]
        
    @cached_property
    def pos_tags_with_punctuation(self):
        if not self._tagged:
            self._words = WordListExtended(WordExtended(word, tag) 
                                           for word, tag in self.pos_tagger.tag(self.raw))
            self._tagged = True
        return [(word, word.pos_tag) for word in self._words]
                
    @cached_property
    def tokens(self):
        if not self._words:
            self.pos_tags_with_punctuation
        return self._words
        
    @cached_property
    def chunks(self):
        if not self._chunked:
            if not self._tagged:
                self.pos_tags_with_punctuation
            chunk_words(self._words)
            calculate_prepositions(self._words)
            self._chunked = True
        return [(word, word.pos_tag, word.chunk, word.preposition) for word in self._words]


SEPARATOR = "/"

NN = r"NN|NNS|NNP|NNPS|NNPS?\-[A-Z]{3,4}|PR|PRP|PRP\$"
VB = r"VB|VBD|VBG|VBN|VBP|VBZ"
JJ = r"JJ|JJR|JJS"
RB = r"(?<!W)RB|RBR|RBS"

# Chunking rules.
CHUNKS_RULES = [
    # Germanic languages: en, de, nl, ...
    (  "NP", re.compile(r"(("+NN+")/)*((DT|CD|CC|CJ)/)*(("+RB+"|"+JJ+")/)*(("+NN+")/)+")),
    (  "PP", re.compile(r"((IN|PP|TO)/)+")),
    (  "VP", re.compile(r"(((MD|"+RB+")/)*(("+VB+")/)+)+")),
    (  "VP", re.compile(r"((MD)/)")),
    ("ADJP", re.compile(r"((CC|CJ|"+RB+"|"+JJ+")/)*(("+JJ+")/)+")),
    ("ADVP", re.compile(r"(("+RB+"|WRB)/)+")),
]

def chunk_words(words, language="en"):
    chunked_words = [x for x in words]
    tags = "".join("%s%s" % (word.pos_tag, SEPARATOR) for word in words)
    # Use Germanic or Romance chunking rules according to given language.
    for tag, rule in CHUNKS_RULES:
        for m in rule.finditer(tags):
            # Find the start of chunks_RULES inside the tags-string.
            # Number of preceding separators = number of preceding tokens.
            i = m.start()
            j = tags[:i].count(SEPARATOR)
            n = m.group(0).count(SEPARATOR)
            for k in range(j, j+n):
                if chunked_words[k].chunk:
                    continue
                # A conjunction can not be start of a chunk.
                if k == j and chunked_words[k].pos_tag in ("CC", "CJ", "KON", "Conj(neven)"):
                    j += 1
                # Mark first token in chunk with B-.
                elif k == j:
                    chunked_words[k].chunk = "B-"+tag
                # Mark other tokens in chunk with I-.
                else:
                    chunked_words[k].chunk = "I-"+tag
    # Mark chinks (tokens outside of a chunk) with O-.
    for chink in filter(lambda x: x.chunk is None, chunked_words):
        chink.chunk = "O"
    # Post-processing corrections.
    for i, word in enumerate(chunked_words):
        if word.pos_tag.startswith("RB") and word.chunk == "B-NP":
            # "Very nice work" (NP) <=> "Perhaps" (ADVP) + "you" (NP).
            if i < len(chunked_words)-1 and not chunked_words[i+1].pos_tag.startswith("JJ"):
                chunked_words[i+0].chunk = "B-ADVP"
                chunked_words[i+1].chunk = "B-NP"
    return chunked_words


def calculate_prepositions(chunked_words):
    # Tokens that are not part of a preposition just get the O-tag.
    for word in chunked_words:
        word.preposition = "O"
    for i, word in enumerate(chunked_words):
        if word.chunk.endswith("PP") and word.preposition == "O":
            # Find PP followed by other PP, NP with nouns and pronouns, VP with a gerund.
            if i < len(chunked_words)-1 and \
             (chunked_words[i+1].chunk.endswith(("NP", "PP")) or \
              chunked_words[i+1].pos_tag in ("VBG", "VBN")):
                word.preposition = "B-PNP"
                pp = True
                for w in chunked_words[i+1:]:
                    if not (w.chunk.endswith(("NP", "PP")) or w.pos_tag in ("VBG", "VBN")):
                        break
                    if w.chunk.endswith("PP") and pp:
                        w.preposition = "I-PNP"
                    if not w.chunk.endswith("PP"):
                        w.preposition = "I-PNP"
                        pp = False
    return chunked_words