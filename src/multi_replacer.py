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
    
    def __init__(self, path):
        self.set_values()
        self.path = path
    
    def set_values(self):
        self.Success = True
        self.text = ''
        self.files = []
        self.errors = []
        self.what = []
        self.with_ = []
    
    def check_path(self):
        f = '[MultiReplacer] multi_replacer.Replacer.check_path'
        if not self.Success:
            sh.com.cancel(f)
            return
        if not self.path:
            self.Success = False
            sh.com.rep_empty(f)
            return
        self.Success = sh.Directory(self.path).Success
    
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
    
    def set_files(self):
        f = '[MultiReplacer] multi_replacer.Replacer.set_files'
        if not self.Success:
            sh.com.cancel(f)
            return
        iwalk = Walker(self.path)
        iwalk.run()
        self.Success = iwalk.Success
        self.files = iwalk.files
    
    def replace(self):
        f = '[MultiReplacer] multi_replacer.Replacer.replace'
        if not self.Success:
            sh.com.cancel(f)
            return
        for file in self.files:
            irepl = lg.Replacer(file, self.what, self.with_)
            irepl.run()
            if not irepl.Success:
                self.errors.append(file)
    
    def report(self):
        f = '[MultiReplacer] multi_replacer.Replacer.report'
        if not self.Success:
            sh.com.cancel(f)
            return
        mes = []
        sub = _('Files processed in total: {}. Errors: {}')
        sub = sub.format(len(self.files), len(self.errors))
        mes.append(sub)
        if self.errors:
            mes.append('')
            sub = _('Files with errors:')
            mes.append(sub)
            mes.append('\n'.join(self.errors))
        mes = '\n'.join(mes)
        sh.objs.get_mes(f, mes).show_info()
    
    def run(self):
        self.check_path()
        self.get_input()
        self.set_lists()
        self.sort_by_len()
        self.set_files()
        self.replace()
        self.report()


if __name__ == '__main__':
    f = '[MultiReplacer] multi_replacer.__main__'
    sh.com.start()
    path = '/home/pete/bin/mclient'
    Replacer(path).run()
    mes = _('Goodbye!')
    sh.objs.get_mes(f, mes, True).show_debug()
    sh.com.end()
