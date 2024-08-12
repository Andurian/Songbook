#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import os
import posixpath
import tempfile
import subprocess
import contextlib

from find_songs import find_songs

# Use / as pathseparator on windows when using texlive
join = posixpath.join

def run_pdflatex(texfile, auxdir, outname):
    pdflatexjob = [
        'pdflatex', 
        '-interaction=nonstopmode', 
        '-output-directory={}'.format(auxdir), 
        '-jobname={}'.format(outname), 
        texfile
    ]
    subprocess.run(pdflatexjob)

def run_lualatex(texfile, auxdir, outname):
    lulatexjob = [
        'lualatex', 
        '-shell-escape',
        '-interaction=nonstopmode', 
        '-output-directory={}'.format(auxdir), 
        '-jobname={}'.format(outname), 
        texfile
    ]
    subprocess.run(lulatexjob)
    
def run_index(auxdir):
    indexjob = [
        'texlua', 
        'songidx.lua',
        '{}/cbtitle.sxd'.format(auxdir), 
        '{}/cbtitle.sbx'.format(auxdir)
    ]
    subprocess.run(indexjob)

def make_filecontents():
    filecontents = {}

    songs = find_songs()
    for key in songs:
        instrument = key.split('_')[-1]
        filecontents[instrument] = '\\begin{{filecontents}}{{{}}}\n{}\n\\end{{filecontents}}'.format(key + '.tex', songs[key])
    
    return filecontents

class SongbookBuilder():

    def __init__(self, auxdir):
        self.filecontents = make_filecontents()

        if auxdir is None: 
            self.tempdir = tempfile.TemporaryDirectory(dir='.')
            self.auxdir = self.tempdir.split(os.sep)[-1]
        else:
            self.tempdir = None
            self.auxdir = auxdir
            if not os.path.exists(self.auxdir):
                os.makedirs(self.auxdir)


    def __del__(self):
        if self.tempdir is not None:
            self.tempdir.cleanup()

    def build_instrument(self, instrument, force_fullbuild):
        auxdir = self.auxdir

        filename = join(auxdir, '{}.tex'.format(instrument))
        outname = 'Songbook_{}'.format(instrument)
        outname_pdf = outname + ".pdf"
        outname_full = join(auxdir, outname_pdf)
        
        fullbuild = not os.path.exists(outname_full) or force_fullbuild

        with open(filename, 'w+') as outfile:
            document = self.filecontents[instrument] + '\n\n\\newcommand{{\\instrument}}{{{}}}\n\\newcommand{{\\builddir}}{{{}}}\n\\input{{Songbook}}'.format(instrument, auxdir)
            outfile.write(document)
            print(document)
        
        run_lualatex(filename, auxdir, outname)
        if fullbuild:
            run_lualatex(filename, auxdir, outname)
            run_index(auxdir)
            run_lualatex(filename, auxdir, outname)

        if self.tempdir is not None:
            os.rename(outname_full, outname_pdf)

    def build_all(self, force_fullbuild):
        for instrument in self.filecontents:
            self.build_instrument(instrument, force_fullbuild)



parser = argparse.ArgumentParser()

parser.add_argument("-d", "--dir", help="Use an existing build directory")
parser.add_argument("-i", "--instrument", help="Build Songbook only for a specific instrument")
parser.add_argument("-f", "--fullbuild", help="Force a full build", action="store_true", default=False)

args = parser.parse_args()

builder = SongbookBuilder(args.dir)
if(args.instrument):
    builder.build_instrument(args.instrument, args.fullbuild)
else:
    builder.build_all(args.fullbuild)
    
       
        
