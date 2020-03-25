from FileSystem import CFileSystem
import chardet
import re


class CClearUnusedComponent:
    def __init__(self):
        self.m_IgnoreFiles = ('.meta', 'LuaDebug.lua.txt')
        self.m_IgnoreFolders = ('3rd', '.vscode')
        self.m_ExtString = re.compile(r'.+Ctrl\.lua\.txt$')
        self.m_ControlsRex = re.compile(r'local\s*controls\s*=\s*\{([^\}.]*)\}')
        self.m_ControllerNameRex = re.compile(r'(.*)\s*=\s*nil,')
        self.m_DelSplitSpaceRex = re.compile(r'\-\-')
        self.m_Encoding = None

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

    def LookupCtrlFile(self, filePath):
        pass 

    # 删除调试信息
    # codeText 代码文本
    def DeleteDebugInfo(self, codeText):
        # print(codeText)
        # newStr = re.sub(self.s_DeletePattern, '', codeText) # 清除print
        # newStr = re.sub(r'(\-\-\[\[)+(([^\]\]])*)+(\]\])', '', newStr) # 清除多行 --[[]]
        # newStr = re.sub(r'(\-\-)+[^\n\r]*', '', newStr) # 清除单行 --
        # newStr = self.ClearSpaceLines(newStr)
        # print(newStr)
        copyText = codeText
        copyText = copyText.replace('.', '')
        newStr = re.search(self.m_ControlsRex, copyText)

        if newStr is None:
            print('error')
            return
        # print(newStr)
        newStr = newStr.group(1)
        # print(newStr)
        newStr = re.sub(self.m_DelSplitSpaceRex, '', newStr)
        # print(newStr)
        segments = re.findall(self.m_ControllerNameRex, newStr)
        components = []
        for seg in segments:
            components.append(seg.strip())

        for component in components:
            numlist = re.findall(component, codeText)

            if numlist is None or len(numlist) < 2:
                print(component)
    
    # 执行清除
    # dirPath 根目录
    def ExecuteClear(self, dirPath):
        filelist = CFileSystem.GetChildrenFilesByPath(dirPath)

        if filelist is not None and len(filelist) > 0:
            for filePath in filelist:
                self.OpenAndModify(filePath)
                # print(filePath)

    # 打开文件修改
    # filePath 文件路径
    def OpenAndModify(self, filePath):
        if self.ContainsIgnoreFolder(filePath) or self.ContainIgnoreFile(filePath):
            return

        if re.match(self.m_ExtString, filePath) is None:
            return

        print(filePath)
        f = open(filePath, 'rb')
        data = f.read()
        fInfo = chardet.detect(data)
        self.m_Encoding = fInfo['encoding']

        if self.m_Encoding is None:
            return

        text = data.decode(self.m_Encoding)
        self.DeleteDebugInfo(text)
        
        #
        # self.SaveText(filePath, text)

    # 保存修改过的文件
    # path 文件路径
    # codeText 代码文本
    def SaveText(self, path, codeText):
        newFile = open(path, 'wb')
        codeText = codeText.encode(self.m_Encoding)
        newFile.write(codeText)
        newFile.close


if __name__ == "__main__":
    unused = CClearUnusedComponent()
    # unused.ExecuteClear('D:/zestdir')
    unused.ExecuteClear('F:/Work/CT_China/Assets/AssetData/Lua')