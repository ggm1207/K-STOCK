from PyQt5.QtCore import QEventLoop
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


class WaitEvent:
    """Context를 활용해서 코드 깔끔하게 작성."""

    def __init__(self, event: QEventLoop):
        self._event = event

    def __enter__(self):
        self._event.exec_()

    def __exit__(self, ext_type, ex_value, ex_traceback):
        pass


class Handler(QAxWidget):
    kiwoom = None
    tr = dict()
    db = dict()
    lock = dict()

    def __new__(cls):
        """딱 한 번만 실행"""
        from kiwoom.transaction.opw import TR

        cls.kiwoom = Kiwoom()
        for c in TR.__subclasses__():
            cls.tr[c.__name__] = c

    @classmethod
    def run(cls, block, tr_classes):
        for tr_cls, context in tr_classes:
            tr_cls.run(**context)
            cls.lock[tr_cls.__name__] = False

        block.exec_()

    @classmethod
    def execute(cls, trcode: str):
        trcode = trcode.upper()
        temp = cls.tr[trcode].execute()
        print("Handler execute: ", temp, trcode)
        cls.db[trcode] = temp
