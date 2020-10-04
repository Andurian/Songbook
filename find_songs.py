#!/usr/bin/python
# -*- coding: utf-8 -*-
import os

def find_songs():
    ret = {}
    
    for path, dirs, files in os.walk("songs"):
        files = list(filter(lambda x: x.endswith('.tex'), files))
        
        if not files:
            continue
            
        filename = path.replace('\\', '_')
        data = ""
        
        prefix = path.replace('\\', '/')
        newline = ''
        for f in files:
            line = '{}\\inputafterskip{{{}/{}}}'.format(newline, prefix, f)
            data = data + line
            newline = '\n'
        
        ret[filename] = data
        
    return ret
                
if __name__ == '__main__':
    songs = find_songs()
    for key in songs:
        filename = key + '.tex'
        with open(filename, 'w+') as outfile:
            outfile.write(songs[key])
    