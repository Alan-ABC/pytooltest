from FileSystem import CFileSystem
import chardet
import re
from enum import Enum


# ----------------------------------------------------#
# 文本后缀类型
# ----------------------------------------------------#
class CExtension(Enum):
    CS = 1  # c#
    Lua = 2  # lua


class CSyntaxChecker:
    s_Pattern = [
        # re.compile(r'[^(\-\-\n\r)]\s*print')
        re.compile(r'if\s+\(\s*[^\)]+\)\s*;')
    ]

    def __init__(self):
        self.m_TextExt = CExtension.Lua
        self.m_Encoding = None

    # 获取文本后缀类型
    @property
    def TextExt(self):
        return self.m_TextExt
    
    # 设置文本后缀类型
    @TextExt.setter
    def TextExt(self, value):
        self.m_TextExt = value

    # 是否cs或lua
    def CheckTextExt(self, filePath):
        ext = CFileSystem.GetFileExtension(filePath)

        if self.m_TextExt == CExtension.CS:
            return ext == '.cs'
        elif self.m_TextExt == CExtension.Lua:
            return ext == '.txt'

    # 执行清除
    # dirPath 根目录
    def ExecuteCheck(self, dirPath):
        filelist = CFileSystem.GetChildrenFilesByPath(dirPath)

        if filelist is not None and len(filelist) > 0:
            for filePath in filelist:
                # print(filePath)
                if not self.CheckTextExt(filePath):
                    continue
                self.OpenAndCheck(filePath)
                # print(filePath)

    # 打开文件修改
    # filePath 文件路径
    def OpenAndCheck(self, filePath):
        f = open(filePath, 'rb')
        data = f.read()
        fInfo = chardet.detect(data)
        self.m_Encoding = fInfo['encoding']

        if self.m_Encoding is None:
            return
        
        text = data.decode(self.m_Encoding)
        self.PrintInfo(text, filePath)
        f.close()

    # 输出调试信息
    # codeText 代码文本
    def PrintInfo(self, codeText, filePath):
        for rex in self.s_Pattern:
            matches = re.findall(rex, codeText)

            if len(matches) > 0:
                print(filePath)
            
            for match in matches:
                print(match)


if __name__ == "__main__":
    # print('yes')
    sc = CSyntaxChecker()
    sc.TextExt = CExtension.CS
    sc.ExecuteCheck('F:/Work/CT_China/Assets/Scripts')
    print('ok')
