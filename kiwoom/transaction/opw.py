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

from kiwoom.method import (
    SetInputValue,
    SetInputValues,
    CommRqData,
    GetCommData,
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

# 레코드명 삽입: 

class WaitEvent:
    """Context를 활용한 동기화"""

    def __init__(self, event):
        self._event = event

    def __enter__(self):
        self._event.exec_()

    def __exit__(self, ext_type, ex_value, ex_traceback):
        pass


def opw00018(helper, **kwargs):
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
        CommRqData("opw00018_req", "opw00018", 0, "2000")  # 요청
        SetInputValue("조회구분", "3")
        CommRqData("opw00001_req", "opw00001", 0, "2001")  # 요청
        helper.block.exec_()  # 이 코드가 있으면 실행이 안됨.

        data.append(GetCommData("opw00001", "", 0, "d+2추정예수금"))
        data.append(GetCommData("opw00018", "", 0, "총매입금액"))
        data.append(GetCommData("opw00018", "", 0, "총평가금액"))
        data.append(GetCommData("opw00018", "", 0, "총평가손익금액"))
        data.append(GetCommData("opw00018", "", 0, "총수익률(%)"))
        data.append(GetCommData("opw00018", "", 0, "추정예탁자산"))

        return data

    if kwargs["조회구분"] == 2:
        return data


def opw00001(helper, **kwargs):
    """계좌평가잔고내역요청
    Args:
        dict: {
            계좌번호: str
            비밀번호: str
            비밀번호입력매체구분: str
            조회구분: str, 3: 추정조회, 2: 일반조회
        }
    Returns:
        IF "조회구분" == 3:
            Return d2_deposit
        ELIF "조회구분" == 2:
        ...
    """
    SetInputValues(kwargs)

    if kwargs["조회구분"] == 3:  # 추정조회
        CommRqData("opw00001_req", "opw00001", 0, "2001")
        helper.block.exec_()
        return GetCommData(helper.trcode, helper.rcname, 0, "d+2추정예수금")
