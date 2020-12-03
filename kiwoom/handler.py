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
            cls.tr[tr_sub_class.trcode] = tr_sub_class

    @classmethod
    def run(cls, tr_class, context: dict, keys: list):
        tr_class.run(**context)
        cls.lock[tr_class.trcode] = False
        cls.keys[tr_class.trcode] = keys
        print(tr_class.trcode, ": run!")

    @classmethod
    def get_values(cls, trcode):
        temp = cls.tr[trcode].get_multi_values(cls.keys[trcode])
        # trcode = trcode.upper()
        # temp = cls.tr[trcode].execute()
        cls.db[trcode] = temp
        cls.lock[trcode] = True

    @classmethod
    def get(cls, tr_class):
        return cls.db[tr_class.trcode]
