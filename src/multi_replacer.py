#!/usr/bin/python3

import skl_shared.shared as sh
from skl_shared.localize import _

import logic as lg


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



class Replacer:
    
    def __init__(self):
        self.set_values()
    
    def set_values(self):
        self.Success = True
        self.text = ''
        self.what = []
        self.with_ = []
    
    def get_input(self):
        f = '[MultiReplacer] multi_replacer.Replacer.get_input'
        if not self.Success:
            sh.com.cancel(f)
            return
        text = sh.Clipboard().paste()
        #text = sh.com.run_fast_txt(text)
        title = _('Enter tab-delimited text:')
        sh.objs.get_txt().reset(title=title, text=text)
        sh.objs.txt.show()
        self.text = sh.objs.txt.get()
    
    def set_lists(self):
        f = '[MultiReplacer] multi_replacer.Replacer.set_lists'
        if not self.Success:
            sh.com.cancel(f)
            return
        if not self.text:
            self.Success = False
            sh.com.rep_empty(f)
            return
        lists = self.text.splitlines()
        lists = [line.strip() for line in lists if line.strip()]
        if not lists:
            self.Success = False
            sh.com.rep_empty(f)
            return
        if len(lists) != self.text.count('\t'):
            self.Success = False
            sub = '{} == {}'.format(len(lists), self.text.count('\t'))
            mes = _('The condition "{}" is not observed!').format(sub)
            sh.objs.get_mes(f, mes, True).show_warning()
            return
        for i in range(len(lists)):
            if lists[i].count('\t') != 1:
                self.Success = False
                mes = _('Wrong input data "{}" at row #{}!').format(lists[i], i)
                sh.objs.get_mes(f, mes, True).show_warning()
                return
            what, with_ = lists[i].split('\t')
            self.what.append(what)
            self.with_.append(with_)
    
    def sort_by_len(self):
        f = '[MultiReplacer] multi_replacer.Replacer.sort_by_len'
        if not self.Success:
            sh.com.cancel(f)
            return
        self.what, self.with_ = zip(*sorted(zip(self.what, self.with_), key=lambda x: len(x[0]), reverse=True))
    
    def run(self):
        self.get_input()
        self.set_lists()
        self.sort_by_len()


if __name__ == '__main__':
    sh.com.start()
    '''
    path = '/home/pete/bin/mclient'
    iwalker = Walker(path)
    iwalker.run()
    text = '\n'.join(iwalker.files)
    print(text)
    '''
    irepl = Replacer()
    irepl.run()
    mes = 'What:\n{}\n\nWith:\n{}'.format("\n".join(irepl.what), "\n".join(irepl.with_))
    print(mes)
    sh.com.end()
