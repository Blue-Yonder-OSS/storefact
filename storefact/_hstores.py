# -*- coding: utf-8 -*-
""""""

from __future__ import (absolute_import, division, print_function)
import os

from simplekv.contrib import ExtendedKeyspaceMixin
from simplekv.fs import FilesystemStore
from simplekv.memory import DictStore
from simplekv.memory.redisstore import RedisStore
from simplekv.net.azurestore import AzureBlockBlobStore
from simplekv.net.botostore import BotoStore


class HDictStore(ExtendedKeyspaceMixin, DictStore):
    pass


class HRedisStore(ExtendedKeyspaceMixin, RedisStore):
    pass


class HAzureBlockBlobStore(ExtendedKeyspaceMixin, AzureBlockBlobStore):
    pass


class HBotoStore(ExtendedKeyspaceMixin, BotoStore):
    def size(self, key):
        k = self.bucket.lookup(self.prefix + key)
        return k.size


class HFilesystemStore(ExtendedKeyspaceMixin, FilesystemStore):
    def size(self, key):
        return os.path.getsize(self._build_filename(key))
