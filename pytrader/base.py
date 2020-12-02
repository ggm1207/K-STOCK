# from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGroupBox, QTableWidgetItem

from kiwoom.handler import Handler, Wait
from kiwoom.method import GetLoginInfo
from kiwoom.transaction.opw import OPW00018, OPW00001

from config.config import password


class CurStatus(QGroupBox):
    def __init__(self, parent):
        super(QGroupBox, self).__init__(parent)
        self.parent = parent
        self._accounts_setting()
        self._balance_setting()

    def _accounts_setting(self):
        accounts_num = int(GetLoginInfo("ACCOUNT_CNT"))
        accounts = GetLoginInfo("ACCNO")
        account_list = accounts.split(";")[:accounts_num]
        self.parent.accounts.addItems(account_list)

    def _balance_setting(self):
        """OPW00018, OPW"""
        account = self.parent.accounts.currentText()
        where = "00"  # Kiwoom 서버에서 우리를 구별하기 위해 입력하는 값.
        opw00018_context = dict(
            {
                "계좌번호": account,
                "비밀번호": password,
                "비밀번호입력매체구분": where,
                "조회구분": 1,
            }  # 합산
        )

        # 잔고 조회
        # opw00001_context = opw00018_context.copy()
        # opw00001_context["조회구분"] = 3
        context = opw00018_context.copy()

        with Wait(self.parent.block):
            Handler.run(
                OPW00018,
                context,
                keys=["총매입금액", "총평가금액", "총평가손익금액", "총수익률(%)", "추정예탁자산"],
            )
            context["조회구분"] = 3
            Handler.run(OPW00001, context, keys=["d+2추정예수금"])

        # data = Handler.get_values(OPW00018, keys = ["가", "나"])

        # Handler.run(
        # self.parent.helper.block,
        # [(OPW00001, opw00001_context), (OPW00018, opw00018_context)],
        # )

        data = list()
        data += Handler.get_values(OPW00018)
        data += Handler.get_values(OPW00001)

        print("data:", data)

        table = self.parent.balanceTable

        for i in range(6):
            print(f"data {i}:", data[i], end=" ")
            item = QTableWidgetItem(data[i])
            item.setTextAlignment(Qt.AlignVCenter | Qt.AlignCenter)
            table.setItem(0, i, item)

    def _stock_setting(self):
        """ 아직 방법 생각 중.. """
        pass


class EventList(QGroupBox):
    def __init__(self, parent):
        super(QGroupBox, self).__init__(parent)
