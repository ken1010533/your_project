import pandas as pd
from .utils import 判斷公司類型, 提取縣市

def 分析Excel文件(filepath):
    資料框架 = pd.read_excel(filepath)
    
    # 檢查必要欄位
    必要欄位 = ["公司名稱", "公司地址", "統一編號"]
    for 欄位 in 必要欄位:
        if 欄位 not in 資料框架.columns:
            raise ValueError(f"找不到必要欄位『{欄位}』")
    
    # 判斷公司類型與提取縣市
    資料框架["公司類型"] = 資料框架["公司名稱"].apply(判斷公司類型)
    資料框架["縣市"] = 資料框架["公司地址"].apply(提取縣市)
    
    # 初始化「是否營業」欄位
    if "是否營業" not in 資料框架.columns:
        資料框架.insert(0, "是否營業", "尚未查詢")
    else:
        col = 資料框架.pop("是否營業")
        資料框架.insert(0, "是否營業", col)
    
    # 根據「公司類型」分類
    公司列表 = []
    商行列表 = []
    其他列表 = []
    
    for _, row in 資料框架.iterrows():
        類型 = row["公司類型"]
        名稱 = row["公司名稱"]
        統編 = row.get("統一編號", "")
        縣市 = row["縣市"]
        
        if 類型 in ["公司", "事業", "實業"]:
            公司列表.append((名稱, 縣市, 統編))
        elif 類型 in ["社", "行", "廠", "坊"]:
            商行列表.append((名稱, 縣市, 統編))
        elif pd.isna(類型) or 類型 == "無":
            其他列表.append((名稱, 縣市, 統編))
    
    return 資料框架, 公司列表, 商行列表, 其他列表
