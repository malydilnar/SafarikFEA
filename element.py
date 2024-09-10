
class Element(object):

    def __init__(self, eid, nodes, property, config):
        self._eid = eid
        self._nodes = nodes
        self._property = property
        self._mat = property._mat
        self._shape = property._shape
        self._config = config

    def SetCharLength(self, len_x, len_y):
        self._char_len = max(len_x, len_y)
