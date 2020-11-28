import sys

from PyQt5 import uic
from PyQt5.QtCore import QTime, QTimer, QEventLoop
from PyQt5.QtWidgets import QApplication, QMainWindow

from kiwoom.handler import Handler
from pytrader.base import CurStatus, EventList

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
        self.block = QEventLoop()

        # self.setStyleSheet(THEME)
        self.curStatus = CurStatus(self)
        self.eventList = EventList(self)

        self._set_init_widgets()
        # self.OnReceiveTrData.connect(self._on_receive_tr_data)
        # self.OnReceiveChejanData.connect()

    def _on_receive_tr_data(
        self, sScrNo, sRQName, sTrCode, sRecordName, sPrevNext, *args, **kwargs
    ):
        """조회요청 응답을 받거나 조회데이터를 수신했을때 호출됩니다. 조회데이터는 이 이벤트내부에서 GetCommData()함수를 이용해서 얻어올 수 있습니다."""
        self.block.exit()  # TODO: 비동기에서는...?

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
            status = "장 시작 전입니다! \U0001F928"  # faced with raised eyebrow: color
        elif Q_CURTIME > MARKET_END_TIME:
            status = "장 마감... \U0001F644"  # face with rolling eyes: color
        else:
            status = "연결 완료! \U0001F929"  # star-struck: color

            # TODO: Kiwoom Model

        self.statusbar.showMessage(f"{status} | 현재시간: {cur_time}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    kstock = App()
    kstock.show()
    app.exec_()
