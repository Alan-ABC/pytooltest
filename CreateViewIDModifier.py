import chardet
from enum import Enum
import os
import re
from FileSystem import CFileSystem


# ----------------------------------------------------#
# 界面ID操作类
# ----------------------------------------------------#
class CCreateViewIDModifier:
    s_regexList = [
        re.compile(r'GuiMgr:CreateView\(([\"|\']\w*[\"|\'])'),
        re.compile(r'CS\.IView\.SetUIData\(([\"|\']\w*[\"|\'])'),
        re.compile(r'CS\.IView\.GetUIData\(([\"|\']\w*[\"|\'])'),
        re.compile(r'GuiMgr:DestroyView\(([\"|\']\w*[\"|\'])'),
        re.compile(r'GuiMgr:GetView\(([\"|\']\w*[\"|\'])'),
        re.compile(r'GuiMgr:ShowView\(([\"|\']\w*[\"|\'])'),
        re.compile(r'SetUIDataByPanelName\(([\"|\']\w*[\"|\'])'),
        re.compile(r'GetUIDataByPanelName\(([\"|\']\w*[\"|\'])'),
        re.compile(r'GetUIDataByPanelName\(([\"|\']\w*[\"|\'])'),
        re.compile(r'CS\.GUIManager\.Instance:CreateView\(([\"|\']\w*[\"|\'])'),
        re.compile(r'CS\.GUIManager\.Instance:DestroyView\(([\"|\']\w*[\"|\'])'),
    ]

    s_regexList2 = [
        re.compile(r'CS\.GUIManager\.Instance:CreateView\((self\.name)'),
        re.compile(r'CS\.GUIManager\.Instance:DestroyView\((self\.name)'),
        re.compile(r'GuiMgr:CreateView\((self\.name)'),
        re.compile(r'GuiMgr:DestroyView\((self\.name)'),
    ]

    # 初始化
    def __init__(self):
        self.m_IgnoreFiles = ('.meta', 'LuaDebug.lua.txt')
        self.m_IgnoreFolders = ('3rd', '.vscode')
        self.m_Encoding = None
        self.m_DestDir = None
        self.m_WorkDir = None
        self.m_TextOperate = None
    
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

    # 删除调试信息
    # codeText 代码文本
    def DeleteDebugInfo(self, codeText, className):
        for regx in self.s_regexList:
            uiNames = regx.findall(codeText)

            for uiName in uiNames:
                repName = uiName.replace('"', '')
                repName = repName.replace('\'', '')
                locName = 'UIPanelIDDef.' + repName
                codeText = codeText.replace(uiName, locName)

        for regx2 in self.s_regexList2:
            uiNames = regx2.findall(codeText)

            for uiName in uiNames:
                locName = 'UIPanelIDDef.' + className
                codeText = codeText.replace(uiName, locName)

        return codeText

    # 执行清除
    # dirPath 根目录
    def ExecuteClear(self, dirPath):
        filelist = CFileSystem.GetChildrenFilesByPath(dirPath)

        if filelist is not None and len(filelist) > 0:
            for filePath in filelist:
                # print(filePath)
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
        
        shot_name = self.GetUIPanelNameByPath(filePath)
        text = data.decode(self.m_Encoding)
        text = self.DeleteDebugInfo(text, shot_name)

        # saveDir = filePath.replace(self.WorkDir, self.m_DestDir)
        self.SaveText(filePath, text)

    # 通过路径获取界面名
    # path 路径名
    @staticmethod
    def GetUIPanelNameByPath(self, path):
        _, fileName = os.path.split(path)
        shot_name, _ = os.path.splitext(fileName)
        shot_name, _ = os.path.splitext(shot_name)
        
        shot_name = shot_name.replace('PanelCtrl', 'Panel')
        return shot_name

    # 保存修改过的文件
    # path 文件路径
    # codeText 代码文本
    def SaveText(self, path, codeText):
        newFile = open(path, 'wb')
        codeText = codeText.encode(self.m_Encoding)
        newFile.write(codeText)
        newFile.close


if __name__ == "__main__":
    unused = CCreateViewIDModifier()
    # unused.ExecuteClear('D:/zestdir')
    unused.ExecuteClear('F:/Work/Naruto_CubinetTrunk/Assets/AssetData/Lua')