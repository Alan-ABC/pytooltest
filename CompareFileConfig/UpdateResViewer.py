from tkinter import *
from tkinter import ttk
from Helper import *



class UpdateResViewer:
    def __init__(self):
        self._window = None
        self._notbook = None
        self._fromNumber = None
        self._toNumber = None
        self._button = None
        self._tabbooks = []
        self._startNum = 0
        self._endNum = 0
        self._prefix = None
        self._configPath = 'ResVersion1.0.2_'
        self.version_maps_new = {}
        self.version_maps_old = {}
        self.addres = []
        self.delres = []
        self.upres = []

    def CreateWindow(self):
        self._window = Tk()
        self._window.title("查看版本")
        ttk.Label(self._window, text="版本号开始").grid(row=0, column=0)
        self._fromNumber = ttk.Entry(self._window)
        self._fromNumber.grid(row=0, column=1)
        ttk.Label(self._window, text="版本号结束").grid(row=0, column=2)
        self._toNumber = ttk.Entry(self._window)
        self._toNumber.grid(row=0, column=3)
        self._button = ttk.Button(self._window, text="确定", command=self.OnClickButton)
        self._button.grid(row=0, column=4)

        self._notbook = ttk.Notebook(self._window)
        self._notbook.grid(row=1, columnspan=5)

        self._window.mainloop()

    def UpdateWindow(self):
        print('1111111')
        print(self._notbook.select())

    def OnClickButton(self):
        self.InitResourceData()

    def GetPrefix(self, version):
        arr = version.split('.')
        arr.pop()
        end = len(arr)
        outstr = ''

        for i in range(end):
            outstr = '%s%s%s' % (outstr, arr[i], '.')

        return outstr

    def GetExtra(self, version):
        arr = version.split('.')
        return arr[len(arr) - 1]

    def InitResourceData(self):
        start = self._fromNumber.get()
        end = self._toNumber.get()
        prefix = self.GetPrefix(start)
        startNum = int(self.GetExtra(start))
        endNum = int(self.GetExtra(end))
        tabNum = len(self._notbook.tabs())
        self._startNum = startNum
        self._endNum = endNum
        self._prefix = prefix

        self.ReadXml()

        while tabNum > 0:
            self._notbook.forget(0)
            tabNum = len(self._notbook.tabs())
        idx = 0
        for i in range(startNum, endNum + 1):
            tab = ttk.Frame(self._notbook, width=810, height=350)
            columns = ('资源名', 'MD5名', '大小', '状态')
            treev = ttk.Treeview(tab, height=18, show='headings', columns=columns)
            treev.column('资源名', width=300, anchor='center')
            treev.column('MD5名', width=300, anchor='center')
            treev.column('大小', width=100, anchor='center')
            treev.column('状态', width=100, anchor='center')

            treev.heading('资源名', text='资源名')
            treev.heading('MD5名', text='MD5名')
            treev.heading('大小', text='大小')
            treev.heading('状态', text='状态')
            treev.grid(row=2, columnspan=5)
            vscroll = Scrollbar(tab, orient='vertical', command=treev.yview)

            vscroll.grid(row=1, column=6, rowspan=10)
            treev.configure(yscrollcommand=vscroll.set)

            tabdata = self._tabbooks[i - self._startNum]

            if idx > 0:
                self.version_maps_old = self._tabbooks[i - self._startNum - 1]
                self.version_maps_new = tabdata
                self.CompareResVersion()

                adder = 0

                if len(self.addres) > 0:
                    for add in self.addres:
                        treev.insert('', adder, values=(add.name, add.md5, add.size, "增加"))
                        adder += 1

                if len(self.delres) > 0:
                    for rm in self.delres:
                        treev.insert('', adder,
                                     values=(rm.name, rm.md5, rm.size, "删除"))
                        adder += 1

                if len(self.upres) > 0:
                    for up in self.upres:
                        treev.insert('', adder,
                                     values=(up.name, up.md5, up.size, "删除"))

                vscroll.set(0, adder)
            else:
                for da in tabdata:
                    treev.insert('', i - self._startNum, values=(tabdata[da].name, tabdata[da].md5, tabdata[da].size, "增加"))
                vscroll.set(0, len(tabdata))

            idx = idx + 1
            self._notbook.add(tab, text='%s%s%s' % ('RV', prefix, i))
        self._notbook.bind('<<NotebookTabChanged>>', self.UpdateWindow())

    def ReadXml(self):
        for i in range(self._startNum, self._endNum + 1):
            temp = {}
            root = ReadXmlConfig('%s%s%s%s' % (self._configPath, self._prefix, i, '.xml'))
            MakeMapData(root, temp)
            self._tabbooks.append(temp)

    def CompareResVersion(self):
        modify_files_count = 0
        delete_files_count = 0
        self.addres = []
        self.delres = []
        self.upres = []

        for k, v in self.version_maps_old.items():
            if k in self.version_maps_new:
                # print(k)
                # print(version_maps_online[k].md5)
                # print(version_maps[k].md5)
                if self.version_maps_old[k].md5 != self.version_maps_new[k].md5:
                    # update_file_info = '文件名：%s，原MD5码：%s，现MD5码：%s' % (
                    # k, self.version_maps_old[k].md5, self.version_maps_new[k].md5)
                    # print(update_file_info)
                    self.upres.append(self.version_maps_new[k])
                    modify_files_count += 1

                del self.version_maps_new[k]
            else:
                # delete_file_info = '删除的文件名：%s,MD5码：%s' % (k, self.version_maps_old[k].md5)
                # print(delete_file_info)
                self.delres.append(self.version_maps_old[k])
                delete_files_count += 1

        if modify_files_count > 0:
            print('修改的文件数量：%s' % modify_files_count)

        if delete_files_count > 0:
            print('删除的文件数量：%s' % delete_files_count)

        add_files_count = len(self.version_maps_new)

        for remain in self.version_maps_new:
            #remain_file_info = '增加的文件名：%s，MD5码：%s' % (remain, self.version_maps_new[remain].md5)
            #print(remain_file_info)
            self.addres.append(self.version_maps_new[remain])

        if add_files_count > 0:
            print('增加的文件数量：%s' % add_files_count)

        update_total_count = add_files_count + modify_files_count

        if update_total_count > 0:
            print('更新的文件总数量：%s' % update_total_count)


if __name__ == '__main__':
    viewer = UpdateResViewer()
    viewer.CreateWindow()