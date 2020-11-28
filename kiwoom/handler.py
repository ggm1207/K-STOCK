from PyQt5.QtCore import QEventLoop
from PyQt5.QAxContainer import QAxWidget

class Kiwoom(QAxWidget):
    """Kiwoom API
    server - 1: 모의서버, 나머지: 실서버
    """
    def __init__(self):
        print("Kiwoom Open")
        super().__init__()
        self.setControl("KHOPENAPI.KHOpenAPICtrl.1")
        print("Kiwoom Giant")
        self.dynamicCall("CommConnect()")
        print("Kiwoom HollyShit")
        self.login_event_loop = QEventLoop()
        print("Kiwoom Helpme")
        self.login_event_loop.exec_()

        print("before server check" * 100)
        self.server = self.dynamicCall("KOA_Functions(QString, QString)", "GetServerGubun", "")
        print("GGGG Open" * 100)

    def _event_connect(self, err_code):
        if err_code == 0:
            print("connected")
        else:
            print("disconnected")

        self.login_event_loop.exit()
        
class Handler(QAxWidget):
    print("Handler Before")
    kiwoom = Kiwoom()
    print("Handler After")
