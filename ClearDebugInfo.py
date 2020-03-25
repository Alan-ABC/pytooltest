from FileSystem import CFileSystem
from FileSystem import CFileType

from DebugInfoCleaner import CDebugInfoCleaner
from DebugInfoCleaner import CTextOpertation
import os
import sys


if __name__ == "__main__":
    '''abc = CFileSystem()
    files = abc.GetFilesByPath('d:/python', CFileType.Both)

    if files != None:
        for path in files:
            print(path)
    '''
    dd = CDebugInfoCleaner()
    # hasVal = dd.ContainIgnoreFile('d:/LuaDebug.lua')
    # print(hasVal)
    dd.TextOperate = CTextOpertation.Delete
    # path = 'd:/aaa/bbb/ccc/a.txt'
    # dir = os.path.abspath(os.path.dirname(path) + os.path.sep + ".")
    # print(dir)

    # dd.ExecuteClear('D:/newclient/Assets/AssetData/Lua')
    dd.ExecuteClear('D:/zestdir')
    print('ok!')

