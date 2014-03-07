# Copyright (C) Ivan Kravets <me@ikravets.com>
# See LICENSE for details.

from json import load as json_load

from twisted.python.reflect import namedAny


def singleton(cls):
    """ From PEP-318 http://www.python.org/dev/peps/pep-0318/#examples """
    _instances = {}

    def get_instance(*args, **kwargs):
        if cls not in _instances:
            _instances[cls] = cls(*args, **kwargs)
        return _instances[cls]
    return get_instance


def load_service(sas, module, options):
    module = 'smartanthill.%s.service' % module
    return namedAny(module).makeService(sas, options)


def load_config(path):
    with open(path) as fp:
        return json_load(fp)


def merge_nested_dicts(d1, d2):
    for k1, v1 in d1.iteritems():
        if not k1 in d2:
            d2[k1] = v1
        elif isinstance(v1, dict):
            merge_nested_dicts(v1, d2[k1])
    return d2


def calc_crc16(dataset):
    crc_table = [
        0x0000, 0xcc01, 0xd801, 0x1400, 0xf001, 0x3c00, 0x2800, 0xe401,
        0xa001, 0x6c00, 0x7800, 0xb401, 0x5000, 0x9c01, 0x8801, 0x4400
    ]

    crc = 0
    tbl_idx = 0

    for data in dataset:
        tbl_idx = crc ^ (data >> (0 * 4))
        crc = crc_table[tbl_idx & 0x0f] ^ (crc >> 4)
        tbl_idx = crc ^ (data >> (1 * 4))
        crc = crc_table[tbl_idx & 0x0f] ^ (crc >> 4)

    return crc & 0xffff
