from PyQt5.QtCore import QEventLoop
from PyQt5.QAxContainer import QAxWidget


class Kiwoom(QAxWidget):
    """Kiwoom API
    self.server - 1: 모의서버, 나머지: 실서버
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


class Wait:
    """Context를 활용해서 코드 깔끔하게 작성."""

    def __init__(self, event: QEventLoop):
        self._event = event

    def __enter__(self):
        pass

    def __exit__(self, ext_type, ex_value, ex_traceback):
        self._event.exec_()


class Handler(QAxWidget):
    kiwoom = None
    tr = dict()
    db = dict()
    keys = dict()
    lock = dict()

    def __new__(cls):
        """딱 한 번만 실행"""
        from kiwoom.transaction.opw import TR

        cls.kiwoom = Kiwoom()

        for tr_sub_class in TR.__subclasses__():
            cls.tr[tr_sub_class.window] = tr_sub_class

    @classmethod
    def run(cls, tr_class, context: dict, keys: list):
        tr_class.run(**context)
        cls.lock[tr_class.window] = False
        cls.keys[tr_class.window] = keys
        print(tr_class.window, ": run!")

    @classmethod
    def get_values(cls, window):
        temp = cls.tr[window].get_values(cls.keys[window])
        # window = window.upper()
        # temp = cls.tr[window].execute()
        cls.db[window] = temp
        cls.lock[window] = True

    @classmethod
    def get(cls, tr_class):
        return cls.db[tr_class.window]
