# -*- coding: utf-8 -*-
from abc import *


class Repository(ABC):

    @abstractmethod
    def find(self, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def insert(self, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def delete(self, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def clear(self):
        raise NotImplementedError

