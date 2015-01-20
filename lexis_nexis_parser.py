import re
import sys
import csv
import argparse

field_extractor = '{0}:\s*((?:.*\n)*?)(?:(?:[^a-z]*[A-Z][^a-z]*:)|$)'
doc_seperator = re.compile('(\d+) of (\d+) DOCUMENTS')
publication_date_re = re.compile(
    'Copyright(?:.+\n)(?:[^\S\r\n]*\S+.*\n)*[^\S\r\n]*(?:All Rights Reserved\s*)*(\S.*?)\n(?:.*\n)*?\s*(.+\d{4}.+)')
geographic_regex = re.compile(field_extractor.format('GEOGRAPHIC'))
geo_splitter = re.compile('(.*?)\s*\((\d+)%\);*\s*')


def match_and_group(regex, string):
    match = regex.search(string)
    if match:
        return match.groups()


class LexisNexisParser(object):
    """A data structure for processing Lexis Nexis output"""
    def __init__(self, args):
        self.document = ''
        self.first_doc = True
        self.num_geo = args.num_geo
        self.max_char = args.max_char
        self.filename = args.filename
        self.outfile_name = args.out_file or '.'.join(args.filename.split('.')[:-1] + ['_out.csv'])
        self.key_word_fields = args.fields or [
            'PUBLICATION-TYPE', 'HEADLINE', 'BODY'] + args.extra_fields
        titles = ["publication", "pub_date"] + self.key_word_fields
        geo_titles = [['geo {0}'.format(i), 'percent {0}'.format(i)] for i in xrange(
            1, args.num_geo + 1)]
        geo_titles = sum(geo_titles, [])        # Flattening list
        self.titles = titles + geo_titles
        self.regexes = [re.compile(field_extractor.format(word))
                   for word in self.key_word_fields]
        self.csv_writer = None

    def parse_document(self):
        data = list(
            match_and_group(publication_date_re, self.document) or ['', ''])

        for regex in self.regexes:
            data.append((match_and_group(regex, self.document) or [''])[0][:self.max_char])

        geographic = (match_and_group(geographic_regex, self.document) or [''])[0]
        geographic = [(loc, float(per))
                      for loc, per in geo_splitter.findall(geographic)]
        geographic = sorted(geographic, key=lambda x: -x[1])[:self.num_geo]
        geographic = list(sum(geographic, ()))

        return [i.strip() if type(i) == str else i for i in data + geographic]


    def process_line(self, line):
        doc_num = (doc_seperator.findall(line) or [None])[0]
        if not doc_num:
            self.document += line
        elif self.document.strip() and not self.first_doc:
            try:
                row = self.parse_document()
            except Exception, e:
                row = []
                print "------ error with self.document {0} ------".format(doc_num[0])
                print "Error: {0}".format(e)
            self.csv_writer.writerow(row)
            self.document = ''
            print 'parsing {0} of {1}'.format(*doc_num)
        else:
            self.first_doc = False
            print 'parsing {0} of {1}'.format(*doc_num)


    def parse_file(self):

        with open(self.filename) as read_file:
            with open(self.outfile_name, 'w') as write_file:
                self.csv_writer = csv.writer(write_file, quoting=csv.QUOTE_ALL)
                self.csv_writer.writerow(self.titles)
                for line in read_file:
                    self.process_line(line)
                self.csv_writer.writerow(self.parse_document())

if __name__ == '__main__':
    args_parser = argparse.ArgumentParser(
        description='Extract fields from a Lexisnexis file')
    args_parser.add_argument('filename', type=str, help='input file name')
    args_parser.add_argument(
        '--num-geo', type=int, default=5, help='maximum number of GEOGRAPHIC locations to keep')
    args_parser.add_argument(
        '-m', '--max-char', type=int, default=32766,
        help='maximum number of characters for a single cell')
    args_parser.add_argument(
        '-o', '--out-file', type=str, help='name of output file')
    # args_parser.add_mutually_exclusive_group()
    args_parser.add_argument('-e', '--extra-fields', type=str,
                             nargs='+', default=[], help='fields in addition to defaults')
    args_parser.add_argument(
        '--fields', '--fields', type=str, nargs='+', help='fields replacing defaults')
    args = args_parser.parse_args()
    

    print args.__dict__
    LexisNexisParser(args).parse_file()
