#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    author: Ágnes Kalivoda, Noémi Vadász
    last update: 2020.01.07.

"""
from argparse import FileType

from xtsv.xtsv import build_pipeline, parser_skeleton


def main():
    """
    - beolvassa a korpuszt
    - meghívja a dictionary-gyártó függvényt a termek beolvasásához
    - a dictionary-t és a korpuszt átadja a korpusz-feldolgozó függvénynek
    - kiírja a korpuszt
    """
    argparser = parser_skeleton(description='emTerm -- multiword terminology expressions marker')
    argparser.add_argument('--term-list', dest='term_list', type=FileType(), required=True,
                           help='Specify the terminology dictionary file', metavar='FILE')
    opts = argparser.parse_args()

    # Set input and output iterators...
    if opts.input_text is not None:
        input_data = opts.input_text
    else:
        input_data = opts.input_stream
    output_iterator = opts.output_stream

    # Set the tagger name as in the tools dictionary
    used_tools = ['term']
    presets = []

    # Init and run the module as it were in xtsv

    # The relevant part of config.py
    em_term = ('emterm', 'EmTerm', 'Mark multiword terminology expressions from fixed list',
               (opts.term_list,), {'source_fields': {'form', 'lemma'}, 'target_fields': ['term']})
    tools = [(em_term, ('term', 'emTerm'))]

    # Run the pipeline on input and write result to the output...
    output_iterator.writelines(build_pipeline(input_data, used_tools, tools, presets))

    # TODO this method is recommended when debugging the tool
    # Alternative: Run specific tool for input (still in emtsv format):
    # output_iterator.writelines(process(input_iterator, inited_tools[used_tools[0]]))

    # Alternative2: Run REST API debug server
    # app = pipeline_rest_api('TEST', inited_tools, presets,  False)
    # app.run()


if __name__ == '__main__':
    main()
