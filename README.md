# Songbook

This is a personal project to create a songbook (actually one book per instrument) to sing from at campfires on warm summer nights.
It uses the LaTeX `songs` package.
The book itself is designed to be easy to read from with minimal page turning within songs.
It is double sided and new songs always start on the left of a doublepage.
New songs can be added easily by creating a new .tex-file in the corresponding songs subdirectory and rerunning the buildscripts.
Each instrument has extra information (most likely chords) that can be printed in an extra chapter at the end of the book.

Currently supported instruments are `Guitar` and `Bouzouki`. 
But other instruments are easy to add.

## Building 

There are two ways of compiling the book.
You can build it (more or less) manually or you can use the automated build.

### Requirements

You need:
  
  - PDFLaTeX
  - LuaLaTeX
  - Python 3
  
LuaLaTeX is more or less optional and only necessary if you want to build the index of the book.
All code is probably platform independent but has only been tested on Windows so far.

### Automated build

This method is preferred if you just want to create the PDFs.
Simpliy navigate to the root directory and run:

    python make_songbook.py
    
After some LaTeX output you should find the finished and appropriately named songbooks in the root directory.

### Manual Build

This method is advised when you want to develop and edit the structure and overall layout songbook.
First you need to run:

    python find_songs.py
    
This will traverse the `songs` directory and write a `songs_<Instrument>.tex` file in the root directory.
Open `Songbook.tex` and insert the name of the instrument you want to build the songbook for in the line:

    \providecommand{\instrument}{<Instrument>}

Run `PDFLaTeX` twice and all songs should be where they are. 
The only thing missing now is the index. 
The index building process requires LuaLaTeX and you need to run:

    texlua songidx.lua <build>/cbtitle.sxd <build>/cbtitle.sbx
    
where `<build>` is your auxiliary build directory.
Now you can run `PDFLaTeX` a final time and you should have your songbook ready.

## Adding new Songs and Instruments

You can add new songs by simply adding new `.tex` files in the directory `songs/<Instrument>`.
New chords or other extra information can be added to the file `extra/extra_<Instrument>.tex` in the `\printextra` command.

New instruments are added by creating a corresponding directory in `songs` and a corresponding file in `extra`.
That file must at least contain a `\printextra` command.

Everything after that should be handled automatically by the build process.

## Design Ideas

This section is only relevant if you plan to change the structure, layout, or the build process of the songbooks.
It will be added later.

    
