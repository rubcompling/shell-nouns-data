#!/usr/bin/env python3

import os
import argparse
import pickle
from lxml import etree
from sys import argv

from objects import *

## returns a list of ints 
def to_index(s):
    outlist = list()
    spl1 = s.split(',')
    try:
        for item in spl1:
            spl2 = item.split('..')
            start = int(spl2[0].split('_')[1])
            end = int(spl2[1].split('_')[1]) if len(spl2) > 1 else start
            outlist.extend([i - 1 for i in range(start, end + 1)])
    except ValueError:
        print(s)
    return outlist


def get_SNs(node):
    snes = list()
    try:
        for sn in node.find("shellnouns").iter("shellnoun"):
            snes.append((sn.get("content_phrases"),
                         to_index(sn.get("span")),
                         sn.get("value")))
    except AttributeError:
        pass
    return snes


if __name__ == '__main__':

    ap = argparse.ArgumentParser()
    ap.add_argument("inputfiles", type=str, nargs='+',
                    help="xml input files")
    ap.add_argument("-o", "--outputfile", type=str, default="sn_data.pickle",
                    help="name of output pickle")
    ap.add_argument("-a", "--annotated", action="store_true",
                    help="use if xml files are annotated w/SN info")
    userargs = ap.parse_args()

    i = 0
    corpus = Corpus()
    for fname in userargs.inputfiles:
        docroot = etree.parse(fname).getroot()
        myname, ext = os.path.splitext(fname)

        print("processing", myname + "...")
        session_start = i
        for turn in docroot.iter("turn"):
            turn_start = i
            mylang = "de" if "de" in turn.get("turn_id") else "en"

            for sentence in turn.iter("sent"):
                sent_start = i
                for tok in sentence.iter("tok"):
                    corpus.tokens.append(Token(tok.text, tok.attrib, i,
                                               mylang, session_start))
                    i += 1
                sent_end = i
                corpus.sentences.append(range(sent_start, sent_end))
            turn_end = i
            corpus.turns.append(range(turn_start, turn_end))
        session_end = i
        corpus.sessions.append(range(session_start, session_end))

        if userargs.annotated:
            
            # dict: CP id -> Antecedent
            cps = dict()
            for cp in docroot.find("content_phrases").iter("content_phrase"):
                cp_indices = to_index(cp.get("span"))
                is_nom = cp.get("nominal")
                new_ante = Antecedent([corpus.tokens[x + session_start] 
                                       for x in cp_indices],
                                      is_nom)
                corpus.antecedents.append(new_ante)
                cps[cp.get("id")] = new_ante                

            # list[tuples]           "proto-Anaphor"
            snes = get_SNs(docroot)

            for cp_key, sn_indices, val in snes:

                my_anaphor = Anaphor([corpus.tokens[x + session_start]
                                      for x in sn_indices],
                                     val)
                corpus.anaphors.append(my_anaphor)

                my_antecedents = list()
                for key in cp_key.split(";"):
                    try:
                        my_antecedents.append(cps[key])
                    except KeyError:
                        pass
                        
                my_instance = RefInstance(my_anaphor, *my_antecedents)

                # only keep (non-empty) entries
                if my_instance.antecedents:
                    corpus.ref_instances.append(my_instance)

    with open(userargs.outputfile, 'wb') as outfile:
        print("read corpus with", len(corpus.tokens), "tokens...")
        pickle.dump(corpus, outfile)

    print("done!")
