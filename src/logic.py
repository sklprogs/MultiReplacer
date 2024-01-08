#!/usr/bin/python3

import skl_shared.shared as sh
from skl_shared.localize import _


class Replacer:
    
    def __init__(self, file, what, with_):
        self.Success = True
        self.file = file
        self.what = what
        self.with_ = with_
        self.text = ''
    
    def check(self):
        f = '[MultiReplacer] logic.Replacer.check'
        if not self.file or not self.what or not self.with_:
            self.Success = False
            sh.com.rep_empty(f)
            return
        self.Success = sh.File(self.file).Success
        if len(self.what) != len(self.with_):
            self.Success = False
            sub = f'{len(self.what)} == {len(self.with_)}'
            mes = _('The condition "{}" is not observed!').format(sub)
            sh.objs.get_mes(f, mes, True).show_warning()
    
    def set_text(self):
        f = '[MultiReplacer] logic.Replacer.set_text'
        if not self.Success:
            sh.com.cancel(f)
            return
        self.text = sh.ReadTextFile(self.file, Empty=True).get()
    
    def replace(self):
        f = '[MultiReplacer] logic.Replacer.replace'
        if not self.Success:
            sh.com.cancel(f)
            return
        for i in range(len(self.what)):
            self.text = self.text.replace(self.what[i], self.with_[i])
    
    def save(self):
        f = '[MultiReplacer] logic.Replacer.save'
        if not self.Success:
            sh.com.cancel(f)
            return
        self.Success = sh.WriteTextFile(self.file, True, True).write(self.text)
    
    def run(self):
        self.check()
        self.set_text()
        self.replace()
        self.save()
