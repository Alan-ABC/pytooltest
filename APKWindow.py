from tkinter import *
from tkinter import ttk
import tkinter
import re
import xml.etree.ElementTree as ET
import datetime
import zipfile
import os

from tkinter import messagebox

pathconfigArr = []
platformArr = []

platformDataArr = {}

platformNameArr = []

buildPlatformArr = []
buildSetting = {
    'buildResource': 0,
    "buildPlatformOrAddressFirst": 0,
    "buildResVersionSet": '',
}


class PlatformData:
    def __init__(self):
        self._type = 0
        self._name = ""
        self._packageName = ''
        self._version = ''
        self._bundleCode = 0
        self._useObb = '0'
        self._addresses = []
        self._buildAddress = []

        self._packageLabel = None
        self._packageNameText = None
        self._versionLabel = None
        self._VersionValue = None
        self._codeLabel = None
        self._codeValue = None
        self._splitLabel = None
        self._splitValue = None
        self._listboxLeft = None
        self._listboxRight = None
        self._btn = None
        self._btn3 = None
        self._checkval = None
        self._labFrame = None
        self._addAddressLabel = None
        self._listboxLeft = None
        self._listboxRight = None
        self._tablePage = None
        self.adderIndex = 0

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        self._type = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def packageName(self):
        return self._packageName

    @packageName.setter
    def packageName(self, value):
        self._packageName = value

    @property
    def version(self):
        return self._version

    @version.setter
    def version(self, value):
        self._version = value

    @property
    def tablePage(self):
        return self._tablePage

    @property
    def bundleCode(self):
        return self._bundleCode

    @bundleCode.setter
    def bundleCode(self, value):
        self._bundleCode = value

    @property
    def useObb(self):
        return self._useObb

    @useObb.setter
    def useObb(self, value):
        self._useObb = value

    @property
    def addresses(self):
        return self._addresses

    @addresses.setter
    def addresses(self, value):
        self._addresses = value

    @property
    def buildAddress(self):
        return self._buildAddress

    @buildAddress.setter
    def buildAddress(self, value):
        self._buildAddress = value

    def CheckHasBuildAddress(self, newUrl):
        for url in self.buildAddress:
            if newUrl == url:
                return True

        self.buildAddress.append(newUrl)
        return False

    def RemoveBuildAddress(self, newUrl):
        for url in self.buildAddress:
            if url == newUrl:
                self.buildAddress.remove(newUrl)
                break

    def UpdateTableUI(self, tab):
        self._tablePage = tab
        offy = 5
        platformData = platformDataArr[int(self.type)]

        if self._packageLabel is None:
            self._packageLabel = ttk.Label(tab, text='包名:   ')
            self._packageLabel.place(anchor=NW, y=offy, width=100, height=30)

        if self._packageNameText is None:
            self._packageNameText = tkinter.Entry(tab)
            self._packageNameText.place(anchor=NW, y=offy, x=100, width=400, height=30)

        self._packageNameText.delete(0, 100)
        self._packageNameText.insert(0, platformData.packageName)

        offy = 40

        if self._versionLabel is None:
            self._versionLabel = ttk.Label(tab, text='Version:   ')
            self._versionLabel.place(anchor=NW, y=offy, width=100, height=30)

        if self._VersionValue is None:
            self._VersionValue = ttk.Entry(tab)
            self._VersionValue.place(anchor=NW, y=offy, x=100, width=400, height=30)
            self._VersionValue.bind("<Return>", lambda r: SetVersionValue(int(self.type), self._VersionValue.get()))

        self._VersionValue.delete(0, 100)
        self._VersionValue.insert(0, platformData.version)

        offy = 75

        if self._codeLabel is None:
            self._codeLabel = ttk.Label(tab, text='BundleCode:   ')
            self._codeLabel.place(anchor=NW, y=offy, width=100, height=30)

        if self._codeValue is None:
            self._codeValue = ttk.Entry(tab)
            self._codeValue.place(anchor=NW, y=offy, x=100, width=400, height=30)
            self._codeValue.bind("<Return>", lambda r: SetBundleCodeValue(int(self.type), self._codeValue.get()))

        self._codeValue.delete(0, 100)
        self._codeValue.insert(0, platformData.bundleCode)

        offy = 110

        if self._splitLabel is None:
            self._splitLabel = ttk.Label(tab, text='是否生成Obb:   ')
            self._splitLabel.place(anchor=NW, y=offy, width=100, height=30)
            self._checkval = tkinter.IntVar()
            self._splitValue = tkinter.Checkbutton(tab, variable=self._checkval, command=lambda: SavePlatformSplitByType(int(self.type), self._checkval.get()))
            self._splitValue.place(anchor=NW, y=offy + 5, x=100, width=20, height=20)

        if platformData.useObb == '1':
            self._checkval.set(1)
            self._splitValue.select()
        else:
            self._checkval.set(0)
            self._splitValue.deselect()

        offy = 145
        if self._labFrame is None:
            self._labFrame = ttk.LabelFrame(tab, text='打包地址选择')
            self._labFrame.place(anchor=NW, y=offy, width=800, height=200)

        offy = 170

        if self._addAddressLabel is None:
            self._addAddressLabel = ttk.Label(self._labFrame, text='将需要打包地址双击到右边栏中，如果取消请双击右边的地址')
            self._addAddressLabel.place(x=150, y=5, width=400)

        if self._listboxLeft is None:
            self._listboxLeft = tkinter.Listbox(self._labFrame, selectmode=tkinter.BROWSE)
            self._listboxLeft .place(y=30, width=390, height=80)
            yscrollbar = tkinter.Scrollbar(self._listboxLeft , command=self._listboxLeft .yview)
            yscrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
            self._listboxLeft .config(yscrollcommand=yscrollbar.set)

            for i in range(len(platformData.addresses)):
                self._listboxLeft.insert(tkinter.END, platformData.addresses[i])

        if self._listboxRight is None:
            self._listboxRight = tkinter.Listbox(self._labFrame, selectmode=tkinter.BROWSE)
            self._listboxRight.place(x=420, y=30, width=350, height=80)
            yscrollbarRight = tkinter.Scrollbar(self._listboxRight, command=self._listboxRight.yview)
            yscrollbarRight.pack(side=tkinter.RIGHT, fill=tkinter.Y)
            self._listboxRight.config(yscrollcommand=yscrollbarRight.set)
            self._listboxLeft.bind("<Double-Button-1>",
                                   lambda r: AddUrlToBuildAddress(self._listboxRight, platformData,
                                                                  self._listboxLeft.get(
                                                                    self._listboxLeft.curselection())))
            self._listboxRight.bind("<Double-Button-1>",
                                    lambda r: RemoveUrlFromBuildAddress(self._listboxRight,
                                                                        platformData,
                                                                        self._listboxRight.curselection()))

        offy = offy + 35 * len(platformNameArr) - 15

        if self._btn is None:
            self._btn = ttk.Button(tab, text="修改配置", command=lambda: SavePlatformByType(int(self.type)))
            self._btn.place(x=250, y=offy, width=100, height=30)

        if self._btn3 is None:
            self._btn3 = ttk.Button(tab, text="同步配置", command=lambda: SyncAllPlatform(int(self.type)))
            self._btn3.place(x=450, y=offy, width=100, height=30)


def LoadConfigXml():
    tree = ET.parse('config.xml')
    root = tree.getroot()

    for platform in root.iter('platform'):
        platdata = PlatformData()
        platdata.type = platform.attrib['type']
        platdata.name = platform.attrib['name']
        platdata.packageName = platform.find('packageName').text
        platdata.version = platform.find('version').text
        platdata.bundleCode = platform.find('bundleCode').text
        platdata.useObb = platform.find('useObb').text
        platformNameArr.append(platdata.name)

        for addr in platform.iter('address'):
            platdata.addresses.append(addr.text)

        platformDataArr[int(platdata.type)] = platdata
    vv = str(root.find('resVersion').text)
    buildSetting['buildResVersionSet'] = vv


def WriteConfigXml():
    root = ET.Element('config')
    platforms = ET.SubElement(root, 'platforms')
    count = len(platformNameArr)
    for i in range(count):
        platformData = platformDataArr[i]
        platform = ET.SubElement(platforms, 'platform')
        platform.attrib['type'] = platformData.type
        platform.attrib['name'] = platformData.name
        packageName = ET.SubElement(platform, 'packageName')
        packageName.text = platformData.packageName
        version = ET.SubElement(platform, 'version')
        version.text = platformData.version
        bundleCode = ET.SubElement(platform, 'bundleCode')
        bundleCode.text = platformData.bundleCode
        useObb = ET.SubElement(platform, 'useObb')
        useObb.text = platformData.useObb
        addresses = ET.SubElement(platform, 'addresses')
        for k in range(len(platformData.addresses)):
            address = ET.SubElement(addresses, 'address')
            address.text = platformData.addresses[k]

    resVersion = ET.SubElement(root, 'resVersion')
    resVersion.text = buildSetting['buildResVersionSet']
    tree = ET.ElementTree(root)
    tree.write('config.xml')


def ChangeAndroidMainifestURL(url):
    file = open("AndroidManifest.xml", encoding='utf-8')
    data = file.read()
    url1 = 'meta-data android:name="ResourceServerIp" android:value="' + url + '"'
    data = re.sub('meta-data android:name="ResourceServerIp" android:value=".+"', url1, data)
    url2 = 'meta-data android:name="ResourceBakServerIp" android:value="' + url + '"'
    data = re.sub('meta-data android:name="ResourceBakServerIp" android:value=".+"', url2, data)

    newfile = open("AndroidManifest.xml", 'w+', encoding='utf-8')
    newfile.write(data)
    newfile.close()
    file.close()


def AddUrlToBuildAddress(listbox, platData, url):
    if platData.CheckHasBuildAddress(url) is False:
        listbox.insert(tkinter.END, url)


def RemoveUrlFromBuildAddress(listbox, platData, index):
    removeUrl = listbox.get(index)
    listbox.delete(index)
    platData.RemoveBuildAddress(removeUrl)


def SavePlatformByType(type):
    WriteConfigXml()
    messagebox.showinfo(title='提示', message='保存配置成功')


def SyncAllPlatform(currType):
    platformData = platformDataArr[currType]
    for k in platformDataArr:
        if currType is not k:
            val = platformDataArr[k]
            val.version = platformData.version
            val.bundleCode = platformData.bundleCode
            val.useObb = platformData.useObb
            val.UpdateTableUI(val.tablePage)
    WriteConfigXml()
    messagebox.showinfo(title='提示', message='同步配置成功')


def SavePlatformSplitByType(type, val):
    platformData = platformDataArr[type]
    platformData.useObb = str(val)


def GetPlatformIndex(platName):
    count = len(platformNameArr)
    for i in range(count):
        if platName == platformNameArr[i]:
            return i
    return 0


def SetBuildPlatformFlag(platIdx, val):
    # idx = GetPlatformIndex(platName)
    buildPlatformArr[platIdx] = val


def SetBuildResourceFlag(val):
    buildSetting['buildResource'] = val


def SetBuildPlartformOrAddressFirst(typ, val):
    if typ == 1 and val == 1:
        buildSetting['buildPlatformOrAddressFirst'] = 1
    elif typ == 2 and val == 1:
        buildSetting['buildPlatformOrAddressFirst'] = 2
    else:
        buildSetting['buildPlatformOrAddressFirst'] = 1


def SetVersionValue(typ, val):
    platformData = platformDataArr[typ]
    platformData.version = val


def SetBundleCodeValue(typ, val):
    platformData = platformDataArr[typ]
    platformData.bundleCode = val


def SetResVersionValue(val):
    buildSetting['buildResVersionSet'] = val
    WriteConfigXml()
    messagebox.showinfo(title='提示', message='保存资源版本号成功')


def OnBuildPackage():
    time = datetime.datetime.now().strftime('%Y-%m-%d')
    apkName = '_' + buildSetting['buildResVersionSet']
    apkName = re.sub(r'\.', '_', apkName)
    apkName = time + apkName
    fileName = 'apk_project_build_trunk11301.py'
    platformData = platformDataArr[0]
    if buildSetting['buildResource'] == 1:
        with open(fileName, encoding='utf-8') as f:
            code = compile(f.read(), fileName, 'exec')
            exec(code, {'AppVersion': platformData.version, 'BaseResVersion': '1.0.48',
                        'AddResVersion': buildSetting['buildResVersionSet'],
                        'BuildRes': 1, 'BuildPlayer': 0, 'BundleCode': platformData.bundleCode,
                        'Split': platformData.useObb, 'PlatformIndex': -1, 'ApkName': apkName})

    buildplats = []
    count = len(buildPlatformArr)
    for i in range(count):
        if buildPlatformArr[i].get() == 1:
            buildplats.append(i)

    for k in buildplats:
        platdata = platformDataArr[k]
        for addr in platdata.buildAddress:
            with open(fileName, encoding='utf-8') as f:
                code = compile(f.read(), fileName, 'exec')
                exec(code, {'AppVersion': platformData.version, 'BaseResVersion': '1.0.48',
                            'AddResVersion': buildSetting['buildResVersionSet'], 'BuildRes': 0, 'BuildPlayer': 0,
                            'BundleCode': platformData.bundleCode, 'Split': platformData.useObb,
                            'PlatformIndex': k, 'ApkName': apkName})
            ChangeAndroidMainifestURL(addr)
            with open(fileName, encoding='utf-8') as f:
                code = compile(f.read(), fileName, 'exec')
                exec(code, {'AppVersion': platformData.version, 'BaseResVersion': '1.0.48',
                            'AddResVersion': buildSetting['buildResVersionSet'], 'BuildRes': 0, 'BuildPlayer': 1,
                            'BundleCode': platformData.bundleCode, 'Split': platformData.useObb,
                            'PlatformIndex': -1, 'ApkName': apkName})


def dfs_get_zip_file(input_path, result):
    files = os.listdir(input_path)
    for file in files:
        if os.path.isdir(input_path + '/' + file):
            dfs_get_zip_file(input_path + '/' + file, result)
        else:
            result.append(input_path+'/'+file)


def zip_path(input_path, output_path, output_name):
    f = zipfile.ZipFile(output_path + '/' + output_name, 'w', zipfile.ZIP_DEFLATED)
    filelists = []
    dfs_get_zip_file(input_path, filelists)
    for file in filelists:
        f.write(file)
    f.close()
    return output_path + r"/" + output_name


def zipResource():
    time = datetime.datetime.now().strftime('%Y-%m-%d')
    resVersion = '_' + buildSetting['buildResVersionSet']
    resVersion = re.sub(r'\.', '_', resVersion)
    filename = time + resVersion + '.zip'
    # os.system('cd F:/Work/Naruto_CubinetTrunk/Assets/StreamingAssets;zip -r -m -o \'%s\' \'.*\' ' % filename)
    zip_path('F:/Work/Naruto_CubinetTrunk/Assets/StreamingAssets',
             'F:/Work/Naruto_CubinetTrunk/streamAssetsBackup/', filename)
    # zfile = zipfile.ZipFile(filename, "w", zipfile.ZIP_DEFLATED)
    # zfile.write('F:/Work/Naruto_CubinetTrunk/Assets/StreamingAssets/')
    # filename = 'C:/naruto/StreamingAssets/streamAssetsBackup/' + time + buildSetting['buildResVersionSet'] + '.zip'
    # os.system('cd C:/naruto/CubinetTrunk/Assets/StreamingAssets;zip -r -m -o \'%s\' \'.*\' ' % filename)
    # zfile.close()
    messagebox.showinfo(title='提示', message='备份资源成功')


def MergeResources(fro, to, newV):
    if fro == '' or to == '' or newV == '':
        messagebox.showinfo(title='提示', message='输入正确的合并方式')
        return


LoadConfigXml()
# WriteConfigXml()
# LoadAndroidMainifest('https://naruto-up.obs.ap-southeast-3.myhuaweicloud.com/ob/')
root = Tk()
root.title('打包工具')
root.geometry('810x700')
# root.resizable(False, False)
book = ttk.Notebook(root)
book.pack(side=LEFT, anchor=NE)

for i in range(len(platformNameArr)):
    cubinet = ttk.Frame(book, width=810, height=350)
    book.add(cubinet, text=platformNameArr[i])
    platformData = platformDataArr[i]
    platformData.UpdateTableUI(cubinet)

# -------------------------------------------------------------------
typeLabel = ttk.LabelFrame(root, text="打包平台")
typeLabel.place(anchor=NW, y=400, width=750, height=50)
for i in range(len(platformNameArr)):
    buildPlatformArr.append(tkinter.IntVar())
    cbtn = tkinter.Checkbutton(typeLabel, text=platformNameArr[i], variable=buildPlatformArr[i])
    cbtn.pack(anchor=NW, side=LEFT)

checkbtnList = ttk.LabelFrame(root, text="操作选项")
checkbtnList.place(anchor=NW, y=450, width=750, height=50)
check1 = tkinter.IntVar()
resource1 = tkinter.Checkbutton(checkbtnList, text="打资源", variable=check1,
                                command=lambda: SetBuildResourceFlag(check1.get()))
resource1.pack(side=LEFT)
labRversion = ttk.Label(checkbtnList, text="资源版本号:")
labRversion.pack(side=LEFT)

labRversionText = ttk.Entry(checkbtnList)
labRversionText.pack(side=LEFT)
labRversionText.delete(0, 100)
labRversionText.insert(0, buildSetting['buildResVersionSet'])
labRversionText.bind("<Return>", lambda r: SetResVersionValue(labRversionText.get()))

'''check2 = tkinter.IntVar()
platformFirst = tkinter.Checkbutton(checkbtnList, text="平台优先", variable=check2, 
                                    command=lambda: SetBuildPlartformOrAddressFirst(1, check2.get()))
platformFirst.pack(side=LEFT, padx=30)
check3 = tkinter.IntVar()
addressFirst = tkinter.Checkbutton(checkbtnList, text="地址优先", variable=check3, 
                                    command=lambda: SetBuildPlartformOrAddressFirst(2, check3.get()))
addressFirst.pack(side=LEFT, padx=30)'''

btnList = ttk.LabelFrame(root, text="其它操作选项")
btnList.place(anchor=NW, y=510, width=750, height=100)
backupBtn = ttk.Button(btnList, text="备份资源", command=zipResource)
backupBtn.pack(side=LEFT, padx=20)
'''addResource = ttk.LabelFrame(btnList, text="包合并选项")
addResource.pack(side=LEFT)
lab1 = ttk.Label(addResource, text="从:")
lab1.pack(side=LEFT)
labFrom = ttk.Entry(addResource)
labFrom.pack(side=LEFT)
lab2 = ttk.Label(addResource, text="到:")
lab2.pack(side=LEFT)
labTo = ttk.Entry(addResource)
labTo.pack(side=LEFT)
lab3 = ttk.Label(addResource, text="新版本号:")
lab3.pack(side=LEFT)
newVersion = ttk.Entry(addResource)
newVersion.pack(side=LEFT)
exec = ttk.Button(addResource, text="执行", 
                    command=lambda: MergeResources(labFrom.get(), labTo.get(), newVersion.get()))
exec.pack(side=LEFT)'''

btn = ttk.Button(root, text="打包", command=OnBuildPackage)
btn.place(anchor=CENTER, y=650, relx=0.5, width=200, height=50)

root.mainloop()
