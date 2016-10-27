
import re
from textblob import TextBlob, Word, WordList
from textblob.blob import _penn_to_wordnet
from textblob.compat import unicode
from textblob.decorators import cached_property
from textblob.tokenizers import word_tokenize
from textblob.utils import PUNCTUATION_REGEX


class WordExtended(Word):

    def __init__(self, string, pos_tag=None, chunk=None, preposition=None, relation=None):
        super(WordExtended, self).__init__(string, pos_tag)
        self.chunk = chunk
        self.preposition = preposition
        self.relation = relation

    def __repr__(self):
        return "{0} {1} {2} {3} {4}".format(self.string, self.pos_tag, self.chunk, self.preposition, self.relation)


class WordListExtended(WordList):
    
    def __init__(self, collection):
        """ collection is a list of (Word, tag), that come from a WordBlob.pos_tags"""
        
        self._collection = [w for w in collection]
        super(WordList, self).__init__(self._collection)


class TextBlobExtended(TextBlob):

    def __init__(self, *args, **kwargs):
        super(TextBlobExtended, self).__init__(*args, **kwargs)
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
        
    @cached_property
    def relations(self):
        if not self._chunked:
            self.chunks
        calculate_relations(self._words)
        return self._words

        
###################################################
###   Chunker and semantic role labeler         ###
###   conviniently 'borrowed' from CLIPS's      ###
###   pattern module:                           ###
###   http://www.clips.ua.ac.be/pages/pattern   ###
###################################################

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


BE = dict.fromkeys(("be", "am", "are", "is", "being", "was", "were", "been"), True)
GO = dict.fromkeys(("go", "goes", "going", "went"), True)

def calculate_relations(chunked_words):
    """ The input is a list of [token, tag, chunk]-items.
        The output is a list of [token, tag, chunk, relation]-items.
        A noun phrase preceding a verb phrase is perceived as sentence subject.
        A noun phrase following a verb phrase is perceived as sentence object.
    """
    tag = lambda word: word.chunk.split("-")[-1] # B-NP => NP
    # Group successive tokens with the same chunk-tag.
    chunks = []
    for word in chunked_words:
        if len(chunks) == 0 \
        or word.chunk.startswith("B-") \
        or tag(word) != tag(chunks[-1][-1]):
            chunks.append([])
        word.relation = "O"
        chunks[-1].append(word)
    # If a VP is preceded by a NP, the NP is tagged as NP-SBJ-(id).
    # If a VP is followed by a NP, the NP is tagged as NP-OBJ-(id).
    # Chunks that are not part of a relation get an O-tag.
    id = 0
    for i, chunk in enumerate(chunks):
        if tag(chunk[-1]) == "VP" and i > 0 and tag(chunks[i-1][-1]) == "NP":
            if chunk[-1].relation == "O":
                id += 1
            for token in chunk:
                token.relation = "VP-" + str(id)
            for token in chunks[i-1]:
                token.relation += "*NP-SBJ-" + str(id)
                token.relation = token.relation.lstrip("O-*")
        if tag(chunk[-1]) == "VP" and i < len(chunks)-1 and tag(chunks[i+1][-1]) == "NP":
            if chunk[-1].relation == "O":
                id += 1
            for token in chunk:
                token.relation = "VP-" + str(id)
            for token in chunks[i+1]:
                token.relation = "*NP-OBJ-" + str(id)
                token.relation = token.relation.lstrip("O-*")
    # This is more a proof-of-concept than useful in practice:
    # PP-LOC = be + in|at + the|my
    # PP-DIR = go + to|towards + the|my
    for i, chunk in enumerate(chunks):
        if 0 < i < len(chunks)-1 and len(chunk) == 1 and chunk[-1].relation == "O":
            t0, t1, t2 = chunks[i-1][-1], chunks[i][0], chunks[i+1][0] # previous / current / next
            if tag(t1) == "PP" and t2.pos_tag in ("DT", "PR", "PRP$"):
                if t0.string in BE and t1.string in ("in", "at")      : t1.relation = "PP-LOC"
                if t0.string in GO and t1.string in ("to", "towards") : t1.relation = "PP-DIR"
    # related = []; [related.extend(chunk) for chunk in chunks]
    return chunked_words
