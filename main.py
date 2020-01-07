#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    author: Ágnes Kalivoda, Noémi Vadász
    last update: 2020.01.07.

"""

import csv
import re
import sys
from collections import namedtuple
import argparse


def get_termdict(path):
    """
    - soronként beolvassa a term-öket vagy descriptorokat tartalmazó fájlt
    - a sorokat kettévágja ID-ra és elnevezésre, a felesleges space-eket törli
    - ha az elnevezés még nem szerepel kulcsként a dictionary-ben, akkor létrehozza ezt a kulcsot egy üres listával
      FONTOS: azonos elnevezéshez több ID is tartozhat, ezért kell a lista!
    - a megfelelő kulcshoz hozzáadja az új ID-t
    """

    termdict = {}
    maxlen = 0

    with open(path, encoding='utf-8') as fr:
        for line in fr:
            uid, term = line.strip().split('\t')
            uid = re.sub(r'\s+', '', uid)
            term = re.sub(r'\s+', '', term)
            if term not in termdict.keys():
                termdict[term] = []
            termdict[term].append(uid)
            actlen = len(term.split('@'))
            if maxlen < actlen:
                maxlen = actlen

    return termdict, maxlen


def canonical(ls):
    """
    a token-szekvenciát olyan formájúra alakítja, hogy kereshető legyen a dictionary kulcsai között úgy, hogy:
    - végigmegy egyesével a szekvencia tokenjein
    - ha az utolsóhoz ér, annak a lemmáját őrzi meg
    - ha egyéb token van soron, annak a formját őrzi meg
    - az így létrejött szekvencia elemeit @-cal köti össze
    """

    canonized_ls = []
    for i, item in enumerate(ls):
        if i == len(ls)-1:
            canonized_ls.append(item[0].lemma)
        else:
            canonized_ls.append(item[0].form)

    return '@'.join(canonized_ls)


def add_annotation(act_sent, i, r, hit_counter, ctoken, termdict):
    """
    - beilleszti a részletes annotációt a találat első szavához (ha egyszavas a találat, akkor végzett is)
    - többszavas találat esetén a maradék szavaknál jelzi, hogy ezek hányadik találatnak a részei
    """
    # TODO a × helyére mi kell? ez nem új találat, egyszerűen több ID tartozik ugyanahhoz a term-höz
    act_sent[i][1] += '{}:{};'.format(hit_counter, '×'.join(termdict[ctoken]))
    if '@' in ctoken:
        for x, token in enumerate(act_sent):
            if i < x < r:
                act_sent[x][1] = '{};'.format(hit_counter)

    return act_sent


def annotate_sent(act_sent, termdict, maxlen):
    """
    - a találat-számlálót 1-re állítja minden új mondat esetén
    - végigmegy a mondat tokenjein:
        - az aktuális tokentől kezdve végigveszi az összes token-szekvenciát, a mondat végével bezárólag, pl.
          'süt a nap' -> 'süt', 'süt a', 'süt a nap'; 'a', 'a nap'; 'nap'
        - minden token-szekvenciát átad egy függvénynek, ami a dictionary-nek megfelelő formátumban hozza ezeket
        - ha az átalakított szekvencia megtalálható a dictionary kulcsai között:
            - meghív egy függvényt, ami a pontos annotációt beilleszti a megfelelő oszlopba
            - növeli eggyel a találat-számlálót
    - végül elvégez pár formai igazítást az utolsó oszlopon
    """

    hit_counter = 1
    all_tokens = len(act_sent)

    for i, token in enumerate(act_sent):
        for r in range(i+1, min(maxlen+i, all_tokens+1)+1):
            ctoken = canonical(act_sent[i:r])
            if ctoken in termdict.keys():
                act_sent = add_annotation(act_sent, i, r, hit_counter, ctoken, termdict)
                hit_counter += 1

        act_sent[i][1] = act_sent[i][1].rstrip(';')

    return act_sent


def main():
    """
    - beolvassa a korpuszt
    - meghívja a dictionary-gyártó függvényt a termek beolvasásához
    - a dictionary-t és a korpuszt átadja a korpusz-feldolgozó függvénynek
    - kiírja a korpuszt
    """

    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--termlist", required=True, type=str, help="Add termlist!")
    args = parser.parse_args()

    term_dict, maxlen = get_termdict(args.termlist)

    reader = csv.reader(iter(sys.stdin.readline, ''), delimiter='\t', quoting=csv.QUOTE_NONE)
    header = next(reader)
    Line = namedtuple("Line", header)
    header.append("term")

    sent = list()

    print('\t'.join(header))
    for line in reader:
        if line:
            sent.append([Line._make(line), ''])
        else:
            sent = annotate_sent(sent, term_dict, maxlen)
            for token in sent:
                print('\t'.join([field for field in token[0]]), '\t', token[1])
            sent = list()
            print('')

    if sent:
        sent = annotate_sent(sent, term_dict, maxlen)
        for token in sent:
            print('\t'.join([field for field in token[0]]), '\t', token[1])


if __name__ == "__main__":
    main()
