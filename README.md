lexis-nexis-parser
==================

Extract metadata from Lexis Nexis Output

Basic Usage:
```
$ python lexis_nexis_parser.py file.txt
```

This will process the input file and extract the following fields: 
  - publication
  - pub_date
  - PUBLICATION-TYPE
  - HEADLINE
  - BODY
  - up to 5 GEOGRAPHIC locations

Advanced Usage:
```
python lexis_nexis_parser.py file.txt --num-geo=6 -o data.csv -e CITY -m 1000
```

This parses the same file but extract an extra field (CITY), it also extracts up to 6 geo locations and has a maxumum number of characters per excel cell of 1000. Also the advanced version saves the output to data.csv instead of {filename}_out.csv


```
$ python lexis_nexis_parser.py --help

usage: lexis_nexis_parser.py [-h] [--num-geo NUM_GEO] [-m MAX_CHAR]
                             [-o OUT_FILE]
                             [-e EXTRA_FIELDS [EXTRA_FIELDS ...]]
                             [--fields FIELDS [FIELDS ...]]
                             filename

Extract fields from a Lexisnexis file

positional arguments:
  filename              input file name

optional arguments:
  -h, --help            show this help message and exit
  --num-geo NUM_GEO     maximum number of GEOGRAPHIC locations to keep
  -m MAX_CHAR, --max-char MAX_CHAR
                        maximum number of characters for a single cell
  -o OUT_FILE, --out-file OUT_FILE
                        name of output file
  -e EXTRA_FIELDS [EXTRA_FIELDS ...], --extra-fields EXTRA_FIELDS [EXTRA_FIELDS ...]
                        fields in addition to defaults
  --fields FIELDS [FIELDS ...], --fields FIELDS [FIELDS ...]
                        fields replacing defaults
  ```
