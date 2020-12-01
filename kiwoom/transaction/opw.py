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
from kiwoom.handler import Handler
from kiwoom.method import SetInputValues, CommRqData, GetCommData

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
        temp = Handler.db[cls.trcode]
        Handler.db[cls.trcode] = []  # flush
        print(temp)
        return temp


class OPW00018(TR):
    trcode: str = "opw00018"
    rcname: str = "계좌평가잔고내역"
    window: str = "2000"

    @staticmethod
    def excute():
        data = list()
        data.append(GetCommData("opw00018", "계좌평가잔고내역", 0, "총매입금액"))
        data.append(GetCommData("opw00018", "계좌평가잔고내역", 0, "총평가금액"))
        data.append(GetCommData("opw00018", "계좌평가잔고내역", 0, "총평가손익금액"))
        data.append(GetCommData("opw00018", "계좌평가잔고내역", 0, "총수익률(%)"))
        data.append(GetCommData("opw00018", "계좌평가잔고내역", 0, "추정예탁자산"))
        return data


class OPW00001(TR):
    trcode: str = "opw00001"
    rcname: str = "예수금상세현황요청"
    window: str = "2001"

    @staticmethod
    def execute():
        data = list()
        data.append(GetCommData("opw00001", "예수금상세현황요청", 0, "d+2추정예수금"))
        return data
