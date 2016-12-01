import re

class Corpus:

    def __init__(self):
        self.tokens = list()
        self.sentences = list()
        self.turns = list()
        self.sessions = list()
        self.anaphors = list()
        self.antecedents = list()
        self.ref_instances = list()

    def get(self, annotation):
        # annotations stored as lists of ranges
        # ranges represent spans of sessions, turns, etc.
        output = list()
        for r in getattr(self, annotation):
            x = [self.tokens[t] for t in r]
            if x[0].lang == "de":
                output.append(x)
        return output

    def print(self, a_range):
        for i in a_range:
            if isinstance(i, int):
                tok = self.tokens[i]
            else:
                tok = i
            if tok.pos == "$.":
                print(tok.form)
            else:
                print(tok.form, end=" ")

    def daughters(self, token):
        x = token.index
        return [t for t in self.tokens[x-100:x+100]
                if t.mother == x]


class RefInstance:

    def __init__(self, _ana, *_ante):
        self.antecedents = _ante
        self.anaphor = _ana
        self.lang = self.anaphor[0].lang

        # calc dist
        self.distance = list()
        for ante in self.antecedents:
            if self.anaphor[-1].index < ante[0].index:
                self.distance.append(ante[0].index - self.anaphor[-1].index)
            else:
                self.distance.append(ante[-1].index - self.anaphor[0].index)

    def __repr__(self):
        anaphor = " ".join(x.form for x in self.anaphor.tokens)
        ante = [" ".join(x.form for x in y.tokens)
                for y in self.antecedents]
        return anaphor + " => " + repr(ante)

    def __str__(self):
        return "RefInstance({}, {}, {})".format(str(self.antecedents),
                                                str(self.anaphor),
                                                self.distance)


class Antecedent:

    def __init__(self, _toks, _nominal=False):
        self.tokens = _toks
        self.nominal = _nominal

    def __getitem__(self, index):
        return self.tokens[index]

    def __repr__(self):
        return str(self.__dict__)

    def __str__(self):
        return "Antecedent({}, {})".format(" ".join(str(x) for x in self.tokens),
                                           self.nominal)

    def get_text(self):
        return " ".join(x.form for x in self.tokens)


class Anaphor:

    def __init__(self, _toks, _value):
        self.tokens = _toks
        self.value = _value

    def __getitem__(self, index):
        return self.tokens[index]

    def __repr__(self):
        return str(self.__dict__)

    def __str__(self):
        return "Anaphor({}, {})".format(" ".join(str(x) for x in self.tokens),
                                        self.value)

    def get_text(self):
        return " ".join(x.form for x in self.tokens)


class Token:

    def __init__(self, wofo, attribs, index, lang, offset=0):
        self.form = wofo
        self.lang = lang
        self.index = index
        for key, val in attribs.items():
            if key == 'mate_pos':
                self.pos = val
            elif key == 'mate_morph':
                self.morph = val
            elif key == 'mate_lemma':
                self.lemma = val
            elif 'mother' in key:  # in some XML, these attrs have the wrong names
                try:
                    if val == "t_0":
                        self.mother = None
                    else:
                        # minus one because the tok_ids start at 1
                        self.mother = offset + int(re.search(r"(\d+)$", val).group(1)) - 1
                except AttributeError:
                    self.mother = val
            elif 'rel' in key:
                self.relation = val
            elif 'id' in key:
                self.id = val

    def __repr__(self):
        return str(self.__dict__)

    def __str__(self):
        return "Token({})".format(self.form)


