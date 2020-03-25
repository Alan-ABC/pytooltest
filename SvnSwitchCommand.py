import os
UNITY_PROJECT_PATH = 'F:/Work/Naruto_CubinetTrunk/Assets/Plugins/Android'


def SwitchSvnPath():
    os.system('cd /d %s;svn sw --ignore-ancestry https://192.168.1.242/svn/Naruto/Program/Client/GameSDK/Cubinet/OppoSDK/Android  --username=xianx --password=123456' % UNITY_PROJECT_PATH)


if __name__ == '__main__':
    SwitchSvnPath()