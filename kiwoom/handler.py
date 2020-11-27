from PyQt5.QAxContainer import QAxWidget

class Handler:
    self = QAxWidget.setControl("KHOPENAPI.KHOpenAPICtrl.1")
    def __init__(self):
        self.dynamicCall("CommConnect()")
