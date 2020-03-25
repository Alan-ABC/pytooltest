import os
from enum import Enum

# ----------------------------------------------------#
# 文件的类型
# ----------------------------------------------------#
class CFileType(Enum):
    File = 1 # 文件
    Dir = 2  # 文件夹
    Both = 3 # 全部


# ----------------------------------------------------#
# 文件操作类
# ----------------------------------------------------#
class CFileSystem:
    # 初始化
    def __init__(self):
        pass

    # 获取该文件夹下的所有文件或文件夹
    # dicPath 目标文件夹
    # fileType 文件类型
    @staticmethod
    def GetFilesByPath(dicPath, fileType):
        if dicPath is None or len(dicPath) == 0:
            return None
        
        flist = []

        for filePath in os.listdir(dicPath):
            isfile = os.path.isfile(filePath)
            abspath = os.path.join(dicPath, filePath)
            abspath = CFileSystem.ReplacePath(abspath)

            if fileType == CFileType.File:
                if isfile:
                    flist.append(abspath) 
            elif fileType == CFileType.Dir:
                if not isfile:
                    flist.append(abspath)
            else:
                flist.append(abspath)

        return flist

    # 获取该文件夹下所有子文件夹的文件
    # dicPath 目标文件夹
    @staticmethod
    def GetChildrenFilesByPath(dicPath):
        if dicPath is None or len(dicPath) == 0:
            return None
        
        flist = []
        for root, _, files in os.walk(dicPath):
            for filePath in files:
                joinPath = os.path.join(dicPath, root, filePath)
                joinPath = CFileSystem.ReplacePath(joinPath)
                flist.append(joinPath)

        return flist
    
    # 转换分割符
    # filePath 文件路径
    @staticmethod
    def ReplacePath(filePath):
        return filePath.replace('\\', '/')

    # 获取文件后缀
    # filePath 文件路径
    @staticmethod
    def GetFileExtension(filePath):
        flist = os.path.splitext(filePath)

        if len(flist) > 1:
            return flist[1]
        else:
            return ''
    
