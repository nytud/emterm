#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    author: Ágnes Kalivoda, Noémi Vadász
    last update: 2020.01.07.

"""

from xtsv import build_pipeline


def main():
    """
    - beolvassa a korpuszt
    - meghívja a dictionary-gyártó függvényt a termek beolvasásához
    - a dictionary-t és a korpuszt átadja a korpusz-feldolgozó függvénynek
    - kiírja a korpuszt
    """

    # Set input and output iterators...
    input_iterator = open('teszt.xtsv', encoding='UTF-8')  # Or sys.stdin
    output_iterator = open('teszt.out', 'w', encoding='UTF-8')  # Or sys.stdout

    # Set the tagger name as in the tools dictionary
    used_tools = ['term']
    presets = []

    # Init and run the module as it were in xtsv

    # The relevant part of config.py
    em_term = ('emterm', 'EmTerm', 'Mark multiword terminology expressions from fixed list',
               ('termlist.tsv',), {'source_fields': {'form', 'lemma'}, 'target_fields': ['term']})
    tools = [(em_term, ('term', 'emTerm'))]

    # Run the pipeline on input and write result to the output...
    output_iterator.writelines(build_pipeline(input_iterator, used_tools, tools, presets))

    # TODO this method is recommended when debugging the tool
    # Alternative: Run specific tool for input (still in emtsv format):
    # output_iterator.writelines(process(input_iterator, inited_tools[used_tools[0]]))

    # Alternative2: Run REST API debug server
    # app = pipeline_rest_api('TEST', inited_tools, presets,  False)
    # app.run()


if __name__ == '__main__':
    main()
