# pyUpdateConfluenceImageFile
Confluenceに配置した画像をローカル上で編集し更新したあと、  
ワンボタンでConfluence側の画像も更新するためのツール  
公式が提供しているAtlassian Python APIを使用してどのページに画像がありファイル名が何かを取得し、  
ローカルフォルダ内の同名ファイルが見つかった場合はそれをConfluenceの各ページに画像のバージョン更新の形でアップロードする。  
https://atlassian-python-api.readthedocs.io/
