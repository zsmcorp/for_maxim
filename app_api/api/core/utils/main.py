import random
from typing import Optional, Union, Any, List, Callable, Type, Iterable
import os
import re
import _io
from django.core.files import File
from django.http import QueryDict
from django.utils.crypto import get_random_string
import string
from django.utils import timezone
from datetime import datetime

from pytz import UTC
from itertools import groupby
import itertools
from collections import OrderedDict
import collections.abc
import difflib
from uuid import UUID
from copy import deepcopy
import json
import logging

logger = logging.getLogger(__name__)


# # special value placeholder for filtering empty values
class _SpecNone:
    def __bool__(self):
        return False


SpecNone = _SpecNone()

# # datetimes

EPOCH_DATETIME = datetime(1970, 1, 1)
EPOCH_DATETIME_AWARE = datetime(1970, 1, 1, tzinfo=UTC)

NULL_DATETIME = datetime.min  # datetime(1, 1, 1)
NULL_DATETIME_AWARE = timezone.make_aware(NULL_DATETIME, UTC)

# # uuid
NULL_UUID = UUID('0' * 32)


def id_generator(size=20, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


# # str similarity
def str_similarity(seq1: str, seq2: str) -> float:  # case insensetive
    return difflib.SequenceMatcher(a=seq1.lower(), b=seq2.lower()).ratio()


def find_str_similar(s: str, lst: Union[set, list], similarity: float) -> Optional[str]:
    # returns most similar and checks minimum similarity condition
    # if not met condition or no similar found - returns None
    lst = set(lst)
    similarities = sorted(
        [(str_similarity(s, t), t) for t in lst],
        reverse=True
    )
    if similarities and similarities[0][0] >= similarity:
        return similarities[0][1]
    return None


# # types

NoneType = type(None)


def not_none(e, noneoverride=None) -> bool:
    return e is not noneoverride


def islist(e) -> bool:
    return isinstance(e, list)


def istuple(e) -> bool:
    return isinstance(e, tuple)


def islisttuple(e) -> bool:
    return isinstance(e, (list, tuple))


def islisttupleset(e) -> bool:
    return isinstance(e, (list, tuple, set))


def isdict(e) -> bool:
    return isinstance(e, dict)


def isstr(e) -> bool:
    return isinstance(e, str)


def isnum(e) -> bool:
    return isinstance(e, (int, float))


def isint(e) -> bool:
    return isinstance(e, int)


def isfloat(e) -> bool:
    return isinstance(e, float)


def isbool(e) -> bool:
    return isinstance(e, bool)


def check_allowed_types_list(l: list, types: list) -> bool:
    types = tuple(types)
    return all([isinstance(e, types) for e in l])


def check_nums_list(l: list) -> bool:
    return check_allowed_types_list(l, [int, float])


# # misc

def args_list(*args) -> list:
    return list(args)


def kwargs_dict(**kwargs) -> dict:
    return kwargs


def apply_if_type(v: Any, t: Type, c: Callable):
    if isinstance(v, t):
        return c(v)
    return v


def stripped_if_str(s: Any) -> Optional[str]:
    if isinstance(s, str):
        return s.strip()
    return s


def stripped_if_str_list(l: list) -> list:
    return [stripped_if_str(e) for e in l]


def filter_as_true(l: list):
    return [e for e in l if e]


# # misc 2

def json_try_parse(dstr: str) -> Optional[Any]:
    try:
        return json.loads(dstr)
    except Exception:
        pass
    return None


def try_iso_date_parse(datestr: str, noneoverride=None) -> Optional[datetime]:
    assert datetime.fromisoformat
    try:
        return datetime.fromisoformat(datestr)
    except Exception:
        return noneoverride


def int_in_range(value: int, start: int, end: int):
    if value < start:
        return start
    elif value > end:
        return end
    return value


def floor_to_list(v: Union[int, float], floors: list, default=None) -> Union[int, float]:
    # 12, [0, 15, 30], None -> 0 # -1, [0, 15, 30], None -> None
    return next((c for c in sorted(list(set(floors)), reverse=True) if v >= c), default)


def ceil_to_list(v: Union[int, float], ceils: list, default=None) -> Union[int, float]:
    # 12, [0, 15, 30], None -> 15 # 35, [0, 15, 30], None -> None
    return next((c for c in sorted(list(set(ceils))) if v <= c), default)


def assert_exc(cond: Any, exc: Exception):
    if not cond:
        raise exc


def bool_reverse_if(v: bool, cond: bool):
    return v if not cond else not v


def path_no_ext(p: str, basename=False) -> str:
    if basename:
        p = os.path.basename(p)
    p = os.path.splitext(p)[0]
    return p


def path_get_ext(p: str, pre_dot_if_found=False) -> str:
    r = os.path.splitext(p)[1].strip('.')
    return r if not (pre_dot_if_found and r) else f'.{r}'


def path_dot_if_ext(p: str) -> str:
    return f'.{p}' if p else ''


# # misc 3

def conditional_decorator(dec, condition, *args, **kwargs):  # apply decorator on condition
    def decorator(func):
        if not condition:
            return func
        return dec(*args, **kwargs)(func)

    return decorator


def make_random_string(len: int = 8, charset: str = string.ascii_letters + string.digits):
    return get_random_string(len, charset)


def timestamp_alpha_code(ten_alphas='PMIBTVRCWX') -> str:
    srcs = '0123456789'
    assert len(set(srcs)) == len(set(ten_alphas))
    alphanum = dict(zip(srcs, ten_alphas))
    code = re.sub('[^0-9]', '', datetime.now().isoformat())
    for n, a in alphanum.items():
        code = code.replace(n, a)
    return code


def fullgroupby(i: Iterable, key: Callable):  # the values from key func should be sortable
    # group by returns - pairs of key and found key value pairs
    return groupby(sorted(i, key=key), key=key)


# misc 4 django

def querydict_to_full_dict(qd: QueryDict) -> dict:
    return dict([(k, vl if len(vl) > 1 else vl[0]) for k, vl in qd.lists()])


def file_bool(file: Union[File, _io.BufferedReader]):
    return bool(not_none(file) and getattr(file, 'size', 0) > 0)


# # lists

def unique(ll) -> list:
    # keeps order, while set destroys it
    return list(OrderedDict.fromkeys(ll))


def flattenstep(l: List[Union[list, tuple]]):  # flatten list of lists, requires to be List[list]
    return list(itertools.chain.from_iterable(l))


def flattendeep(l: Union[list, tuple]):  # flatten lists recursively (any depth)
    # https://stackoverflow.com/questions/12472338/flattening-a-list-recursively#answer-12472564
    l = list(l)
    if len(l) == 0:
        return l
    if isinstance(l[0], (list, tuple)):
        return flattendeep(l[0]) + flattendeep(l[1:])
    return l[:1] + flattendeep(l[1:])


# # dicts

def reversed_dict(d: dict) -> dict:
    return dict([(v, k) for k, v in d.items()])


def updated(*args: dict):  # non-deep (top level and without coping referenced objects) dicts update
    if not args:
        return {}
    res = args[0].copy()
    [res.update(a) for a in args[1:]]
    return res


def deepupdate(d, u):  # updates d, future both mutual danger
    def _is_mapping(e):
        return isinstance(e, collections.abc.Mapping)

    if _is_mapping(d) and _is_mapping(u):
        for k, v in u.items():
            if _is_mapping(v):
                d[k] = deepupdate(d.get(k, {}), v)
            else:
                d[k] = v
        return d
    return u


def deepupdater(d, u, _copyd=True):
    # not mutates the data
    d = deepcopy(d) if _copyd else d

    def _is_mapping(e):
        return isinstance(e, collections.abc.Mapping)

    if _is_mapping(d) and _is_mapping(u):
        for k, v in u.items():
            if _is_mapping(v):
                d[k] = deepupdater(d.get(k, {}), v, _copyd=False)
            else:
                d[k] = deepcopy(v)
        return d
    return deepcopy(u)


def deeptypesprocessor(dat: Any, ttype: Union[Type, list, tuple, set], process: Callable):
    # not mutates the data if process function doesn't (but keep same objects of not considered types)
    # processes list, tuple, set, dict and types from ttype, others just returns
    # transforms tuple and set types to list
    if type(ttype) not in [list, tuple, set]:
        ttype = [ttype]
    ttype = tuple(ttype)
    if isinstance(dat, ttype):
        return process(dat)
    elif isinstance(dat, (list, tuple, set)):
        return [deeptypesprocessor(d, ttype, process) for d in dat]
    elif isinstance(dat, dict):
        return dict([(deeptypesprocessor(k, ttype, process), deeptypesprocessor(v, ttype, process))
                     for k, v in dat.items()])
    else:
        return dat


def dict_walk(indict, pre=None):  # walk dict with paths
    # https://stackoverflow.com/questions/12507206/how-to-completely-traverse-a-complex-dictionary-of-unknown-depth#answer-12507546
    pre = pre[:] if pre else []
    if isinstance(indict, dict):
        for key, value in indict.items():
            if isinstance(value, dict):
                for d in dict_walk(value, pre + [key]):
                    yield d
            elif isinstance(value, (list, tuple)):
                for v in value:
                    for d in dict_walk(v, pre + [key]):
                        yield d
            else:
                yield pre + [key, value]
    else:
        yield pre + [indict]


def dict_by_path_value(path: list, value: Any):
    d = {}
    dd = d
    dp = None
    dn = None
    for p in path:
        dd[p] = {}
        dp = dd
        dn = p
        dd = dd[p]
    dp[dn] = value
    return d


def dict_excluded(v: dict, exkeys: list) -> dict:
    return dict([(k, v) for k, v in v.items() if k not in exkeys])


# # categorized

class Types:
    NoneType = NoneType
    not_none = not_none
    islist = islist
    isdict = isdict
    isstr = isstr
    isnum = isnum
    isint = isint
    isfloat = isfloat
    isbool = isbool
    check_allowed_types_list = check_allowed_types_list
    check_nums_list = check_nums_list


class Lists:
    unique = unique
    flattenstep = flattenstep
    flattendeep = flattendeep


class Dicts:
    reversed_dict = reversed_dict
    updated = updated
    deepupdate = deepupdate
    deepupdater = deepupdater
    deeptypesprocessor = deeptypesprocessor
    dict_walk = dict_walk
    dict_by_path_value = dict_by_path_value
    dict_excluded = dict_excluded


# # properties, classes

class Properties:
    """
    Provide methods to get lists of names of properties which have getters / setters / deleters
    (works for builtin property class and its subclasses)

    # prop.fget - getter; prop.fset - setter; fdel - deleter;

    ref: https://stackoverflow.com/questions/49943380/check-if-class-property-with-setter
    """

    @staticmethod
    def get_readable(cls) -> list:
        return [attr for attr, value in vars(cls).items()
                if isinstance(value, property) and value.fget is not None]

    @staticmethod
    def get_writeable(cls) -> list:
        return [attr for attr, value in vars(cls).items()
                if isinstance(value, property) and value.fset is not None]

    @staticmethod
    def get_deletable(cls) -> list:
        return [attr for attr, value in vars(cls).items()
                if isinstance(value, property) and value.fdel is not None]

    #

    @staticmethod
    def get_readable_recursive(cls, unique: bool = True) -> list:
        res = Properties.get_readable(cls) + flattenstep(
            [Properties.get_readable_recursive(cls, False) for cls in cls.__bases__]
        )
        if unique:
            res = list(OrderedDict.fromkeys(res))
        return res

    @staticmethod
    def get_writeable_recursive(cls, unique: bool = True) -> list:
        res = Properties.get_writeable(cls) + flattenstep(
            [Properties.get_writeable_recursive(cls, False) for cls in cls.__bases__]
        )
        if unique:
            res = list(OrderedDict.fromkeys(res))
        return res

    @staticmethod
    def get_deletable_recursive(cls, unique: bool = True) -> list:
        res = Properties.get_deletable(cls) + flattenstep(
            [Properties.get_deletable_recursive(cls, False) for cls in cls.__bases__]
        )
        if unique:
            res = list(OrderedDict.fromkeys(res))
        return res


class Classes:
    @staticmethod
    def get_bases(cls) -> list:
        return list(cls.__bases__)

    @staticmethod
    def get_bases_recursive(cls) -> list:
        return Classes.get_bases(cls) + flattenstep(
            [Classes.get_bases_recursive(cls) for cls in cls.__bases__]
        )

    @staticmethod
    def get_chain(cls) -> list:
        return [cls] + list(Classes.get_bases_recursive(cls))
