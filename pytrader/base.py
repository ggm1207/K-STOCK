from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGroupBox, QTableWidgetItem

from kiwoom.transaction.opw import opw00018
from kiwoom.method import GetLoginInfo, CommRqData


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
        password = "340978"  # TODO: 계좌별 비밀번호를 불러오도록 수정
        where = "00"  # Kiwoom 서버에서 우리를 구별하기 위해 입력하는 값.
        context = dict(
            {"계좌번호": account, "비밀번호": password, "비밀번호입력매체구분": where, "조회구분": 1}  # 합산
        )

        # 잔고 조회
        data = opw00018(self.parent.helper, **context)
        table = self.parent.balanceTable
        item = QTableWidgetItem("0")
        item.setTextAlignment(Qt.AlignVCenter | Qt.AlignCenter)
        table.setItem(0, 0, item)

        for i in range(1, 6):
            item = QTableWidgetItem(data[i-1])
            item.setTextAlignment(Qt.AlignVCenter | Qt.AlignCenter)
            table.setItem(0, i, item)

        # 종목 조회
        # context["조회구분"] = 2  # 개별
        # data = OPW00018(context)

    def _stock_setting(self):
        pass


class EventList(QGroupBox):
    def __init__(self, parent):
        super(QGroupBox, self).__init__(parent)
