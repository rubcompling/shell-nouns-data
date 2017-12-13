
import json
from pathlib import Path

def root(tok_seq):
    try:
        x = next(filter(lambda x: x.rel != "ROOT" and not x.pos.startswith("$"), 
                        tok_seq))
    except StopIteration:
        x = tok_seq[0]
    while x.rel != "ROOT" and x.mother in tok_seq:
        x = x.mother
    return x


def depth(tok):
    counter = 0
    x = tok
    while x.rel != "ROOT" and x.mother is not None:
        x = x.mother
        counter += 1
    return counter
    

def daughters(tok):
    return [x for x in tok.source if x.mother == tok]


def path(tok1, tok2):
    x = tok1.mother
    while x != tok2 and x is not None:
        x = x.mother
    return x == tok2


def tok_with_deps(tok, punct=False):
    deps = [x for x in tok.source if path(x, tok)]
    deps.append(tok)
    output = sorted(deps, key=lambda x: x.index)
    if punct:
        try:
            next_token = tok.source[output[-1].index + 1]
            if next_token.pos == "$.":
                output.append(next_token)
        except IndexError:
            pass
    return output


class Doc:

    def __init__(self, input):
        if isinstance(input, str):
            with open(input) as infile:
                jsondict = json.load(infile)
        elif isinstance(input, Path):
            with input.open("r") as infile:
                jsondict = json.load(infile)
        elif isinstance(input, dict):
            jsondict = input
        else:
            jsondict = None

        # required contents
        self.name = jsondict["name"]

        self._tokens = [Token(tokdict) for tokdict in jsondict["tokens"]]

        self.sentences = [self._tokens[start:end] 
                            for start, end in jsondict["sentences"]]

        self.lang = jsondict.get("lang", "")

        # (fix references)
        offset = int(self._tokens[0].index)
        for tok in self._tokens:
            tok.source = self
            tok.index = int(tok.index) - offset
            if tok.mother is not None:
                tok.mother = self._tokens[int(tok.mother) - offset]

        # other annotations (span-based)
        if "antecedents" in jsondict:
            self.antecedents = [self._tokens[ante["start"]:ante["end"]] 
                                for ante in jsondict["antecedents"]]
        if "anaphors" in jsondict:
            self.anaphors = [self._tokens[ana["start"]:ana["end"]] 
                             for ana in jsondict["anaphors"]]
        if "ref_instances" in jsondict:
            self.ref_instances = [(self.anaphors[inst["anaphor"]], 
                                   self.antecedents[inst["antecedent"]])
                                  for inst in jsondict["ref_instances"]]

    def __iter__(self):
        return iter(self._tokens)

    def __len__(self):
        return len(self._tokens)

    def __getitem__(self, index):
        return self._tokens[index]

    def __repr__(self):
        return "\n".join(" ".join(tok.text for tok in sent) 
                         for sent in self.sentences)

    def to_dict(self):
        def span2inds(z):
            return (z[0].index, z[-1].index + 1)

        outdict = dict()
        outdict["name"] = self.name
        outdict["tokens"] = [tok.to_dict() for tok in self._tokens]
        outdict["sentences"] = [span2inds(x) for x in self.sentences]
        
        if hasattr(self, "ref_instances"):
            outdict["antecedents"] = [span2inds(x) for x in self.antecedents]
            outdict["anaphors"] = [span2inds(x) for x in self.anaphors]
            outdict["ref_instances"] = [(span2inds(x), span2inds(y))
                                        for x, y in self.ref_instances]
        if hasattr(self, "sn_pos"):
            outdict["sn_pos"] = [x.index for x in self.sn_pos]
            outdict["sn_neg"] = [x.index for x in self.sn_neg]

        return outdict


class Token:

    def __init__(self, attrib):
        self.__dict__ = attrib

    def __str__(self):
        return self.text

    def __repr__(self):
        return self.text

    def to_dict(self):
        outdict = self.__dict__
        del outdict["source"]
        if outdict["mother"] is not None:
            outdict["mother"] = outdict["mother"].index
        return outdict

    def get_sentence(self, offset=0):
        """Get either sentence containing `atoken` (+/- offset) or None."""
        for no, sent in enumerate(self.source.sentences):
            if self in sent:
                return self.source.sentences[no + offset]
        return None

    def neighbor(self, offset=1):
        return self.source[self.index + offset]