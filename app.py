import sys

from PyQt5 import uic
from PyQt5.QtCore import QTime, QTimer, QEventLoop
from PyQt5.QtWidgets import QApplication, QMainWindow

from kiwoom.handler import Handler
from pytrader.base import CurStatus, EventList, ManualOrder

UIPATH = "./view/app.ui"
THEME = "./view/white.css"
ONE_SECOND = 1000

UI = uic.loadUiType(UIPATH)[0]
MARKET_START_TIME = QTime(9, 0, 0)
MARKET_END_TIME = QTime(15, 30, 0)


class App(QMainWindow, UI):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        Handler()  # QWidget Init After QApplication
        self._event_connect()

        self.block = QEventLoop()
        Handler.kiwoom.init(self.block)

        # self.setStyleSheet(THEME)
        self.manualOrder = ManualOrder(self)
        self.curStatus = CurStatus(self)
        self.eventList = EventList(self)

        self._set_init_widgets()

    def _event_connect(self):
        Handler.kiwoom.OnEventConnect.connect(self._on_event_connect)
        Handler.kiwoom.OnReceiveTrData.connect(self._on_receive_tr_data)
        Handler.kiwoom.OnReceiveChejanData.connect(
            self._on_receive_chejan_data
        )

    def _on_event_connect(self, err_code):
        msg = "connected"
        if err_code != 0:
            msg = "disconnected"

        print(msg)
        self.block.exit()

    def _on_receive_tr_data(
        self, sScrNo, sRQName, sTrCode, sRecordName, sPrevNext, *args, **kwargs
    ):
        print("in event", sScrNo, sTrCode)
        print(sRQName, sTrCode)

        if sTrCode.startswith("op"):
            Handler.get_values(sTrCode)

        if all(Handler.lock.values()):  # 그리 큰
            self.block.exit()  # TODO: 비동기에서는...?

    def _on_receive_chejan_data(self, gubun, item_cnt, fid_list):
        """ 주문체결 데이터를 출력할 UI가 존재하지 않으므로... """
        print("gubun:", gubun)
        print(123124124)
        print(123124124)
        print(123124124)
        print(123124124)

    def _set_init_widgets(self):
        # 서버와의 연결을 확인하는 Timer
        self._check_connected()
        self.check_connected_timer = QTimer(self)
        self.check_connected_timer.start(ONE_SECOND)
        self.check_connected_timer.timeout.connect(self._check_connected)

    def _check_connected(self):
        status = ""
        Q_CURTIME = QTime.currentTime()
        cur_time = Q_CURTIME.toString("hh:mm:ss")

        if Q_CURTIME < MARKET_START_TIME:
            # faced with raised eyebrow: color
            status = "장 시작 전입니다! \U0001F928"
        elif Q_CURTIME > MARKET_END_TIME:
            # face with rolling eyes: color
            status = "장 마감... \U0001F644"
        else:
            # star-struck: color
            status = "연결 완료! \U0001F929"

            # TODO: Kiwoom Model

        self.statusbar.showMessage(f"{status} | 현재시간: {cur_time}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    kstock = App()
    kstock.show()
    app.exec_()
