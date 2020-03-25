from CompareFileConfig.VersionConfigData import VersionData
from FileSystem import CFileSystem
import os
from Helper import *

version_maps_new = {}
version_maps_old = {}


def CheckMD5File(container, file_path):

    file_list = CFileSystem.GetChildrenFilesByPath(file_path)
    name_list = []

    for file in file_list:
        file_name = os.path.basename(file)

        if file_name.find('.meta') > -1:
            continue

        file_name = GetFileNameNoExtra(file_name)
        name_list.append(file_name)

    delay_remove_file_container = []

    for key in container:
        config = container[key]

        if config.md5 in name_list:
            if config.md5 not in delay_remove_file_container:
                delay_remove_file_container.append(config.name)

    for remove_file_name in delay_remove_file_container:
        del container[remove_file_name]

    no_files = len(container)
    no_files_num = 0
    if no_files > 0:
        for no_file in container:
            if no_file.find('Video/') > -1:
                pass
            else:
                print("缺少的文件：%s" % no_file)
                no_files_num = no_files_num + 1

    print("缺少的文件：%s" % no_files_num)


def CheckUnusedMD5File(xml_path, file_path):
    MakeMapData(ReadXmlConfig(xml_path), version_maps_old)
    file_list = CFileSystem.GetChildrenFilesByPath(file_path)
    name_list = []

    for file in file_list:
        file_name = os.path.basename(file)

        if file_name.find('.meta') > -1 or file_name.find('AppResVersion') > -1 or file_name.find('ResVersion') > -1:
            continue

        file_name = GetFileNameNoExtra(file_name)

        name_list.append(file_name)
        # print(file_name)

    delay_remove_file_container = []

    for path in name_list:
        for k, v in version_maps_old.items():
            if path == v.md5:
                delay_remove_file_container.append(path)
                break

    for path in delay_remove_file_container:
        name_list.remove(path)

    num = len(name_list)
    if num > 0:
        for name in name_list:
            print("无用的的文件：%s" % name)
        print("无用的的文件的数量：%s" % num)
    else:
        print("无残留的资源")


def CompareResVersion(oldVersion, newVersion):
    MakeMapData(ReadXmlConfig(oldVersion), version_maps_old)
    MakeMapData(ReadXmlConfig(newVersion), version_maps_new)

    modify_files_count = 0
    delete_files_count = 0

    for k, v in version_maps_old.items():
        if k in version_maps_new:
            # print(k)
            # print(version_maps_online[k].md5)
            # print(version_maps[k].md5)
            if version_maps_old[k].md5 != version_maps_new[k].md5:
                update_file_info = '文件名：%s，原MD5码：%s，现MD5码：%s' % (k, version_maps_old[k].md5, version_maps_new[k].md5)
                print(update_file_info)
                modify_files_count += 1

            del version_maps_new[k]
        else:
            delete_file_info = '删除的文件名：%s,MD5码：%s' % (k, version_maps_old[k].md5)
            print(delete_file_info)
            delete_files_count += 1

    if modify_files_count > 0:
        print('修改的文件数量：%s' % modify_files_count)

    if delete_files_count > 0:
        print('删除的文件数量：%s' % delete_files_count)

    add_files_count = len(version_maps_new)

    for remain in version_maps_new:
        remain_file_info = '增加的文件名：%s，MD5码：%s' % (remain, version_maps_new[remain].md5)
        print(remain_file_info)

    if add_files_count > 0:
        print('增加的文件数量：%s' % add_files_count)

    update_total_count = add_files_count + modify_files_count

    if update_total_count > 0:
        print('更新的文件总数量：%s' % update_total_count)


if __name__ == '__main__':
    #CompareResVersion('ResVersion1.0.4_12.xml', 'ResVersion1.0.4_15.xml')
    '''CheckUnusedMD5File('G:\\更新包\\2020.3.23\\IOS更新文件2020.3.23外网cubinet\\ServerRes1.0.4_1.0.16\\Naruto\\IOS\\High\\ResVersion1.0.4.xml',
                       'G:\\更新包\\2020.3.23\\IOS更新文件2020.3.23外网cubinet\\ServerRes1.0.4_1.0.16\\Naruto\\IOS\\High')'''
    CheckUnusedMD5File(
        'G:\\更新包\\2020.3.23\\Android更新文件2020.3.23外网cubinet\\Android\\ServerRes1.0.2_1.0.53\\Naruto\\Android\\High\\ResVersion1.0.2.xml',
        'G:\\更新包\\2020.3.23\\Android更新文件2020.3.23外网cubinet\\Android\\ServerRes1.0.2_1.0.53\\Naruto\\Android\\High')

    '''MakeMapData(ReadXmlConfig('F:\\main.15.com.narutoslugfest.cubinet.android\\assets\\ResVersion1.0.2.xml'), version_maps_old)
    # CheckMD5File(version_maps_old, 'F:\\main.15.com.narutoslugfest.cubinet.android\\assets')

    # MakeMapData(ReadXmlConfig('ResVersion1.0.2_1.0.51.xml'), version_maps_old)
    # CheckMD5File(version_maps_old, 'F:\\main.15.com.narutoslugfest.cubinet.android\\assets')'''


