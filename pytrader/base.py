from PyQt5 import uic
from PyQt5.QtWidgets import QGroupBox


class CurStatus(QGroupBox):
    def __init__(self, parent):
        super(QGroupBox, self).__init__(parent)
        self._accounts_setting()

    def _accounts_setting(self):
        from kiwoom.method import GetLoginInfo, CommRqData

        accounts_num = int(GetLoginInfo("ACCOUNT_CNT"))
        accounts = GetLoginInfo("ACCNO")
        print(accounts_num)
        print(accounts)
        account_list = accounts.split(";")[:accounts_num]
        self.accounts.addItems(account_list)

    def _balance_setting(self):
        from kiwoom.transaction.opw import OPW00018
        df = OPW00018

    def _stock_setting(self):
        pass

class EventList(QGroupBox):
    def __init__(self, parent):
        super(QGroupBox, self).__init__(parent)
    
