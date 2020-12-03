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
    GetCommDataEx,
)
from kiwoom.transaction.utils import change_format


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
    def get_values(cls, keys):
        data = list()
        for key in keys:
            data.append(GetCommData(cls.trcode, cls.rcname, 0, key))
        return data

    @classmethod
    def get_multi_values(cls, keys):
        data = GetCommDataEx(cls.trcode, cls.rcname)
        print(data)
        return data

    def __str__(self):
        return self.trcode


class OPW00018(TR):
    trcode: str = "opw00018"
    rcname: str = "계좌평가잔고내역"
    window: str = "2000"

    @classmethod
    def get_values(cls, keys):
        data = super().get_values(keys)
        data = list(map(lambda x: change_format(x), data))
        data[3] = (
            float(eval(data[3] / 300))
            if Handler.kiwoom.server == 1
            else data[3]
        )
        return data

    @staticmethod
    def execute(keys):
        data = list()
        data.append(GetCommData("opw00018", "계좌평가잔고내역", 0, "총매입금액"))
        data.append(GetCommData("opw00018", "계좌평가잔고내역", 0, "총평가금액"))
        data.append(GetCommData("opw00018", "계좌평가잔고내역", 0, "총평가손익금액"))
        data.append(GetCommData("opw00018", "계좌평가잔고내역", 0, "총수익률(%)"))
        data.append(GetCommData("opw00018", "계좌평가잔고내역", 0, "추정예탁자산"))

        data = list(map(lambda x: change_format(x), data))
        data[3] = (
            float(eval(data[3] / 300))
            if Handler.kiwoom.server == 1
            else data[3]
        )

        return data


class OPW00001(TR):
    trcode: str = "opw00001"
    rcname: str = "예수금상세현황요청"
    window: str = "2001"

    @classmethod
    def get_values(cls, keys):
        data = super().get_values(keys)
        data = list(map(change_format, data))
        return data

    @staticmethod
    def execute():
        data = list()
        data.append(GetCommData("opw00001", "예수금상세현황요청", 0, "d+2추정예수금"))
        data = list(map(lambda x: x.lstrip("0"), data))
        return data
