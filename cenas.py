import re
import textblob
from textblob import TextBlob

from samantha.nlputils import TextBlobExtended, WordExtended


SEPARATOR = "/"

NN = r"NN|NNS|NNP|NNPS|NNPS?\-[A-Z]{3,4}|PR|PRP|PRP\$"
VB = r"VB|VBD|VBG|VBN|VBP|VBZ"
JJ = r"JJ|JJR|JJS"
RB = r"(?<!W)RB|RBR|RBS"
CC = r"CC|CJ"

# Chunking rules.
# CHUNKS[0] = Germanic: RB + JJ precedes NN ("the round table").
# CHUNKS[1] = Romance: RB + JJ precedes or follows NN ("la table ronde", "une jolie fille").
CHUNKS = [[
    # Germanic languages: en, de, nl, ...
    (  "NP", r"((NN)/)* ((DT|CD|CC)/)* ((RB|JJ)/)* (((JJ)/(CC|,)/)*(JJ)/)* ((NN)/)+"),
    (  "VP", r"(((MD|TO|RB)/)* ((VB)/)+ ((RP)/)*)+"),
    (  "VP", r"((MD)/)"),
    (  "PP", r"((IN|PP)/)+"),
    ("ADJP", r"((RB|JJ)/)* ((JJ)/,/)* ((JJ)/(CC)/)* ((JJ)/)+"),
    ("ADVP", r"((RB)/)+"),
], [
    # Romance languages: es, fr, it, ...
    (  "NP", r"((NN)/)* ((DT|CD|CC)/)* ((RB|JJ|,)/)* (((JJ)/(CC|,)/)*(JJ)/)* ((NN)/)+ ((RB|JJ)/)*"),
    (  "VP", r"(((MD|TO|RB)/)* ((VB)/)+ ((RP)/)* ((RB)/)*)+"),
    (  "VP", r"((MD)/)"),
    (  "PP", r"((IN|PP)/)+"),
    ("ADJP", r"((RB|JJ)/)* ((JJ)/,/)* ((JJ)/(CC)/)* ((JJ)/)+"),
    ("ADVP", r"((RB)/)+"),
]]

for i in (0, 1):
    for j, (tag, s) in enumerate(CHUNKS[i]):
        s = s.replace("NN", NN)
        s = s.replace("VB", VB)
        s = s.replace("JJ", JJ)
        s = s.replace("RB", RB)
        s = s.replace(" ", "")
        s = re.compile(s)
        CHUNKS[i][j] = (tag, s)

# Handle ADJP before VP, 
# so that RB prefers next ADJP over previous VP.
CHUNKS[0].insert(1, CHUNKS[0].pop(3))
CHUNKS[1].insert(1, CHUNKS[1].pop(3))

def find_chunks(tagged, language="en"):
    """ The input is a list of [token, tag]-items.
        The output is a list of [token, tag, chunk]-items:
        The/DT nice/JJ fish/NN is/VBZ dead/JJ ./. =>
        The/DT/B-NP nice/JJ/I-NP fish/NN/I-NP is/VBZ/B-VP dead/JJ/B-ADJP ././O
    """
    chunked = [x for x in tagged]
    tags = "".join("%s%s" % (tag, SEPARATOR) for token, tag in tagged)
    # Use Germanic or Romance chunking rules according to given language.
    for tag, rule in CHUNKS[int(language in ("ca", "es", "pt", "fr", "it", "pt", "ro"))]:
        for m in rule.finditer(tags):
            # Find the start of chunks inside the tags-string.
            # Number of preceding separators = number of preceding tokens.
            i = m.start()
            j = tags[:i].count(SEPARATOR)
            n = m.group(0).count(SEPARATOR)
            for k in range(j, j+n):
                if len(chunked[k]) == 3:
                    continue
                if len(chunked[k]) < 3:
                    # A conjunction or comma cannot be start of a chunk.
                    if k == j and chunked[k][1] in ("CC", "CJ", ","):
                        j += 1
                    # Mark first token in chunk with B-.
                    elif k == j:
                        chunked[k].append("B-" + tag)
                    # Mark other tokens in chunk with I-.
                    else:
                        chunked[k].append("I-" + tag)
    # Mark chinks (tokens outside of a chunk) with O-.
    for chink in filter(lambda x: len(x) < 3, chunked):
        chink.append("O")
    # Post-processing corrections.
    for i, (word, tag, chunk) in enumerate(chunked):
        if tag.startswith("RB") and chunk == "B-NP":
            # "Perhaps you" => ADVP + NP
            # "Really nice work" => NP
            # "Really, nice work" => ADVP + O + NP
            if i < len(chunked)-1 and not chunked[i+1][1].startswith("JJ"):
                chunked[i+0][2] = "B-ADVP"
                chunked[i+1][2] = "B-NP"
            if i < len(chunked)-1 and chunked[i+1][1] in ("CC", "CJ", ","):
                chunked[i+1][2] = "O"
            if i < len(chunked)-2 and chunked[i+1][2] == "O":
                chunked[i+2][2] = "B-NP"
    return chunked

def find_prepositions(chunked):
    """ The input is a list of [token, tag, chunk]-items.
        The output is a list of [token, tag, chunk, preposition]-items.
        PP-chunks followed by NP-chunks make up a PNP-chunk.
    """
    # Tokens that are not part of a preposition just get the O-tag.
    for ch in chunked:
        ch.append("O")
    for i, chunk in enumerate(chunked):
        if chunk[2].endswith("PP") and chunk[-1] == "O":
            # Find PP followed by other PP, NP with nouns and pronouns, VP with a gerund.
            if i < len(chunked)-1 and \
             (chunked[i+1][2].endswith(("NP", "PP")) or \
              chunked[i+1][1] in ("VBG", "VBN")):
                chunk[-1] = "B-PNP"
                pp = True
                for ch in chunked[i+1:]:
                    if not (ch[2].endswith(("NP", "PP")) or ch[1] in ("VBG", "VBN")):
                        break
                    if ch[2].endswith("PP") and pp:
                        ch[-1] = "I-PNP"
                    if not ch[2].endswith("PP"):
                        ch[-1] = "I-PNP"
                        pp = False
    return chunked

#--- SEMANTIC ROLE LABELER -------------------------------------------------------------------------
# Naive approach.

BE = dict.fromkeys(("be", "am", "are", "is", "being", "was", "were", "been"), True)
GO = dict.fromkeys(("go", "goes", "going", "went"), True)

def find_relations(chunked_words):
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







s1 = "Sometimes I can't see crows buzzing around the tree trunks in my iron-clad yellowed pajamas and boots." #" Don't' fish a fish."
s2 = "I look at the trees dancing."
s3 = "Python is a high-level programming language."
s4 = "What day of the week is December fifth"




a = TextBlobExtended(s1)
b = [[w.string, t] for w, t in a.pos_tags_with_punctuation]

print(b)
print()

b = find_chunks(b)
print(b)
print()

b = find_prepositions(b)
print(b)
print()

b = find_relations([w[0] for w in a.chunks])
print(b)
print()

print(repr(a.words[3]))

