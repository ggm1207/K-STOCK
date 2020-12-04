"""
    키움 API Method를 모아놓은 모듈. 키움 Method명과 똑같이 camelCase를 사용해서 표기했다.
Usage:
    GetLoginInfo("ACCNO")
"""
from kiwoom.handler import Handler


def SendOrder(
    sRQName,
    sScreenNo,
    sAccNo,
    nOrderType,
    sCode,
    nQty,
    nPrice,
    sHogaGb,
    sOrgOrderNo,
):
    """주식 주문을 서버로 전송한다.
    Args:
        sRQName - 사용자 구분 요청 명
        sScreenNo - 화면번호[4]
        sAccNo - 계좌번호[10]
        nOrderType - 주문유형 (1:신규매수, 2:신규매도, 3:매수취소, 4:매도취소, 5:매수정정, 6:매도정
        정)
        sCode, - 주식종목코드
        nQty – 주문수량
        nPrice – 주문단가
        sHogaGb - 거래구분
        sOrgOrderNo – 원주문번호
    Returns:
        err_code - 에러코드
    """

    err_code = Handler.kiwoom.dynamicCall(
        "SendOrder(QString, QString, QString, int, QString, \
        int, int, QString, QString)",
        [
            sRQName,
            sScreenNo,
            sAccNo,
            nOrderType,
            sCode,
            nQty,
            nPrice,
            sHogaGb,
            sOrgOrderNo,
        ],
    )
    return err_code


def CommRqData(sRQName: str, sTrCode: str, nPrevNext: int, sScreenNo: str):
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
    ret = Handler.kiwoom.dynamicCall(
        "CommRqData(QString, QString, int, QString)",
        sRQName,
        sTrCode,
        nPrevNext,
        sScreenNo,
    )
    return ret


def GetLoginInfo(tag: str):
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
    if tag in [
        "ACCOUNT_CNT",
        "ACCNO",
        "USER_ID",
        "USER_NAME",
        "KEY_BSECGB",
        "FIREW_SECGB",
    ]:
        return Handler.kiwoom.dynamicCall("GetLoginInfo(QString)", tag)
    raise AttributeError("존재하지 않는 태그입니다!")


def GetMasterCodeName(strCode: str):
    """종목코드의 한글명을 반환한다.
    Args:
        strCode[str] - 종목코드
    Returns:
        strName[str] - 종목한글명
    """
    strName = Handler.kiwoom.dynamicCall("GetMasterCodeName(QString)", strCode)
    return strName


def SetInputValue(sID: str, sValue: str):
    """Tran 입력 값을 서버통신 전에 입력한다.
    Args:
        sID[str] – 아이템명
        sValue[str] – 입력 값
    E.G)
        SetInputValue("종목코드", "000660");
        SetInputValue("계좌번호", "5015123401")
    """
    Handler.kiwoom.dynamicCall("SetInputValue(QString, QString)", sID, sValue)


def SetInputValues(sItems: dict):
    """Dict를 입력받아 Key, Id를 SetInputValue를 수행한다.
    Args:
        sItems[dict] - (sId[str], sValue[str])의 형식을 가진 Dict
    E.G)
        SetInputValues({"종목코드": "000660", "계좌번호": "5015123401"})
    """
    for key, value in sItems.items():
        SetInputValue(key, value)


def GetCommData(trCode, rName, nIndex, itemName):
    """수신 데이터를 반환한다, 조회 정보 요청.
    반드시 OnReceiveTRData()이벤트가 호출될때 그 안에서 사용해야 한다.
    Args:
        strTrCode[str] – Tran 코드
        strRecordName[str] – 레코드명
        nIndex[int] – TR 반복부
        strItemName[str] – TR에서 얻어오려는 출력항목 이름
    Returns:
        수신 데이터를 반환한다.
    E.G)
        GetCommData("OPT10001", "주식기본정보", 0, "현재가")
    """
    ret = Handler.kiwoom.dynamicCall(
        "GetCommData(QString, QString, int, QString)",
        trCode,
        rName,
        nIndex,
        itemName,
    )
    return ret.strip()


def GetCommDataEx(sTrCode, strRecordName):
    """차트 조회처럼 반복데이터가 많은 데이터를 한꺼번에 받아서 처리하고 싶을 때 사용한다.
    Args:
        sTrCode[str] - 조회한 TR코드
        strRecordName[str] - 조회한 TR명
    Returns:
        - 배열로 반환 (파이썬에서는 아마 리스트?)
    """
    ret = Handler.kiwoom.dynamicCall(
        "GetCommDataEx(QString, QString)", sTrCode, strRecordName
    )
    return ret


def GetRepeatCnt(sTrCode, sRecordName):
    """
    Args:
        sTrCode[str] - Tran 명
        sRecordName[str] - 레코드 명
    Returns:
        repeat_cnt[int] - 레코드의 반복횟수
    """
    repeat_cnt = Handler.kiwoom.dynamicCall(
        "GetRepeatCnt(QString, QString)", sTrCode, sRecordName
    )
    return int(repeat_cnt)
