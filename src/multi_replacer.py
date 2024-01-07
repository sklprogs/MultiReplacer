#!/usr/bin/python3

import skl_shared.shared as sh
from skl_shared.localize import _


class Walker:
    
    def __init__(self, path):
        self.set_values()
        self.path = path
    
    def set_values(self):
        self.Success = True
        self.formats = ('.py',)
        self.files = []
    
    def set_files(self):
        f = '[MultiReplacer] multi_replacer.Walker.set_files'
        if not self.Success:
            sh.com.cancel(f)
            return
        self.files = sh.Directory(path).get_subfiles()
        if not self.files:
            self.Success = False
            sh.com.rep_empty(f)
            return
    
    def filter(self):
        f = '[MultiReplacer] multi_replacer.Walker.filter'
        if not self.Success:
            sh.com.cancel(f)
            return
        self.files = [file for file in self.files \
                      if sh.Path(file).get_ext_low() in self.formats
                     ]
        if not self.files:
            self.Success = False
            sh.com.rep_lazy(f)
            return
    
    def run(self):
        self.set_files()
        self.filter()


if __name__ == '__main__':
    sh.com.start()
    path = '/home/pete/bin/mclient'
    iwalker = Walker(path)
    iwalker.run()
    text = '\n'.join(iwalker.files)
    print(text)
    sh.com.end()
