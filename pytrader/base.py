# from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGroupBox, QTableWidgetItem

from kiwoom.handler import Handler, Wait
from kiwoom.method import (
    GetLoginInfo,
    GetCommDataEx,
    GetMasterCodeName,
    SendOrder,
)
from kiwoom.transaction.opw import OPW00018, OPW00001

from config.config import password


class ManualOrder(QGroupBox):
    def __init__(self, parent):
        super(QGroupBox, self).__init__(parent)
        self.parent = parent
        self._manual_order_setting()
        self.parent.mo_sendOrder.clicked.connect(self._send_order)

    def _code_changed(self):
        code = self.parent.mo_code.text()
        name = GetMasterCodeName(code)
        self.parent.mo_class.setText(name)

    def _manual_order_setting(self):
        # 계좌
        accounts_num = int(GetLoginInfo("ACCOUNT_CNT"))
        accounts = GetLoginInfo("ACCNO")
        account_list = accounts.split(";")[:accounts_num]
        self.parent.mo_accounts.addItems(account_list)

        # 종목
        self.parent.mo_code.textChanged.connect(self._code_changed)

    def _send_order(self):
        order_type_lookup = {"신규매수": 1, "신규매도": 2, "매수취소": 3, "매도취소": 4}
        hoga_lookup = {"지정가": "00", "시장가": "03"}

        account = self.parent.mo_accounts.currentText()
        order_type = self.parent.mo_order.currentText()
        code = self.parent.mo_code.text()
        hoga = self.parent.mo_hoga.currentText()
        num = self.parent.mo_num.value()
        price = self.parent.mo_price.value()

        SendOrder(
            "send_order_req",
            "0101",
            account,
            order_type_lookup[order_type],
            code,
            num,
            price,
            hoga_lookup[hoga],
            "",
        )


class CurStatus(QGroupBox):
    def __init__(self, parent):
        super(QGroupBox, self).__init__(parent)
        self.parent = parent
        self._balance_setting()
        self._stock_setting()

    def _balance_setting(self):
        """OPW00018, OPW"""
        account = self.parent.mo_accounts.currentText()
        where = "00"  # Kiwoom 서버에서 우리를 구별하기 위해 입력하는 값.
        context = dict(
            {
                "계좌번호": account,
                "비밀번호": password,
                "비밀번호입력매체구분": where,
                "조회구분": 1,
            }  # 합산
        )

        # with Wait(self.parent.block):
            # Handler.run(
                # OPW00018,
                # context,
                # keys=["총매입금액", "총평가금액", "총평가손익금액", "총수익률(%)", "추정예탁자산"],
            # )
            # context["조회구분"] = 3
            # Handler.run(OPW00001, context, keys=["d+2추정예수금"])

        # datas = list()
        # datas += Handler.get(OPW00001)
        # datas += Handler.get(OPW00018)

        # table = self.parent.balanceTable

        # for i, data in enumerate(datas):
            # item = QTableWidgetItem(data)
            # item.setTextAlignment(Qt.AlignVCenter | Qt.AlignCenter)
            # table.setItem(0, i, item)

    def _stock_setting(self):
        """ 내가 가지고 있는 주식 종목 들 """
        account = self.parent.mo_accounts.currentText()
        where = "00"  # Kiwoom 서버에서 우리를 구별하기 위해 입력하는 값.
        context = dict(
            {
                "계좌번호": account,
                "비밀번호": password,
                "비밀번호입력매체구분": where,
                "조회구분": 2,
            }  # 개별
        )

        with Wait(self.parent.block):
            Handler.run(
                OPW00018,
                context,
                keys=["종목명", "보유수량", "매입가", "현재가", "평가손익", "수익률(%)"],
            )

        datas = Handler.get(OPW00018) 


class EventList(QGroupBox):
    def __init__(self, parent):
        super(QGroupBox, self).__init__(parent)
