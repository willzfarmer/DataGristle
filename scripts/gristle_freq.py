#!/usr/bin/env python
""" Creates a frequency distribution of values from a single column of the
    input file and prints this out in descending order.
   
    See the file "LICENSE" for the full license governing this code. 
    Copyright 2011 Ken Farmer

    To do:
    - add stdin & directed output
    - add consistent value width
   
"""

#--- standard modules ------------------
import sys
import os
import optparse
import csv
import collections
import operator

#--- gristle modules -------------------
sys.path.append('../')  # allows running out of project structure
sys.path.append('../../')  # allows running out of project structure

import gristle.file_type           as file_type 


#from pprint import pprint as pp
#pp(sys.path)


def main():
    """ Runs analyzer to automatically determine file format
        Then accumulates the frequency distribution for the requested column
        Then sorts the distribution by value
        Then prints it
    """
    field_freq = collections.defaultdict(int)

    (opts, dummy) = get_opts_and_args()
    if opts.filename:
        my_file       = file_type.FileTyper(opts.filename, 
                                            opts.delimiter,
                                            opts.recdelimiter,
                                            opts.hasheader)
        my_file.analyze_file()
        dialect                = my_file.dialect
    else:
        # dialect parameters needed for stdin - since the normal code can't
        # analyze this data.
        dialect                = csv.Dialect
        dialect.delimiter      = opts.delimiter
        dialect.quoting        = opts.quoting
        dialect.quotechar      = opts.quotechar
        dialect.lineterminator = '\n'                 # naive assumption

    if opts.filename:
        infile = open(opts.filename, 'r')
    else:
        infile = sys.stdin

    for fields in csv.reader(infile, dialect):
        try:
            field_freq[fields[opts.column_number]] += 1
        except IndexError:
            continue   # skip short, bad, record
        if len(field_freq) > 50000:
            print 'Number of unique values exceeds limits - will truncate'
            break
    infile.close()

    sort_freq = sorted(field_freq.iteritems(), 
                       key=operator.itemgetter(1),
                       reverse=True)

    write_freq(sort_freq, opts.output)

    return 0     


def write_freq(freq_list, outfile_name):
    """ Writes output to output destination.
        Input:
            - frequency distribution
        Output:
            - delimited output record written to stdout
        To Do:
            - write to output file
    """
    key   = 0
    value = 1

    # figure out label length for formatting:
    max_v_len = 0
    for freq_tup in freq_list:
        if len(freq_tup[key]) > max_v_len:
            max_v_len = len(freq_tup[key])
    if max_v_len > 50:                     # chose 50 byte max width arbitrarily
        min_format_len = 54
    else:
        min_format_len  =  max_v_len + 4

    if outfile_name:
        outfile = open(outfile_name, 'w')
    else:
        outfile = sys.stdout

    for freq_tup in freq_list:
        outfile.write('%-*s    -    %d\n' % (min_format_len, freq_tup[key], freq_tup[value]))

    # don't close stdout
    if outfile_name:
        outfile.close()


def get_opts_and_args():
    """ gets opts & args and returns them
        Input:
            - command line args & options
        Output:
            - opts dictionary
            - args dictionary 
    """
    use = ("%prog is used to print a frequency distribution of a single column"
           " from the input file: \n"
           "\n"
           "   %prog -f [file] [misc options] "
           "\n")
    parser = optparse.OptionParser(usage = use)

    parser.add_option('-f', '--file',
           dest='filename',
           help='Specifies the input file, defaults to stdin.')
    parser.add_option('-o', '--output',
           help='Specifies the output file, defaults to stdout.')
    parser.add_option('-q', '--quiet',
           action='store_false',
           dest='verbose',
           default=True,
           help='provides less detail')
    parser.add_option('-v', '--verbose',
           action='store_true',
           dest='verbose',
           default=True,
           help='provides more detail')
    parser.add_option('-c', '--column',
           type=int,
           dest='column_number',
           help='column number to analyze')
    parser.add_option('-d', '--delimiter',
           help=('Specify a quoted single-column field delimiter. This may be'
                 'determined automatically by the program - unless you pipe the'
                 'data in.'))
    parser.add_option('--quoting',
           default=False,
           help='Specify field quoting - generally only used for stdin data.'
                '  The default is False.')
    parser.add_option('--quotechar',
           default='"',
           help='Specify field quoting character - generally only used for '
                'stdin data.  Default is double-quote')
    parser.add_option('--recdelimiter',
           help='Specify quoted end-of-record delimiter.')
    parser.add_option('--hasheader',
           default=False,
           action='store_true',
           help='indicates that there is a header in the file.')

    (opts, args) = parser.parse_args()

    # validate opts
    if opts.filename:
        if not os.path.exists(opts.filename):
            parser.error("filename %s could not be accessed" % opts.filename)
    else:
        if not opts.delimiter:
            parser.error('Please provide delimiter when piping data into program via stdin')

    return opts, args



if __name__ == '__main__':
    sys.exit(main())
