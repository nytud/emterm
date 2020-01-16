# __emTerm__ - a module for marking single word and multi-word units in POS-tagged text

__emTerm__ is an experimental module of the [e-magyar text processing system (__emtsv__)](https://github.com/dlt-rilmta/emtsv). It can be used to find and mark single word or multi-word expressions (e.g. legal terms) in POS-tagged text. It can also be used independently of __emtsv__ by means of the [__xtsv__ framework](https://github.com/dlt-rilmta/xtsv).

## Usage

1. __emTerm__ works with two input files:
	- A POS-tagged text in xtsv format (a tsv file with headers, see `test_input.xtsv`).
	- A simple predefined list of terms (see `test_termlist.tsv`). The list consists of two columns separated by tab characters: The first column contains the identifiers of the terms and the second contains the terms themselves. In the case of multi-word expressions, white spaces must be substituted for @ characters.

2. There are two ways to run __emTerm__:
	- 1st: As a part of the __emtsv__ pipeline (see the [emtsv documentation](https://github.com/dlt-rilmta/emtsv) for usage scenarios).
	- 2nd: As a single tool, using the [__xtsv__ framework](https://github.com/dlt-rilmta/xtsv). Below you can find four different ways of using __emTerm__ in the command line, independently of __emtsv__:

```bash
    cat test_input.xtsv | python3 main.py --term-list test_termlist.tsv
    cat test_input.xtsv | python3 main.py --term-list test_termlist.tsv -o test_output.xtsv
    python3 main.py --term-list test_termlist.tsv -i test_input.xtsv
    python3 main.py --term-list test_termlist.tsv -i test_input.xtsv -o test_output.xtsv
```

3. The output of __emTerm__ keeps the xtsv format by adding a new column (`term`) to the end of the original, POS-tagged text. The annotation format used in this column is `serial_number_of_the_hit:identifier`. The numbering of hits starts with 1 by every new sentence. In the case of multi-word expressions, the whole annotation can be seen by the starting word, while the expression's further words get the same serial number as the first one but the identifier is not present. If a token can be found in several expressions, all of its hits are shown separated by semicolons (;).

## Citing and License

__emTerm__ is licensed under the GPL 3.0 license.

We are currently working on a paper which should be cited when __emTerm__ is used.
