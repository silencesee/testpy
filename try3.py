# encoding: UTF-8
from try2 import *
class Parrot(object):
    def __init__(self):
        self._voltage = 100000
        self.__high = 5


    @property
    def voltage(self):
        """Get the current voltage."""
        return self._voltage

    @property
    def high(self):
        return self.__high

    # @voltage.setter
    # def voltage(self, new_value):
    #     if new_value<0:
    #         raise ValueError('value must be > 0')
    #         return
    #     self._voltage = new_value


if __name__ == "__main__":
    tt1()
    val1