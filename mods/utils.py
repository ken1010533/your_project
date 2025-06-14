import pandas as pd
import re
from math import nan

def 判斷公司類型(名稱):
    if pd.isna(名稱):
        return nan
    名稱 = str(名稱)
    if "公司" in 名稱:
        return "公司"
    elif "社" in 名稱:
        return "社" 
    elif "行" in 名稱:
        return "行"
    elif "廠" in 名稱:
        return "廠"
    elif "事業" in 名稱:
        return "事業"
    elif "實業" in 名稱:
        return "實業"
    elif "坊" in 名稱:
        return "坊"
    else:
        return "無"

def 提取縣市(地址):
    if not isinstance(地址, str):
        return "未知"
    
    # 替換常見錯字
    地址 = 地址.replace("臺", "台").replace("巿", "市")
    
    模式 = r"(台北市|新北市|桃園市|台中市|台南市|高雄市|基隆市|新竹市|嘉義市|新竹縣|苗栗縣|彰化縣|南投縣|雲林縣|嘉義縣|屏東縣|宜蘭縣|花蓮縣|台東縣|澎湖縣|金門縣|連江縣)"
    匹配 = re.search(模式, 地址)
    if 匹配:
        return 匹配.group(1).replace("台", "臺")
    return "未知"

def 取得營業狀態(狀態):
    if pd.isna(狀態) or 狀態 in ["無資料", None, ""]:
        return "查無結果"
    狀態 = str(狀態).strip()
    # return 狀態
    if any(關鍵字 in 狀態 for 關鍵字 in ["營業中", "營運中", "復業","副業副本","許可","核准設立","延展開業"]):
        return "營業中"
    elif any(關鍵字 in 狀態 for 關鍵字 in [  "解散", "廢止", "停業", "撤銷",
                                            "重整","解散","撤銷",
                                            "破產","合併解散","撤回認許","廢止","廢止認許",
                                            "解散已清算完結","撤銷已清算完結","廢止已清算完結",
                                            "撤回認許已清算完結","撤銷認許已清算完結","廢止認許已清算完結",
                                            "撤銷認許分割解散","終止","破產中止","破產塗銷",
                                            "破產","破產程序終結(終止)","破產程序終結(終止)清算中",
                                            "破產已清算完結","接管","撤銷無需清算",
                                            "撤銷許可","廢止許可","撤銷許可已清算完結",
                                            "廢止許可已清算完結","清理撤銷公司設立","清理完結"
                                             "歇業", "停業中","停業副本","破產"]):
        return "非營業中"
    else:
        return 狀態
