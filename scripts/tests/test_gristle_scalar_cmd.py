#!/usr/bin/env python
""" To do:
      1.  test with multiple input files

    See the file "LICENSE" for the full license governing this code. 
    Copyright 2011,2012,2013 Ken Farmer
"""

import sys
import os
import tempfile
import random
import time
import fileinput
import subprocess
import pytest


script_path = os.path.dirname(os.path.dirname(os.path.realpath((__file__))))
fq_pgm      = os.path.join(script_path, 'gristle_scalar')



def generate_test_file(delim, record_cnt):
    (fd, fqfn) = tempfile.mkstemp(prefix='TestScalarIn_')
    fp = os.fdopen(fd,"w")

    for i in range(record_cnt):
        fields = []
        fields.append(str(i))
        fields.append('A')
        fields.append('B')
        fields.append('C')
        fp.write(delim.join(fields)+'\n')

    fp.close()
    return fqfn



class TestCommandLine(object):

    def setup_method(self, method):

        self.easy_fqfn          = generate_test_file(delim='|', record_cnt=100)
        self.empty_fqfn         = generate_test_file(delim='|', record_cnt=0)
        (dummy, self.out_fqfn)  = tempfile.mkstemp(prefix='TestScalarOut_')

    def teardown_method(self, method):
        os.remove(self.easy_fqfn)
        os.remove(self.empty_fqfn)
        os.remove(self.out_fqfn)


    def test_easy_file(self):
        cmd = '%s %s -o %s -c 0 -t integer -a max' % (fq_pgm, self.easy_fqfn, self.out_fqfn)

        p = subprocess.Popen(cmd,
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE,
                             shell=True)
        p_output      = p.communicate()[0]
        stdout_recs   = p_output[:-1].split('\n')
        out_recs      = []
        for rec in fileinput.input(self.out_fqfn):
            out_recs.append(rec)
        fileinput.close()

        max_val, dummy = out_recs[0].split('\n')
        assert max_val == '99'
        assert len(out_recs) == 1



    def test_empty_file(self):
        cmd = '%s %s -o %s -c0 -t integer -a max' % (fq_pgm, self.empty_fqfn, self.out_fqfn)
        p =  subprocess.Popen(cmd,
                              stdin=subprocess.PIPE,
                              stdout=subprocess.PIPE,
                              shell=True)
        records =  p.communicate()[0]
        out_recs  = []
        assert len(out_recs) == 0


    def test_multiple_empty_files(self):
        cmd = "%s %s %s -o %s -c0 -t integer -a max -d'|'" % (fq_pgm, self.empty_fqfn, 
                                                              self.empty_fqfn, self.out_fqfn)
        p =  subprocess.Popen(cmd,
                              stdin=subprocess.PIPE,
                              stdout=subprocess.PIPE,
                              shell=True)
        records =  p.communicate()[0]
        out_recs  = []
        assert len(out_recs) == 0


    def test_multiple_full_files(self):
        cmd = "%s %s %s -o %s -c0 -t integer -a max -d'|'" % (fq_pgm, self.easy_fqfn, 
                                                              self.easy_fqfn, self.out_fqfn)
        p =  subprocess.Popen(cmd,
                              stdin=subprocess.PIPE,
                              stdout=subprocess.PIPE,
                              shell=True)
        records =  p.communicate()[0]
        out_recs  = []
        for rec in fileinput.input(self.out_fqfn):
            out_recs.append(rec)
        fileinput.close()

        assert len(out_recs) == 1
        max_val, dummy = out_recs[0].split('\n')
        assert max_val == '99'



    def test_empty_stdin_file(self):
        cmd = "cat %s | %s -o %s  -c 0 -t integer -a max -d'|'" % (self.empty_fqfn, 
                                                                   fq_pgm, self.out_fqfn)
        p =  subprocess.Popen(cmd,
                              stdin=subprocess.PIPE,
                              stdout=subprocess.PIPE,
                              shell=True)
        records =  p.communicate()[0]
        out_recs  = []
        for rec in fileinput.input(self.out_fqfn):
            out_recs.append(rec)
        fileinput.close()

        assert len(out_recs) == 0
        p.stdin.close()


