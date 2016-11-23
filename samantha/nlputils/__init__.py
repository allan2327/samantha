        
def search_token(tokens, lemma=None, pos=None, recursive=False):
    # this is depth first
    # TODO implement recursive
    def is_match(token):
        result = True
        if lemma:
            result = result and token.lemma_ == lemma
        if pos:
            result = result and token.pos_ == pos
        return result

    results = []
    for token in tokens:
        if is_match(token):
            results.append(token)
    return results
