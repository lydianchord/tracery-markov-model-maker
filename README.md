Usage: `python tracery_markov_model.py [-h] [-n SIZE] [-l] path/to/corpus/file`

Optional arguments:
* `-h`, `--help` &mdash; Show help message
*  `-n SIZE`, `--ngram SIZE` &mdash; Specify n-gram size (default: 3)
* `-l`, `--lowercase` &mdash; Convert all input to lowercase

The input corpus should be a text file containing statements separated by line breaks (preferably in English since it's the only language I've tested so far). The output JSON file will appear in a folder named `output`.
