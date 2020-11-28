from kiwoom.handler import Handler


class CommRqData(Handler):
    """Tran을 서버로 송신한다
    Args:
        BSTR sRQName - 사용자구분 명
        BSTR sTrCode - Tran명 입력
        long nPrevNext - 0: 조회, 2: 연속
        BSTR sScreenNo - 4자리의 화면번호, 요청을 구별하기 위한 키값 0000을 제외한 임의의 숫자를 사용.
        ( 200개 제한 )
    Returns:
        OP_ERR_SISE_OVERFLOW – 과도한 시세조회로 인한 통신불가
        OP_ERR_RQ_STRUCT_FAIL – 입력 구조체 생성 실패
        OP_ERR_RQ_STRING_FAIL – 요청전문 작성 실패
        OP_ERR_NONE – 정상처리
    """

    def __call__(self, sRQName: str, sTrCode: str, nPrevNext: int, sScreenNo: str):
        return


class GetLoginInfo(Handler):
    """로그인한 사용자 정보를 반환한다
    Args:
        BSTR sTag : 사용자 정보 구분 TAG값 (비고)
        BSTR sTag에 들어 갈 수 있는 값은 아래와 같음
        - `ACCOUNT_CNT` – 전체 계좌 개수를 반환한다.
        - `ACCNO` – 전체 계좌를 반환한다. 계좌별 구분은 ‘;’이다.
        - `USER_ID` - 사용자 ID를 반환한다.
        - `USER_NAME` – 사용자명을 반환한다.
        - `KEY_BSECGB` – 키보드보안 해지여부. 0:정상, 1:해지
        - `FIREW_SECGB` – 방화벽 설정 여부. 0:미설정, 1:설정, 2:해지
    Returns:
        TAG값에 따른 데이터 반환
    """

    def __call__(self, tag: str):
        if tag in [
            "ACCOUNT_CNT",
            "ACCNO",
            "USER_ID",
            "USER_NAME",
            "KEY_BSECGB",
            "FIREW_SECGB",
        ]:
            return self.kiwoom.dynamicCall(tag)
        raise AttributeError("존재하지 않는 태그입니다!")


class SetInputValue(Handler):
    """Tran 입력 값을 서버통신 전에 입력한다.
    Args:
        sID – 아이템명
        sValue – 입력 값
    E.G)
        SetInputValue("종목코드", "000660");
        SetInputValue("계좌번호", "5015123401")
    """

    def __call__(self, sID: str, sValue: str):
        self.dynamicCall("SetInputValue(QString, QString)", sID, sValue)


class SetInputValues(Handler):
    """Dict를 입력받아 Key, Id를 SetInputValue를 수행한다.
    Args:
        sItems - (sId, sValue)의 형식을 가진 Dict
    E.G)
        SetInputValues({"종목코드": "000660", "계좌번호": "5015123401"})
    """

    def __call__(self, sItems: dict):
        for key, value in sItems.items():
            SetInputValue(key, value)


class GetCommData(Handler):
    """수신 데이터를 반환한다, 조회 정보 요청.
    반드시 OnReceiveTRData()이벤트가 호출될때 그 안에서 사용해야 한다.
    Args:
        strTrCode – Tran 코드
        strRecordName – 레코드명
        nIndex – TR 반복부
        strItemName – TR에서 얻어오려는 출력항목 이름
    Returns:
        OnReceiveTRData에서 처리된다.
    E.G)
        GetCommData("OPT10001", "주식기본정보", 0, "현재가")
    """


class GetCommDataEx(Handler):
    """차트 조회처럼 반복데이터가 많은 데이터를 한꺼번에 받아서 처리하고 싶을 때 사용한다.
    Args:

    """

    pass
