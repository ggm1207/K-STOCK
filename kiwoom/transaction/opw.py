"""
    OPW로 시작하는 TR모음, Docs와 상관없이 소문자로 구현
    필요한 값들만 가져오므로 값이 없을 경우
    KOA Studio를 통해 더 알아봐야 한다.
    E.G)
        opw00018 -> opw00018
        OPW00017 -> opw00017
    Usage:
        opw00018(**kwargs), kwargs는 opw00018에서 요구하는 인자들
        docs참조해서 작성하면 됨.
"""
from copy import copy

from kiwoom.handler import Handler
from kiwoom.method import (
    SetInputValues,
    CommRqData,
    GetCommData,
    GetRepeatCnt,
)


# Transaction 순서
# 1. SetInputValue의 순서 (Set)
# 2. CommRqData의 순서 (Request)
# 3. EventOnReceive에 연락 옴
# 4. GetCommData 사용해서 데이터 가져 옴.

# class OPW(Handler):
# def receive_tr_data(cls, *args):
# raise NotImplementedError

# 우선 동기로 구현, 나중에 비동기로 수정


class TR:
    trcode: str = None
    rcname: str = None
    window: str = None
    multi: bool = False

    @classmethod
    def run(cls, **kwargs):
        SetInputValues(kwargs)
        CommRqData(cls.rcname, cls.trcode, 0, cls.window)

    @classmethod
    def get(cls):
        temp = copy(Handler.db[cls.trcode])
        Handler.db[cls.trcode] = []  # flush
        return temp

    @classmethod
    def get_values(cls, nIndex, keys):
        data = list()
        for key in keys:
            ret = GetCommData(cls.trcode, cls.rcname, nIndex, key)

            if "." in ret:
                ret = str(float(ret)) + "%"
            elif ret[0] == "-":
                if ret[1:].isdecimal():
                    ret = str(int(ret))
            elif ret.isdecimal():
                ret = str(int(ret))
            data.append(ret)

        return data

    def __str__(self):
        return self.trcode


class OPW00018(TR):
    trcode: str = "opw00018"
    rcname: str = "계좌평가결과"
    window: str = "2000"
    multi: bool = False

    @classmethod
    def get_values(cls, keys):
        if cls.multi:
            count = GetRepeatCnt(cls.trcode, cls.rcname)
            data = list()
            for i in range(count):
                data.append(super().get_values(i, keys))
            return data

        data = super().get_values(0, keys)
        return data


class OPW00001(TR):
    trcode: str = "opw00001"
    rcname: str = "예수금상세현황요청"
    window: str = "2001"
    multi: bool = False

    @classmethod
    def get_values(cls, keys):
        data = super().get_values(0, keys)
        return data
