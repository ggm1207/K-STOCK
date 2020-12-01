# from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGroupBox, QTableWidgetItem

from kiwoom.transaction.opw import OPW00018, OPW00001
from kiwoom.method import GetLoginInfo


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
        password = "0000"  # TODO: 계좌별 비밀번호를 불러오도록 수정
        where = "00"  # Kiwoom 서버에서 우리를 구별하기 위해 입력하는 값.
        context = dict(
            {
                "계좌번호": account,
                "비밀번호": password,
                "비밀번호입력매체구분": where,
                "조회구분": 1,
            }  # 합산
        )

        # 잔고 조회
        OPW00018.run(context)
        context["조회구분"] = 3
        OPW00001.run(context)

        self.parent.helper.block.exec_()

        data = list()
        data += OPW00001.get()
        data += OPW00018.get()

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
