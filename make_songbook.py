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
        '-output-directory={}'.format(auxdir), 
        '-jobname={}'.format(outname), 
        texfile
    ]
    subprocess.run(pdflatexjob)
    
def run_index(auxdir):
    indexjob = [
        'texlua', 
        'songidx.lua',
        '{}/cbtitle.sxd'.format(auxdir), 
        '{}/cbtitle.sbx'.format(auxdir)
    ]
    subprocess.run(indexjob)

filecontents = {}

songs = find_songs()
for key in songs:
    instrument = key.split('_')[-1]
    filecontents[instrument] = '\\begin{{filecontents}}{{{}}}\n{}\n\\end{{filecontents}}'.format(key + '.tex', songs[key])

with tempfile.TemporaryDirectory(dir='.') as auxdir_raw:
    auxdir = auxdir_raw.split(os.sep)[-1]
    print(auxdir)
    for instrument in filecontents:
        filename = os.path.join(auxdir, '{}.tex'.format(instrument))
        with open(filename, 'w+') as outfile:
            document = filecontents[instrument] + '\n\n\\newcommand{{\\instrument}}{{{}}}\n\\newcommand{{\\builddir}}{{{}}}\n\\input{{Songbook}}'.format(instrument, auxdir)
            outfile.write(document)
        outname = 'Songbook_{}'.format(instrument)

        run_pdflatex(filename, auxdir, outname)
        run_pdflatex(filename, auxdir, outname)
        run_index(auxdir)
        run_pdflatex(filename, auxdir, outname)

        os.rename(os.path.join(auxdir, outname + '.pdf'), outname + '.pdf')
        
