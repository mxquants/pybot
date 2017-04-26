#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import dropbox
import os
# %% 

def getDropBoxToken(dropbox_user='rhdzmota'):
    if dropbox_user == 'rhdzmota':
        return 'J8xY1wAWhmAAAAAAAAAACwdIjC1mQU6-Mnd6tq5lCPItxnHF0sIz_XGsqZLifoLF'
    return None

# %% 
class DropBoxManager(object):
    
    
    def __init__(self,dropbox_user='rhdzmota'):
        self.token = getDropBoxToken(dropbox_user)
        self.dbox  = dropbox.Dropbox(self.token)
        
    def getListOfFiles(self,path=""):
        ListFolderResult = self.dbox.files_list_folder(path=path)
        return list(map(lambda x: x.name,ListFolderResult.entries))
    
    def deleteFile(self,filename='temp.png',path=""):

        files = self.getListOfFiles(path)
        
        if filename in files:
            delete_info = self.dbox.files_delete(path=path+'/'+filename)
            return {'status':1,'desc':'deleted file: {}'.format(filename)}
        return {'status':1,'desc':'not found: {}'.format(filename)}
        
    def writeTestFile(self,filename='temp.png'):
        import numpy as np
        import matplotlib.pyplot as plt
        
        x = np.arange(10)
        
        plt.plot(x,list(map(lambda x: np.sin(x)**2,x)))
        plt.savefig(filename)
    
    def uploadFile(self,path="",filename='temp.png'):
        
        # open file and upload to dropbox
        with open(filename,'rb') as file:
            f = file.read()
            self.dbox.files_upload(f,path+'/'+filename)
        return 1
    
    def getTemporaryUrl(self,path='',filename='temp.png'):
        
        # temporary url
        temporary_url = self.dbox.files_get_temporary_link(path+'/'+filename)
        return {'url':temporary_url.link,'metadata':temporary_url.metadata}
    
# %% 






