class VersionData:
    def __init__(self):
        self._name = None
        self._md5 = None
        self._size = None

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def md5(self):
        return self._md5

    @md5.setter
    def md5(self, value):
        self._md5 = value

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value):
        self._size = value
