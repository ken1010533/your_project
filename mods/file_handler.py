# file_handler.pyw
import pandas as pd
import json

def 保存結果到檔案(資料框架, 查詢結果, 文件路徑, 輸出詳細=False):
    try:
        if 輸出詳細 :
            # 強制使用JSON格式保存詳細資料
            if not 文件路徑.endswith('.json'):
                文件路徑 = 文件路徑.rsplit('.', 1)[0] + '.json'
            
            # 合併所有詳細資料
            詳細資料 = {
                "公司資料": [公司.get("詳細資料", {}) for 公司 in 查詢結果.get("公司資料", [])],
                "企業社商行資料": [商行.get("詳細資料", {}) for 商行 in 查詢結果.get("企業社商行資料", [])],
                "其他資料": 查詢結果.get("其他資料", []),
            }
             
            with open(文件路徑, "w", encoding="utf-8") as 檔案:
                json.dump(詳細資料, 檔案, ensure_ascii=False, indent=4)
            return True, f"詳細結果已保存到 {文件路徑}"
        
        # 正常保存流程
        if 文件路徑.endswith('.xlsx'):
            # 格式化日期欄位（如果存在）
            日期欄位 = ["派發日期", "上次派發", "出進口申請", "出進口核發"]
            for 欄位 in 日期欄位:
                if 欄位 in 資料框架.columns:
                    資料框架[欄位] = pd.to_datetime(資料框架[欄位], errors='coerce').dt.strftime('%Y-%m-%d')
            
            # 保存 Excel
            with pd.ExcelWriter(文件路徑) as 寫入器:
                資料框架.to_excel(寫入器, sheet_name="工作表1", index=False)
                if 查詢結果.get("公司資料"):
                    pd.DataFrame(查詢結果["公司資料"]).to_excel(寫入器, sheet_name="公司資料", index=False)
                
                if 查詢結果.get("企業社商行資料"):
                    pd.DataFrame(查詢結果["企業社商行資料"]).to_excel(寫入器, sheet_name="企業社商行資料", index=False)
                
                if 查詢結果.get("其他資料"):
                    pd.DataFrame(查詢結果["其他資料"], columns=["名稱", "縣市", "統一編號"]).to_excel(寫入器, sheet_name="其他資料", index=False)
        else:
            with open(文件路徑, "w", encoding="utf-8") as 檔案:
                json.dump(查詢結果, 檔案, ensure_ascii=False, indent=4)
        return True, f"結果已保存到 {文件路徑}"
    except Exception as 錯誤:
        return False, f"儲存檔案時發生錯誤: {str(錯誤)}",print(f"儲存檔案時發生錯誤: {str(錯誤)}")


def 詳細保存(資料框架, 查詢結果, 文件路徑):
    try:
        if 資料框架.empty:
            return False, "查詢結果為空，無法保存。"
        
        if 資料框架.shape[0] > 10000:
            return False, "查詢結果過大，無法保存。"
        
        # 確保使用JSON格式
        if not 文件路徑.endswith('.json'):
            文件路徑 = 文件路徑.rsplit('.', 1)[0] + '.json'  # 修正變數名稱
        
        # 儲存結果到檔案
        成功, 訊息 = 保存結果到檔案(資料框架, 查詢結果, 文件路徑, 輸出詳細=True)
        return 成功, 訊息
    except Exception as 錯誤:
        return False, f"儲存詳細資料時發生錯誤: {str(錯誤)}",print(f"儲存詳細資料時發生錯誤: {str(錯誤)}")