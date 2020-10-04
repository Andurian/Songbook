#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import tempfile
import subprocess

from find_songs import find_songs

def run_pdflatex(texfile, auxdir, outname):
    pdflatexjob = [
        'pdflatex', 
        '-interaction=nonstopmode', 
        '-aux-directory={}'.format(auxdir), 
        '-jobname={}'.format(outname), 
        texfile
    ]
    subprocess.run(pdflatexjob)
    
def run_index(instrument, auxdir):
    indexjob = [
        'texlua', 
        'songidx.lua',
        '{}/{}_cbtitle.sxd'.format(auxdir, instrument), 
        '{}/{}_cbtitle.sbx'.format(auxdir, instrument)
    ]
    subprocess.run(indexjob)

filecontents = {}

songs = find_songs()
for key in songs:
    instrument = key.split('_')[-1]
    filecontents[instrument] = '\\begin{{filecontents}}{{{}}}\n{}\n\\end{{filecontents}}'.format(key + '.tex', songs[key])

with tempfile.TemporaryDirectory(dir='.') as auxdir:
    print(auxdir)
    for instrument in filecontents:
        filename = '{}/{}.tex'.format(auxdir, instrument)
        with open(filename, 'w+') as outfile:
            document = filecontents[instrument] + '\n\n\\input{{makesongbook}} \\makesongbook{{{}}}'.format(instrument)
            outfile.write(document)
        run_pdflatex(filename, auxdir, 'Songbook_' + instrument)
        run_pdflatex(filename, auxdir, 'Songbook_' + instrument)
        run_index(instrument, auxdir)
        run_pdflatex(filename, auxdir, 'Songbook_' + instrument)
        