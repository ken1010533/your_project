# query_services.py
import requests
import pandas as pd
import time
from .Save_Profile import 讀取設定

設定 = 讀取設定()
時間延遲 = 設定.get("時間延遲", 1)
print("時間延遲:", 時間延遲)
暫停查詢=設定.get("暫停",1)
print("暫停查詢:", 暫停查詢)
def 查詢公司資料(公司列表, text_callback=None):
    結果 = []
    設定 = 讀取設定()
    顯示查詢網址 = 設定.get("顯示查詢網址", 0)  # 從設定取得顯示網址選項
    while 設定.get("暫停",1):
        設定 = 讀取設定()
        time.sleep(1)
        print("暫停中")
    else:
            pass
    for 名稱, 縣市, 統編 in 公司列表:
        if not 統編 or pd.isna(統編):
            if text_callback:
                text_callback(f"⚠️ {名稱} 缺少統一編號，跳過查詢\n")
            continue
        設定 = 讀取設定()
        網址 = f"https://data.gcis.nat.gov.tw/od/data/api/5F64D864-61CB-4D0D-8AD9-492047CC1EA6?$format=json&$filter=Business_Accounting_NO eq {str(int(float(統編)))}"
        設定 = 讀取設定()
        時間延遲 = 設定.get("時間延遲", 1)
        time.sleep(時間延遲)
        if 設定.get("顯示查詢網址",1):
            print(網址)
            設定 = 讀取設定()
        else:
            設定 = 讀取設定()

        try:
            回應 = requests.get(網址, timeout=10)
            if 回應.status_code == 200:
                資料 = 回應.json()
                if 資料:
                    for 項目 in 資料:
                        營業狀態 = 項目.get("Case_Status_Desc", "無資料") or "無資料"
                        資本額 = 項目.get("Paid_In_Capital_Amount", 0)
                        if 資本額 in [None, ""]:
                            資本額 = 0
                        elif isinstance(資本額, str):
                            資本額 = int(資本額) if 資本額.isdigit() else 0
                        負責人 = 項目.get("Responsible_Name", "無資料") or "無資料"
                        
                        結果項目 = {
                            "名稱": 項目.get("Company_Name", "無資料"),
                            "統編": 項目.get("Business_Accounting_NO", "無資料"),
                            "縣市": 縣市,
                            "資本額": 資本額,
                            "營業狀態描述": 營業狀態,
                            "負責人": 負責人,
                            "網址": 網址
                        }
                        
                        # 只有當顯示查詢網址選項開啟時才包含詳細資料
                        if 顯示查詢網址 == 1:
                            詳細資料 = 項目.copy()
                            詳細資料["查詢網址"] = 網址
                            結果項目["詳細資料"] = 詳細資料
                        
                        結果.append(結果項目)
                        
                        if text_callback:
                            text_callback(f"✅ {名稱} ({縣市}) 查詢成功\n")
                else:
                    if text_callback:
                        text_callback(f"⚠️ 統編 {統編} 無查詢結果\n")
            else:
                if text_callback:
                    text_callback(f"❌ {名稱} 查詢失敗 (HTTP {回應.status_code})\n")
        except Exception as 錯誤:
            if text_callback:
                text_callback(f"❌ {名稱} 查詢錯誤: {str(錯誤)}\n")
    
    return 結果

def 查詢商行資料(商行列表, 地區代碼表, text_callback=None):
    結果 = []
    設定 = 讀取設定()
    顯示查詢網址 = 設定.get("顯示查詢網址", 0)  # 從設定取得顯示網址選項
    顯示查詢網址 = 設定.get("顯示查詢網址", 0)  # 從設定取得顯示網址選項
    while 設定.get("暫停",1):
        設定 = 讀取設定()
        time.sleep(1)
        print("暫停中")   
    for 名稱, 縣市, 統編 in 商行列表:
        if not 統編 or pd.isna(統編):
            if text_callback:
                text_callback(f"⚠️ {名稱} 缺少統一編號，跳過查詢\n")
            continue
        
        地區代碼 = 地區代碼表.get(縣市, "376430000A")
        網址 = f"https://data.gcis.nat.gov.tw/od/data/api/7E6AFA72-AD6A-46D3-8681-ED77951D912D?$format=json&$filter=President_No eq {統編} and Agency eq {地區代碼}&$skip=0&$top=50"
        設定 = 讀取設定()
        時間延遲 = 設定.get("時間延遲", 1)
        time.sleep(時間延遲)
        if 設定.get("顯示查詢網址",1):
            print(網址)
            設定 = 讀取設定()
        else:
            設定 = 讀取設定()
        try:
            回應 = requests.get(網址, timeout=10)
            if 回應.status_code == 200:
                資料 = 回應.json()
                if 資料:
                    for 項目 in 資料:
                        營業狀態 = 項目.get("Business_Current_Status_Desc", "無資料") or "無資料"
                        資本額 = 項目.get("Business_Register_Funds", 0)
                        if 資本額 in [None, ""]:
                            資本額 = 0
                        elif isinstance(資本額, str):
                            資本額 = int(資本額) if 資本額.isdigit() else 0
                        負責人 = 項目.get("Responsible_Name", "無資料") or "無資料"
                        
                        結果項目 = {
                            "名稱": 項目.get("Business_Name", "無資料"),
                            "統編": 項目.get("President_No", "無資料"),
                            "縣市": 縣市,
                            "地區代碼": 地區代碼,
                            "資本額": 資本額,
                            "營業狀態描述": 營業狀態,
                            "負責人": 負責人,
                            "網址": 網址
                        }
                        
                        # 只有當顯示查詢網址選項開啟時才包含詳細資料
                        if 顯示查詢網址 == 1:
                            詳細資料 = 項目.copy()
                            詳細資料["查詢網址"] = 網址
                            結果項目["詳細資料"] = 詳細資料
                        
                        結果.append(結果項目)
                        
                        if text_callback:
                            text_callback(f"✅ {名稱} ({縣市}) 查詢成功\n")
                else:
                    if text_callback:
                        text_callback(f"⚠️ 統編 {統編} 無查詢結果 (地區: {縣市})\n")
            else:
                if text_callback:
                    text_callback(f"❌ {名稱} 查詢失敗 (HTTP {回應.status_code}, 地區: {縣市})\n")
        except Exception as 錯誤:
            if text_callback:
                text_callback(f"❌ {名稱} 查詢錯誤: {str(錯誤)} (地區: {縣市})\n")
    
    return 結果