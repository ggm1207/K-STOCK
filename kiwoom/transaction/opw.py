from collections import defaultdict

from PyQt5.QtCore import QEventLoop

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
    def __enter__(self):
        self._event = QEventLoop()

    def __exit__(self):
        self._event.exec_()  # _event.exit()이 호출 될때까지 메소드를 블록함.


class OPW00018(Handler):
    """계좌평가잔고내역요청
    Args:
        sAccountNumber - 계좌번호
        sPassword - 비밀번호
        sWhere(00) - 비밀번호입력매체구분
        sGubun - 조회구분
    Returns:
        context: dict -
    """

    def __init__(self):
        self.data = dict()

    def __call__(self, **kwargs):
        SetInputValues(kwargs)
        with WaitEvent:
            CommRqData("OPW00018", "opw00018", 0, "2000")

        if kwargs["sGubun"] == 1:  # 합산
            return self._request_add_up()

        if kwargs["sGubun"] == 2:  # 개별
            return self._request_individual()

        raise AttributeError("sGubun값은 1(합산) 아니면 2(개별)이 되어야 합니다.")

    def _request_add_up(self):
        total_purchase_price = GetCommData("opw00018", "OPW00018", 0, "총매입금액")
        total_eval_price = GetCommData("opw00018", "OPW00018", 0, "총평가금액")
        total_eval_profit_loss_price = GetCommData("opw00018", "OPW00018", 0, "총평가손익금액")
        total_earning_rate = GetCommData("opw00018", "OPW00018", 0, "총수익률(%)")
        estimated_deposit = GetCommData("opw00018", "OPW00018", 0, "추정예탁자산")

    def _request_individual(self):

        return

    @classmethod
    def receive_tr_data(
        cls,
        screen_no,
        rqname,
        trcode,
        record_name,
        next,
        unused1,
        unused2,
        unused3,
        unused4,
    ):
        return


class OPW00001(Handler):
    """계좌평가잔고내역요청
    Args:
        account

    """

    pass

    # def __call__(self):
