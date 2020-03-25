import chardet
from enum import Enum
import os
import re
from FileSystem import CFileSystem


# ----------------------------------------------------#
# 文本操作类型
# ----------------------------------------------------#
class CTextOpertation(Enum):
    Ignore = 1 # 注释
    Delete = 2 # 删除


# ----------------------------------------------------#
# 调试信息操作类
# ----------------------------------------------------#
class CDebugInfoCleaner:
    s_IgnorPattern = re.compile(r'[^(\-\-\n\r)]\s*print')
    s_DeletePattern = re.compile(r'(\-\-)*print\(.*\)')

    # 初始化
    def __init__(self):
        self.m_IgnoreFiles = ('.meta', 'LuaDebug.lua.txt')
        self.m_IgnoreFolders = ('3rd', '.vscode')
        self.m_Encoding = None
        self.m_TextOperate = CTextOpertation.Ignore
        self.m_DestDir = None
        self.m_WorkDir = None
    
    # 获取文本操作类型
    @property
    def TextOperate(self):
        return self.m_TextOperate
    
    # 设置文本操作类型
    @TextOperate.setter
    def TextOperate(self, value):
        self.m_TextOperate = value
    
    # 获取工作路径
    @property
    def WorkDir(self):
        return self.m_WorkDir
    
    # 设置工作路径
    @WorkDir.setter
    def WorkDir(self, value):
        self.m_WorkDir = value
        '''self.m_DestDir = os.path.abspath(value + os.path.sep + 'test')

        if not os.path.exists(self.m_DestDir):
            os.makedirs(self.m_DestDir)
        '''
    # 是否包含此文件
    # filePath 文件路径
    def ContainIgnoreFile(self, filePath):
        if filePath is None or len(filePath) == 0:
            return False
        
        for fileName in self.m_IgnoreFiles:
            if filePath.find(fileName) > -1:
                return True
        
        return False

    # 是否包含此文件夹
    # folderPath 文件夹路径
    def ContainsIgnoreFolder(self, folderPath):
        if folderPath is None or len(folderPath) == 0:
            return False
        
        for folder in self.m_IgnoreFolders:
            if folderPath.find(folder) > -1:
                return True
        
        return False

    # 忽略调试信息
    # codeText 代码文本
    def IgnoreDebugInfo(self, codeText):
        newStr = re.sub(self.s_IgnorPattern, '--print', codeText)
        # print(newStr)
        return newStr

    # 删除空行
    # codeText 代码文本
    @staticmethod
    def ClearSpaceLines(self, codeText):
        lines = codeText.split('\n')

        if lines is None or len(lines) == 0:
            return codeText

        newLines = []
        for line in lines:
            temp = line
            temp = line.strip()
            if temp != '':
                newLines.append(line)

        codeText = '\n'.join(newLines)

        return codeText

    # 删除调试信息
    # codeText 代码文本
    def DeleteDebugInfo(self, codeText):
        newStr = re.sub(self.s_DeletePattern, '', codeText)  # 清除print
        # newStr = re.sub(r'(\-\-\[\[)+(([^\]\]])*)+(\]\])', '', newStr) # 清除多行 --[[]]
        # newStr = re.sub(r'(\-\-)+[^\n\r]*', '', newStr) # 清除单行 --
        newStr = self.ClearSpaceLines(newStr)
        # print(newStr)

        return newStr

    # 执行清除
    # dirPath 根目录
    def ExecuteClear(self, dirPath):
        file_list = CFileSystem.GetChildrenFilesByPath(dirPath)

        if file_list is not None and len(file_list) > 0:
            for filePath in file_list:
                self.OpenAndModify(filePath)
                # print(filePath)

    # 打开文件修改
    # filePath 文件路径
    def OpenAndModify(self, filePath):
        if self.ContainsIgnoreFolder(filePath) or self.ContainIgnoreFile(filePath):
            return

        f = open(filePath, 'rb')
        data = f.read()
        fInfo = chardet.detect(data)
        self.m_Encoding = fInfo['encoding']

        if self.m_Encoding is None:
            return
        
        text = data.decode(self.m_Encoding)

        if self.m_TextOperate == CTextOpertation.Ignore:
            text = self.IgnoreDebugInfo(text)
        elif self.m_TextOperate == CTextOpertation.Delete:
            text = self.DeleteDebugInfo(text)

        # saveDir = filePath.replace(self.WorkDir, self.m_DestDir)
        self.SaveText(filePath, text)

    # 保存修改过的文件
    # path 文件路径
    # codeText 代码文本
    def SaveText(self, path, codeText):
        newFile = open(path, 'wb')
        codeText = codeText.encode(self.m_Encoding)
        newFile.write(codeText)
        newFile.close


