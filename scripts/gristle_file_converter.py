#!/usr/bin/env python
""" Converts file csv dialect - field delimiter and record delimiter.
    Also can be used to convert between multi-columna and single-column
    field delimiters.

    The input file is specified on the command line and the output is
    written to stdout.

    See the file "LICENSE" for the full license governing this code. 
    Copyright 2011 Ken Farmer
"""

#--- standard modules ------------------
import sys
import os
import optparse
import csv
import fileinput
#import pprint as pp

#--- gristle modules -------------------
sys.path.append('../')     # allows running out of project structure
sys.path.append('../../')  # allows running tests out of project structure

import gristle.file_type           as file_type 

#from pprint import pprint as pp
#pp(sys.path)


#------------------------------------------------------------------------------
# Command-line section 
#------------------------------------------------------------------------------
def main():
    """ Analyzes the file to automatically determine input file csv 
        characteristics.  Then reads one record at a time and writes it
        out.

        Note that it doesn't yet use the csv module (or an extended version)
        for multi-column delimited-files and doesn't use the csv module
        for writing the records.
    """
    (opts, dummy) = get_opts_and_args()

    if opts.filename:
        my_file       = file_type.FileTyper(opts.filename, 
                                           opts.delimiter,
                                           opts.recdelimiter,
                                           opts.hasheader)
        my_file.analyze_file()
        dialect       = my_file.dialect
    else:
        # dialect parameters needed for stdin - since the normal code can't
        # analyze this data.
        dialect                = csv.Dialect
        dialect.delimiter      = opts.delimiter
        dialect.quoting        = opts.quoting
        dialect.quotechar      = opts.quotechar
        dialect.lineterminator = '\n'                 # naive assumption

    if opts.filename:
        infile  = open(opts.filename, 'r')
    else:
        infile  = sys.stdin
    if opts.output:
        outfile  = open(opts.output, 'w')
    else:
        outfile  = sys.stdout

    rec_cnt = -1
    if (not dialect.delimiter
    or len(dialect.delimiter) == 1):
        for fields in csv.reader(infile, dialect):
            rec_cnt += 1
            #if my_file.has_header and rec_cnt == 0:   # need to review what to do with this
            #    continue
            write_fields(fields, opts.out_delimiter, 
                         opts.out_recdelimiter, outfile)        # replace my_file with what?
    else:
        # csv module can't handle multi-column delimiters:
        while true:
            rec = infile.read()
            if not rec:
                break
            else:
                rec_cnt += 1
            if opts.recdelimiter:
                clean_rec = rec[:-1].split(opts.recdelimiter)[0]
            else:
                clean_rec = rec[:-1]
            fields = clean_rec.split(dialect.delimiter)
            #if my_file.has_header and rec_cnt == 0:              # replace my_file with what?
            #    continue
            write_fields(fields, opts.out_delimiter, 
                         opts.out_recdelimiter, outfile)         # replace my_file with what?

    if opts.filename:
        infile.close()
    if opts.output:
        outfile.close()

    return 0     


def write_fields(fields, out_delimiter, out_rec_delimiter, outfile):
    """ Writes output to output destination.
        Input:
            - list of fields to write
            - output object
        Output:
            - delimited output record written 
    """
    if out_rec_delimiter is None:
        rec = out_delimiter.join(fields)
    else:
        rec = "%s%s" % (out_delimiter.join(fields), out_rec_delimiter)
    outfile.write('%s\n'% rec)


def get_opts_and_args():
    """ gets opts & args and returns them
        Input:
            - command line args & options
        Output:
            - opts dictionary
            - args dictionary 
    """
    
    use = ("%prog converts files between different CSV file formats. \n"
           "\n"
           "   %prog -f [file] [misc options]"
           "\n")

    parser = optparse.OptionParser(usage = use)

    parser.add_option('-f', '--file', 
           dest='filename', 
           help='Specifies input file. Default is stdin.')
    parser.add_option('-o', '--output', 
           help='Specifies output file. Default is stdout.')
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
    parser.add_option('-d', '--delimiter',
           help=('Specify a quoted field delimiter.'
                 'This is especially useful for multi-col delimiters.'))
    parser.add_option('-D', '--outdelimiter',
           dest='out_delimiter',
           help=('Specify a quoted field delimiter'
                 'This is especially useful for multi-col delimiters.'))
    parser.add_option('-r', '--recdelimiter',
           help='Specify a quoted end-of-record delimiter. ')
    parser.add_option('-R', '--outrecdelimiter',
           dest='out_recdelimiter',
           help='Specify a quoted end-of-record delimiter. ')
    parser.add_option('--quoting',
           default=False,
           help='Specify field quoting - generally only used for stdin data.'
                '  The default is False.')
    parser.add_option('--quotechar',
           default='"',
           help='Specify field quoting character - generally only used for '
                'stdin data.  Default is double-quote')
    parser.add_option('--hasheader',
           default=False,
           action='store_true',
           help='Indicates the existance of a header in the file.')
    parser.add_option('-H', '--outhasheader',
           default=False,
           action='store_true',
           dest='out_hasheader',
           help='Specify that a header within the input file will be retained')

    (opts, args) = parser.parse_args()

    # validate opts
    if opts.filename:
        if not os.path.exists(opts.filename):
            parser.error("filename %s could not be accessed" % opts.filename)

    return opts, args



if __name__ == '__main__':
    sys.exit(main())
