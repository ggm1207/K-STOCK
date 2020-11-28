from PyQt5 import uic
from PyQt5.QtWidgets import QGroupBox


class CurStatus(QGroupBox):
    def __init__(self, parent):
        super(QGroupBox, self).__init__(parent)
        self._accounts_setting()

    def _accounts_setting(self):
        print("golden bro" * 100)
        from kiwoom.method import GetLoginInfo, CommRqData

        print("gg bro" * 100)
        accounts_num = GetLoginInfo("ACCOUNT_CNT")
        print("accounts_num!" * 100)
        accounts = GetLoginInfo("ACCNO")
        print("accounts!" * 100)
        account_list = accounts.split(";")[:accounts_num]
        print("accounts_list!")
        self.accounts.addItems(account_list)

    def _balance_setting(self):
        from kiwoom.transaction.opw import OPW00018
        df = OPW00018

    def _stock_setting(self):
        pass

class EventList(QGroupBox):
    def __init__(self, parent):
        super(QGroupBox, self).__init__(parent)
    
