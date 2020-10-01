#!/usr/bin/env python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-
"""
    author: Ágnes Kalivoda, Noémi Vadász
    last update: 2020.01.07.

"""
from argparse import FileType

from xtsv import build_pipeline, parser_skeleton, jnius_config


def main():
    """
    - beolvassa a korpuszt
    - meghívja a dictionary-gyártó függvényt a termek beolvasásához
    - a dictionary-t és a korpuszt átadja a korpusz-feldolgozó függvénynek
    - kiírja a korpuszt
    """
    argparser = parser_skeleton(description='emTerm - a module for marking single word and multi-word units '
                                            'in POS-tagged text')
    argparser.add_argument('--term-list', dest='term_list', type=FileType(), required=True,
                           help='Specify the terminology dictionary file', metavar='FILE')
    argparser.add_argument('--counter-marker', dest='counter_marker', type=str, default=':',
                           help='Specify counter marker separator (default: :)')
    argparser.add_argument('--termid-separator', dest='termid_separator', type=str, default='×',
                           help='Specify termid separator (default: ×)')
    argparser.add_argument('--term-separator', dest='term_separator', type=str, default=';',
                           help='Specify term separator (default: ;)')
    argparser.add_argument('--list-mwe-separator', dest='list_mwe_separator', type=str, default='@',
                           help='Specify list mwe separator (default: @)')
    argparser.add_argument('--placeholder', dest='placeholder', type=str, default='_',
                           help='Specify placeholder for empty fields (default: _)')
    opts = argparser.parse_args()

    jnius_config.classpath_show_warning = opts.verbose  # Suppress warning.

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
    em_term = ('emterm', 'EmTerm', 'Mark single word and multi-word units in POS-tagged text',
               (opts.term_list, opts.counter_marker, opts.termid_separator, opts.term_separator,
                opts.list_mwe_separator, opts.placeholder), {'source_fields': {'form', 'lemma'},
                                                             'target_fields': ['term']})
    tools = [(em_term, ('term', 'emTerm'))]

    # Run the pipeline on input and write result to the output...
    output_iterator.writelines(build_pipeline(input_data, used_tools, tools, presets))

    # TODO this method is recommended when debugging the tool
    # Alternative: Run specific tool for input (still in emtsv format):
    # from xtsv import process
    # from emdummy import EmDummy
    # output_iterator.writelines(process(input_data, EmDummy(*em_dummy[3], **em_dummy[4])))

    # Alternative2: Run REST API debug server
    # from xtsv import pipeline_rest_api, singleton_store_factory
    # app = pipeline_rest_api('TEST', tools, {},  conll_comments=False, singleton_store=singleton_store_factory(),
    #                         form_title='TEST TITLE', doc_link='https://github.com/dlt-rilmta/emdummy')
    # app.run()


if __name__ == '__main__':
    main()
