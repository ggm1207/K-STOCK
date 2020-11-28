"""
    OPW로 시작하는 TR모음, Docs와 상관없이 소문자로 구현
    E.G)
        opw00018 -> opw00018
        OPW00017 -> opw00017
    Usage:
        opw00018(**kwargs), kwargs는 opw00018에서 요구하는 인자들
        docs참조해서 작성하면 됨.
"""

from kiwoom.handler import Handler
from kiwoom.method import SetInputValue, SetInputValues, CommRqData, GetCommData

# Transaction 순서
# 1. SetInputValue의 순서 (Set)
# 2. CommRqData의 순서 (Request)
# 3. EventOnReceive에 연락 옴
# 4. GetCommData 사용해서 데이터 가져 옴.

# class OPW(Handler):
# def receive_tr_data(cls, *args):
# raise NotImplementedError


class WaitEvent:
    """Context를 활용한 동기화"""

    def __init__(self, event):
        self._event = event

    def __enter__(self):
        self._event.exec_()

    def __exit__(self, ext_type, ex_value, ex_traceback):
        pass


def opw00018(block, **kwargs):
    """
    Args:
        dict: {
            계좌번호: str
            비밀번호: str
            비밀번호입력매체구분: str
            조회구분: str
        }
    Returns:
        IF "조회구분" == 1:
            [a, b, c, d]: list
            a: 총매입금액
            b: 총평가금액
            c: 총수익률(%)
            d: 추정예탁자산
        ELIF "조회구분" == 2:

    """
    SetInputValues(kwargs)  # 값 설정
    data = list()

    if kwargs["조회구분"] == 1:
        CommRqData("gunmo", "opw00018", "0", "1207")  # 요청
        with WaitEvent(block):  # 대기
            data.append(GetCommData("opw00018", "gunmo", 0, "총매입금액"))
            data.append(GetCommData("opw00018", "gunmo", 0, "총평가금액"))
            data.append(GetCommData("opw00018", "gunmo", 0, "총평가손익금액"))
            data.append(GetCommData("opw00018", "gunmo", 0, "총수익률(%)"))
            data.append(GetCommData("opw00018", "gunmo", 0, "추정예탁자산"))
        return data

    if kwargs["조회구분"] == 2:
        return data


class OPW00001(Handler):
    """계좌평가잔고내역요청
    Args:
        account

    """

    pass

    # def __call__(self):
