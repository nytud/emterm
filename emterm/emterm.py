#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    author: Ágnes Kalivoda, Noémi Vadász
    last update: 2020.01.07.
    modified by Dávid Halász: 2020.09.01.

"""


from collections import defaultdict


class EmTerm:
    def __init__(self, termfile_path, counter_marker=':', termid_separator='×', term_separator=';',
                 list_mwe_separator='@', placeholder='_', source_fields=None, target_fields=None):
        self._counter_marker = counter_marker
        self._termid_separator = termid_separator
        self._term_separator = term_separator
        self._list_mwe_separator = list_mwe_separator
        self._placeholder = placeholder

        self._termdict, self._maxlen = self._get_termdict(termfile_path)

        # Field names for xtsv (the code below is mandatory for an xtsv module)
        if source_fields is None:
            source_fields = set()

        if target_fields is None:
            target_fields = []

        self.source_fields = source_fields
        self.target_fields = target_fields

    def _read_termdict(self, fr):
        """
        - soronként beolvassa a term-öket vagy descriptorokat tartalmazó fájlt
        - a sorokat kettévágja ID-ra és elnevezésre, a felesleges space-eket törli
        - ha az elnevezés még nem szerepel kulcsként a dictionary-ben, akkor létrehozza ezt a kulcsot egy üres listával
          FONTOS: azonos elnevezéshez több ID is tartozhat, ezért kell a lista!
        - a megfelelő kulcshoz hozzáadja az új ID-t
        """

        termdict = defaultdict(list)
        maxlen = 0
        for line in fr:
            uid, term = line.strip().split('\t', maxsplit=1)
            term = tuple(term.strip().lower().split(self._list_mwe_separator))
            termdict[term].append(uid.strip())
            maxlen = max(maxlen, len(term))

        return termdict, maxlen

    def _get_termdict(self, path):
        """
        Megnyitja a fájlt, vagy a megnyitott fájlt továbbítja beolvasásra
        """

        if isinstance(path, str):
            with open(path, encoding='UTF-8') as fr:
                termdict, maxlen = self._read_termdict(fr)
        else:
            termdict, maxlen = self._read_termdict(path)

        return termdict, maxlen

    @staticmethod
    def _canonical(ls, field_indices):
        """
        a token-szekvenciát olyan formájúra alakítja, hogy kereshető legyen a dictionary kulcsai között úgy, hogy:
        - végigmegy egyesével a szekvencia tokenjein
        - ha az utolsóhoz ér, annak a lemmáját őrzi meg
        - ha egyéb token van soron, annak a formját őrzi meg
        - az így létrejött szekvencia elemeit tuple-be rakja
        """

        canonized_ls = [item[field_indices[0]].lower() for item in ls[:-1]]  # Form
        canonized_ls.append(ls[-1][field_indices[1]].lower())  # Lemma

        return tuple(canonized_ls)

    def _add_annotation(self, act_sent, i, r, hit_counter, ctoken, annotation_col):
        """
        - beilleszti a részletes annotációt a találat első szavához (ha egyszavas a találat, akkor végzett is)
        - többszavas találat esetén a maradék szavaknál jelzi, hogy ezek hányadik találatnak a részei
        """

        act_sent[i][annotation_col] += f'{hit_counter}{self._counter_marker}' \
                                       f'{self._termid_separator.join(self._termdict[ctoken])}{self._term_separator}'
        for x, token in enumerate(act_sent[i+1:r], start=i+1):  # Ha i+1 == r, akkor nem többszavas -> nem csinál semmit
            act_sent[x][annotation_col] = f'{hit_counter}{self._term_separator}'

        return act_sent

    def process_sentence(self, act_sent, field_indices):
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

        annotation_col = -1  # Az új oszlop sorszáma
        for token in act_sent:  # Az új oszlop hozzáadása, hogy később már csak a tartalmát kelljen módosítani!
            token.append('')

        for i, token in enumerate(act_sent):
            for r in range(i+1, min(i+1+self._maxlen, all_tokens)):  # Fölülről korlátozza a mondat hossz!
                ctoken = self._canonical(act_sent[i:r], field_indices)
                if ctoken in self._termdict.keys():
                    act_sent = self._add_annotation(act_sent, i, r, hit_counter, ctoken, annotation_col)
                    hit_counter += 1

            act_sent[i][annotation_col] = act_sent[i][annotation_col].rstrip(self._term_separator)
            if act_sent[i][annotation_col] == '':
                act_sent[i][annotation_col] = self._placeholder  # Replace empty string with placeholder

        return act_sent

    @staticmethod
    def prepare_fields(field_names):
        return [field_names['form'], field_names['lemma']]
