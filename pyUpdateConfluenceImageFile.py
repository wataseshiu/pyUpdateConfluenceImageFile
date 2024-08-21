#!/usr/bin/env python
# coding: utf-8

# In[1]:


#インストール
get_ipython().system('pip install atlassian-python-api')

#APIで扱うには、Confluenceアカウントのメールアドレスと、設定で発行するAPIトークンが必要
from atlassian import Confluence
confluence = Confluence(
    url='https://xxxx.atlassian.net',
    username='username@user.com',
    password='password')

# In[2]:


#更新したいローカルファイルのリストを作成する
folderPath = 'folderPath'

import glob

localFilePath = glob.glob(folderPath + "/*.jpg")


# In[3]:


#子ページ取得
def GetChildPageId(parent_page):
    
    #引数のページから、子ページを探す
    child_pages = confluence.get_page_child_by_type(parent_page, type='page', start=None, limit=None)
    #子ページが無ければ終了？
    if child_pages == []:
        return child_pages

    #ページがある場合は、子ページのID取得
    page_id = [data.get('id') for data in child_pages]
    return page_id


# In[4]:


space = 'space'

pageIdList=[]
#更新対象となるページ以下のページIDリストを作る
root_page = 12345
pageIdList.append(root_page)
#1階層目
pageId1 = GetChildPageId(root_page)
pageIdList = pageIdList + pageId1

#2階層目
for pageId in pageId1:
    pageId2 = GetChildPageId(pageId)
    if pageId2 != []:
        #2階層目のページをリストに追加
        pageIdList = pageIdList + pageId2
        #3階層目
        for pageIdin2 in pageId2:
            pageId3 = GetChildPageId(pageIdin2)
            if pageId3 != []:
                #3階層目のページをリストに追加
                pageIdList = pageIdList + pageId3
print(pageIdList)


# In[5]:


def SearchAndUpdateFileInPage(page_id):
    import pathlib

    #confluence のページごとに添付ファイルをリストアップ
    name = confluence.get_attachments_from_content(page_id, start=0, limit=50, expand=None, filename=None, media_type=None).get('results')

    name_list = [data.get('title') for data in name]
    name_list
    
    #ローカルファイルと同じファイル名のデータを探す
    for name in name_list:
        for fileName in localFilePath:
            if name in pathlib.Path(fileName).name:
                #データがあったら、ファイルを更新する
                confluence.attach_file(fileName, name=None, content_type=None, page_id=page_id, title=None, space=None, comment=None)


# In[6]:


#ページごとに、ファイルの存在チェックをして、存在しているファイルはアップロードをする
for page_id in pageIdList:
    SearchAndUpdateFileInPage(page_id)
