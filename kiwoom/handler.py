from PyQt5.QtCore import QEventLoop
from PyQt5.QAxContainer import QAxWidget

class Kiwoom(QAxWidget):
    """Kiwoom API
    server - 1: 모의서버, 나머지: 실서버
    """
    def __init__(self):
        super().__init__()
        self.setControl("KHOPENAPI.KHOpenAPICtrl.1")
        self.dynamicCall("CommConnect()")
        self.login_event_loop = QEventLoop()
        self.login_event_loop.exec_()

        self.server = self.dynamicCall("KOA_Functions(QString, QString)", "GetServerGubun", "")

class Handler(QAxWidget):
    kiwoom = Kiwoom()
