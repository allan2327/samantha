
import re
import textblob
from textblob import TextBlob

from samantha.nlputils import TextBlobExtended

s1 = "Sometimes I can't see crows buzzing around the tree trunks in my iron-clad yellowed pajamas and boots." #" Don't' fish a fish."
s2 = "I look at the trees dancing."

a = TextBlobExtended(s1)


# for x in a.words:
#     print(x, x.pos_tag)
# print('')

# for x in a.tokens:
#     print(x, x.pos_tag)
# print('')

# for x in a.pos_tags:
#     print(x[0], x[0].pos_tag, x[1])
# print('')

# for x in a.pos_tags_with_punctuation:
#     print(x)
# print('')



SEPARATOR = "/"

NN = r"NN|NNS|NNP|NNPS|NNPS?\-[A-Z]{3,4}|PR|PRP|PRP\$"
VB = r"VB|VBD|VBG|VBN|VBP|VBZ"
JJ = r"JJ|JJR|JJS"
RB = r"(?<!W)RB|RBR|RBS"

# Chunking rules.
# CHUNKS[0] = Germanic: RB + JJ precedes NN ("the round table").
# CHUNKS[1] = Romance: RB + JJ precedes or follows NN ("la table ronde", "une jolie fille").
CHUNKS = [
    # Germanic languages: en, de, nl, ...
    (  "NP", re.compile(r"(("+NN+")/)*((DT|CD|CC|CJ)/)*(("+RB+"|"+JJ+")/)*(("+NN+")/)+")),
    (  "PP", re.compile(r"((IN|PP|TO)/)+")),
    (  "VP", re.compile(r"(((MD|"+RB+")/)*(("+VB+")/)+)+")),
    (  "VP", re.compile(r"((MD)/)")),
    ("ADJP", re.compile(r"((CC|CJ|"+RB+"|"+JJ+")/)*(("+JJ+")/)+")),
    ("ADVP", re.compile(r"(("+RB+"|WRB)/)+")),
]


def find_chunks(tagged, language="en"):
    """ The input is a list of [token, tag]-items.
        The output is a list of [token, tag, chunk]-items:
        The/DT nice/JJ fish/NN is/VBZ dead/JJ ./. =>
        The/DT/B-NP nice/JJ/I-NP fish/NN/I-NP is/VBZ/B-VP dead/JJ/B-ADJP ././O
    """
    chunked = [x for x in tagged]
    tags = "".join("%s%s" % (token.pos_tag, SEPARATOR) for token in tagged)
    # Use Germanic or Romance chunking rules according to given language.
    for tag, rule in CHUNKS:
        for m in rule.finditer(tags):
            # Find the start of chunks inside the tags-string.
            # Number of preceding separators = number of preceding tokens.
            i = m.start()
            j = tags[:i].count(SEPARATOR)
            n = m.group(0).count(SEPARATOR)
            for k in range(j, j+n):
                if chunked[k].chunk:
                    continue
                # A conjunction can not be start of a chunk.
                if k == j and chunked[k].pos_tag in ("CC", "CJ", "KON", "Conj(neven)"):
                    j += 1
                # Mark first token in chunk with B-.
                elif k == j:
                    chunked[k].chunk = "B-"+tag
                # Mark other tokens in chunk with I-.
                else:
                    chunked[k].chunk = "I-"+tag
    # Mark chinks (tokens outside of a chunk) with O-.
    for chink in filter(lambda x: len(x) < 3, chunked):
        chink.chunk = "O"
    # Post-processing corrections.
    for i, word in enumerate(chunked):
        if word.pos_tag.startswith("RB") and word.chunk == "B-NP":
            # "Very nice work" (NP) <=> "Perhaps" (ADVP) + "you" (NP).
            if i < len(chunked)-1 and not chunked[i+1].pos_tag.startswith("JJ"):
                chunked[i+0].chunk = "B-ADVP"
                chunked[i+1].chunk = "B-NP"
    return chunked

def find_prepositions(chunked):
    """ The input is a list of [token, tag, chunk]-items.
        The output is a list of [token, tag, chunk, preposition]-items.
        PP-chunks followed by NP-chunks make up a PNP-chunk.
    """
    # Tokens that are not part of a preposition just get the O-tag.
    for ch in chunked:
        ch.preposition = "O"
    for i, chunk in enumerate(chunked):
        if chunk.chunk.endswith("PP") and chunk.preposition == "O":
            # Find PP followed by other PP, NP with nouns and pronouns, VP with a gerund.
            if i < len(chunked)-1 and \
             (chunked[i+1].chunk.endswith(("NP", "PP")) or \
              chunked[i+1].pos_tag in ("VBG", "VBN")):
                chunk.preposition = "B-PNP"
                pp = True
                for ch in chunked[i+1:]:
                    if not (ch.chunk.endswith(("NP", "PP")) or ch.pos_tag in ("VBG", "VBN")):
                        break
                    if ch.chunk.endswith("PP") and pp:
                        ch.preposition = "I-PNP"
                    if not ch.chunk.endswith("PP"):
                        ch.preposition = "I-PNP"
                        pp = False
    return chunked



b = [t[0]for t in a.pos_tags_with_punctuation]

print(b)
print('')
print(find_prepositions(find_chunks(b)))
print('')
print(a.parse().replace(' ', '\n'))

# for i, j in zip(a.parse().split(' '), find_prepositions(find_chunks(b))):
#     print(i.split('/'), '   ', j)


