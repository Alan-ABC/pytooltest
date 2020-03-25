import xml.etree.ElementTree as etree
from CompareFileConfig.VersionConfigData import VersionData


def GetFileNameNoExtra(file_name):
    new_file_name = file_name

    if file_name.find(r'.') > 0:
        splitList = file_name.split('.')

        if len(splitList) > 0:
            splitList.pop()
            tempStr = ''
            for splitstr in splitList:
                tempStr = '%s%s.' % (tempStr, splitstr)

            new_file_name = tempStr[0:len(tempStr) - 1]
    return new_file_name


def ReadXmlConfig(xml_path):
    xml_data = etree.parse(xml_path)
    xml_root = xml_data.getroot()
    return xml_root


def MakeMapData(tempRoot, container):
    for item in tempRoot.iter('as'):
        version_data = VersionData()
        version_data.name = item.attrib['n']
        version_data.md5 = item.attrib['m']
        version_data.size = item.attrib['s']
        container[version_data.name] = version_data
