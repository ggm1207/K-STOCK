from PyQt5.QAxContainer import QAxWidget


class Kiwoom(QAxWidget):
    """Kiwoom API
    server - 1: 모의서버, 나머지: 실서버
    """

    def __init__(self):
        super().__init__()
        self.setControl("KHOPENAPI.KHOpenAPICtrl.1")

    def init(self, block):
        self.dynamicCall("CommConnect()")
        block.exec_()
        self.server = self.dynamicCall(
            "KOA_Functions(QString, QString)", "GetServerGubun", ""
        )


class Handler(QAxWidget):
    kiwoom = None

    def __new__(cls):
        """딱 한 번만 실행"""
        cls.kiwoom = Kiwoom()
