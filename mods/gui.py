import tkinter as tk
from tkinter import messagebox, filedialog
import datetime
# import pandas as pd
from .excel_parser import 分析Excel文件
from .query_services import 查詢公司資料, 查詢商行資料
from .file_handler import 保存結果到檔案 , 詳細保存
from .Save_Profile import  寫入設定, 讀取設定
from .utils import 取得營業狀態
import threading
from tkinter import ttk
from pathlib import Path 
from .Windows_to_Middle_Module import 主視窗至中
import os
class 公司查詢系統GUI:
    # 地區代碼對照表
    地區代碼表 = {
        "臺北市": "379100000G", "新北市": "376410000A", "桃園市": "376430000A",
        "臺中市": "376590000A", "臺南市": "376610000A", "高雄市": "383100000G",
        "基隆市": "376570000A", "新竹市": "376580000A", "嘉義市": "376600000A",
        "新竹縣": "376440000A", "苗栗縣": "376450000A", "彰化縣": "376470000A",
        "南投縣": "376480000A", "雲林縣": "376490000A", "嘉義縣": "376500000A",
        "屏東縣": "376530000A", "宜蘭縣": "376420000A", "花蓮縣": "376550000A",
        "臺東縣": "376540000A", "澎湖縣": "376560000A", "金門縣": "371010000A",
        "連江縣": "371030000A"
    }
    
    def __init__(self, 根視窗):
        self.根視窗 = 根視窗
        self.根視窗.title("公司/商行查詢系統")
        主視窗至中(self.根視窗)


        self.桌面路徑 = str(Path.home() / "Desktop")
        self.設定 = 讀取設定()

        # 初始化输出位置变量
        默认输出位置 = self.設定.get("詳細輸出檔案位置", self.桌面路徑)
        self.輸出位置變數 = tk.StringVar(value=默认输出位置)
        
        # 其他按鈕和狀態變數初始化
        self.查詢按鈕 = None
        self.保存按鈕 = None
        self.分析Excel按鈕 = None
        self.單筆縣市 = None
        self.記住我變數 = tk.IntVar(value=int(self.設定.get("記住我", 0)))
        self.登入狀態變數 = tk.IntVar(value=0)
        self.記住我變數 = tk.IntVar(value=int(self.設定.get("記住我", 0)))
        self.登入帳號 = self.設定.get("使用者名稱", "")
        self.登入密碼 = self.設定.get("密碼", "")
        self.暫停參數 =self.設定.get("暫停",1)












        self.初始化介面()












    def 初始化介面(self):

        self.根視窗.protocol("WM_DELETE_WINDOW", self.設定功能區)
        框架 = tk.Frame(self.根視窗, padx=10, pady=10)
        框架.pack()
        notebook = ttk.Notebook(框架)
        notebook.pack(fill="both", expand=True)
        # 標籤頁
        查詢系統 = ttk.Frame(notebook)
        其他功能 = ttk.Frame(notebook)
        notebook.add(查詢系統, text="批量查詢系統")
        notebook.add(其他功能, text="單筆查詢/其他功能")








        商業司分頁 = ttk.Frame(notebook)
        notebook.add(商業司分頁, text="商業司網址設定")
        # 強化分頁切換事件
        notebook.bind("<<NotebookTabChanged>>", lambda e: self.處理分頁(e))

        self.登入狀態變數 = tk.IntVar(value=0)
        self.登入框架 = tk.Frame(商業司分頁)  # 確保商業司分頁框架有設置
        self.登入框架.pack(padx=10, pady=10, fill="both", expand=True)
        self.顯示登入介面()
        self.登入狀態變數 = tk.IntVar(value=0)
        self.記住我變數 = tk.IntVar(value=int(self.設定.get("記住我", 0)))
        self.登入帳號 = self.設定.get("使用者名稱", "")
        self.登入密碼 = self.設定.get("密碼", "")



        # 文件選擇區段
        文件框架 = tk.LabelFrame(查詢系統, text="1. 選擇Excel文件", padx=5, pady=5)
        文件框架.pack(fill="x", pady=5)
        self.文件路徑 = tk.StringVar()
        tk.Label(文件框架, text="文件路徑:").pack(side="left")
        tk.Entry(文件框架, textvariable=self.文件路徑, width=50).pack(side="left", padx=5)
        tk.Button(文件框架, text="瀏覽...", command=self.選擇文件).pack(side="left")
        
        # 操作按鈕
        按鈕框架 = tk.Frame(查詢系統)
        按鈕框架.pack(pady=10)
        self.分析Excel按鈕=tk.Button(按鈕框架, text="分析Excel", command=self.分析Excel)
        self.分析Excel按鈕.pack(side="left", padx=5)
        # 修改：保存查詢按鈕引用
        self.查詢按鈕 = tk.Button(按鈕框架, text="查詢資料", command=self.查詢資料)
        self.查詢按鈕.pack(side="left", padx=5)
        # 修改：保存保存按鈕引用
        self.保存按鈕 = tk.Button(按鈕框架, text="保存結果", command=self.重新儲存)
        self.保存按鈕.pack(side="left", padx=5)
        self.暫停按鈕=tk.Button(按鈕框架, text="暫停",command=self.暫停 )
        self.暫停按鈕.pack(side="left", padx=5)
        self.暫停()
        tk.Button(按鈕框架, text="退出", command=self.安全退出).pack(side="left", padx=5)



        # 結果顯示區
        結果框架 = tk.LabelFrame(查詢系統, text="查詢結果", padx=5, pady=5)
        結果框架.pack(fill="both", expand=True, pady=5)
        self.結果文字 = tk.Text(結果框架, width=80, height=20)
        滾動條 = tk.Scrollbar(結果框架, command=self.結果文字.yview)
        self.結果文字.configure(yscrollcommand=滾動條.set)
        self.結果文字.pack(side="left", fill="both", expand=True)
        滾動條.pack(side="right", fill="y")
        
        # 狀態欄
        self.狀態變數 = tk.StringVar()
        self.狀態變數.set("準備就緒")
        tk.Label(框架, textvariable=self.狀態變數, bd=1, relief=tk.SUNKEN, anchor=tk.W).pack(fill="x")

        # 進度條
        self.進度條 = ttk.Progressbar(查詢系統, orient="horizontal", length=400, mode="determinate")
        self.進度條.pack(pady=5)
        self.進度條["value"] = 0  # 初始是 0%
        self.進度條["maximum"] = 100
########################################################################################################################################################################################
        水平框架 = tk.Frame(其他功能)
        水平框架.pack(fill="x", padx=10, pady=10)
        ##################
        def on_公司類型變更(event):
            if self.單筆類型.get() == "公司":
                self.單筆縣市.config(state=tk.DISABLED)
            else:
                self.單筆縣市.config(state=tk.NORMAL)
            # ===== 單筆查詢功能 =====
        單筆框架 = tk.LabelFrame(水平框架, text="單筆查詢", padx=10, pady=10)
        單筆框架.pack(padx=10, pady=10,side=tk.LEFT, anchor=tk.W)

        tk.Label(單筆框架, text="公司類型").grid(row=0, column=0, padx=5, pady=5)
        self.單筆類型 = ttk.Combobox(單筆框架, values=["公司", "商行"], width=27)
        self.單筆類型.grid(row=0, column=1, padx=5, pady=5)
        self.單筆類型.set("公司")
        self.單筆類型.bind("<<ComboboxSelected>>", on_公司類型變更) 
        
        tk.Label(單筆框架, text="縣市").grid(row=1, column=0, padx=5, pady=5)
        self.單筆縣市 = ttk.Combobox(單筆框架, values=list(self.地區代碼表.keys()), width=27)
        self.單筆縣市.grid(row=1, column=1, padx=5, pady=5)
        self.單筆縣市.set("臺北市")
        self.單筆縣市.config(state=tk.DISABLED)
        tk.Label(單筆框架, text="名稱").grid(row=2, column=0, padx=5, pady=5)
        self.單筆名稱 = tk.Entry(單筆框架, width=30)
        self.單筆名稱.grid(row=2, column=1, padx=5, pady=5)



        tk.Label(單筆框架, text="統一編號").grid(row=3, column=0, padx=5, pady=5)
        self.單筆統編 = tk.Entry(單筆框架, width=30)
        self.單筆統編.grid(row=3, column=1, padx=5, pady=5)



        tk.Button(單筆框架, text="查詢", command=self.執行單筆查詢).grid(row=4, column=0, columnspan=2, pady=10)

        self.單筆結果文字 = tk.Text(其他功能, height=10, width=80)
        self.單筆結果文字.pack(padx=10, pady=5)

##################################################################################################################################################################################################################################################################################################################################















































        顯示查詢網址 = self.設定.get("顯示查詢網址", "0")
        輸出詳細資料 = self.設定.get("輸出詳細資料", "0")
        自動存檔 = self.設定.get("自動存檔", "0")
        時間延遲 = self.設定.get("時間延遲", 1)  # 預設值為0.25秒



        # 其他功能區
        其他框架 = tk.LabelFrame(水平框架, text="其他功能", padx=10, pady=10)
        其他框架.pack(padx=10, pady=10, side=tk.LEFT, anchor=tk.W)

        # 勾選：是否顯示查詢網址
        self.網址設定視窗 = tk.IntVar()
        tk.Checkbutton(其他框架, text="顯示查詢網址", variable=self.網址設定視窗, command=self.及時寫入設定)\
            .grid(sticky="w", column=0, row=0)
        self.網址設定視窗.set(顯示查詢網址 == "1" and 1 or 0)  # 用 1 或 0 來表示勾選或不勾選
  # 預設值為0.25秒
        # 勾選：是否顯示詳細資料結構
        self.詳細資料結構 = tk.IntVar()
        tk.Checkbutton(其他框架, text="輸出詳細資料", variable=self.詳細資料結構, command=self.及時寫入設定)\
            .grid(sticky="w", column=0, row=1)
        self.詳細資料結構.set(輸出詳細資料)
        self.詳細輸出檔案位置 = tk.Button(其他框架, text="選擇檔案位置", command=self.選擇輸出位置)
        self.詳細輸出檔案位置.grid(sticky="w", column=0, row=4, padx=5)


        self.自動存選擇位置 = tk.IntVar()
        tk.Checkbutton(其他框架, text="自動存檔", variable=self.自動存選擇位置,command=self.及時寫入設定)\
            .grid(sticky="w", column=0, row=2)
        self.自動存選擇位置.set(自動存檔)  # 預設值為0.25秒
        


# 第1欄：靜態文字
        tk.Label(其他框架, text="儲存位置：").grid(column=0, row=3, sticky="w")  # 靠右對齊

        # 第2欄：動態路徑（帶邊框提升可讀性）
        tk.Label(
            其他框架,
            textvariable=self.輸出位置變數,
            relief="sunken",
            width=30,
            anchor="w"
        ).grid(column=0, row=3, sticky="w", padx=65)


        # 時間延遲選擇（Spinbox）
        tk.Label(其他框架, text="查詢時間延遲（秒）:")\
            .grid(sticky="w", column=0, row=5)
        self.時間延遲 = tk.Spinbox(其他框架, from_=0.3, to=5, increment=0.1, width=5, command=self.及時寫入設定)
        self.時間延遲.grid(sticky="w", column=0, row=5, padx=120, pady=3)
        self.時間延遲.delete(0, tk.END)
        self.時間延遲.insert(0, str(時間延遲))  # 預設值




    def 選擇輸出位置(self):
        路徑 = filedialog.askdirectory(title="選擇輸出資料夾")
        if 路徑:
            self.輸出位置變數.set(路徑)
            self.及時寫入設定()

    def 設定功能區(self):
        try:
            設定 = {
                "顯示查詢網址": self.網址設定視窗.get(),
                "輸出詳細資料": self.詳細資料結構.get(),
                "詳細輸出檔案位置": self.輸出位置變數.get(),
                "時間延遲":  float(self.時間延遲.get()),
                "自動存檔": self.自動存選擇位置.get()
            }
            寫入設定(**設定)
        except Exception as e:
            messagebox.showerror("錯誤", f"儲存設定時發生錯誤：{e}")
        self.根視窗.destroy()  # 關閉主視窗

    def 及時寫入設定(self):
        self.設定["時間延遲"] = float(self.時間延遲.get())
        self.設定["顯示查詢網址"] = self.網址設定視窗.get()
        self.設定["輸出詳細資料"] = self.詳細資料結構.get()
        self.設定["詳細輸出檔案位置"] = self.輸出位置變數.get()
        self.設定["自動存檔"] = self.自動存選擇位置.get()
        self.設定["記住我"] = self.記住我變數.get()

        if self.記住我變數.get():
            self.設定["使用者名稱"] = self.使用者名稱輸入框.get()
            self.設定["密碼"] = self.密碼輸入框.get()
        else:
            self.設定["使用者名稱"] = ""
            self.設定["密碼"] = ""

        寫入設定(**self.設定)


        



 
        









































#########################################################################################################

            
    def 選擇文件(self):
        路徑 = filedialog.askopenfilename(
            title="選擇 Excel 檔案",
            filetypes=[("Excel 檔案", "*.xlsx *.xls")]
        )
        if 路徑:
            self.文件路徑.set(路徑)
            self.狀態變數.set(f"已選擇文件: {路徑}")
    
    def 分析Excel(self):
        self.查詢按鈕.config(state=tk.DISABLED)
        self.保存按鈕.config(state=tk.DISABLED)
        self.分析Excel按鈕.config(state=tk.DISABLED)
        if not self.文件路徑.get():
            messagebox.showwarning("警告", "請先選擇Excel文件")
            self.選擇文件()
            self.查詢按鈕.config(state=tk.NORMAL)
            self.保存按鈕.config(state=tk.NORMAL)
            self.分析Excel按鈕.config(state=tk.NORMAL)
            return
        try:
            self.資料框架, self.公司列表, self.商行列表, self.其他列表 = 分析Excel文件(self.文件路徑.get())
            self.資料框架 = self.資料框架.loc[:, ~self.資料框架.columns.str.contains('^Unnamed')]

            self.結果文字.delete(1.0, tk.END)
            self.結果文字.insert(tk.END, "Excel分析完成！\n\n")
            self.結果文字.insert(tk.END, f"公司數量: {len(self.公司列表)}\n")
            self.結果文字.insert(tk.END, f"企業社/商行數量: {len(self.商行列表)}\n")
            self.結果文字.insert(tk.END, f"其他類型數量: {len(self.其他列表)}\n")
            if self.公司列表:
                self.結果文字.insert(tk.END, f"\n公司範例: {self.公司列表[0][0]}\n")
            if self.商行列表:
                self.結果文字.insert(tk.END, f"企業社/商行範例: {self.商行列表[0][0]}\n")
            if self.其他列表:
                self.結果文字.insert(tk.END, f"其他類型範例: {self.其他列表[0][0]}\n")
            self.狀態變數.set("Excel分析完成")
            self.查詢按鈕.config(state=tk.NORMAL)
            self.保存按鈕.config(state=tk.NORMAL)
            self.分析Excel按鈕.config(state=tk.NORMAL)
        except Exception as 錯誤:
            messagebox.showerror("錯誤", f"分析Excel時發生錯誤: {str(錯誤)}")
            self.狀態變數.set("分析失敗")
    
    def 更新進度條(self, 完成數量, 總數量):
        if 總數量 <= 0:
            return
        百分比 = int((完成數量 / 總數量) * 100)
        self.進度條["value"] = 百分比
        self.狀態變數.set(f"查詢進度: {百分比}%")
        self.根視窗.update_idletasks()

    def 查詢資料(self):
        # 禁用按鈕
        self.查詢按鈕.config(state=tk.DISABLED)
        self.保存按鈕.config(state=tk.DISABLED)
        self.分析Excel按鈕.config(state=tk.DISABLED)
        
        查詢執行緒 = threading.Thread(target=self.執行查詢資料)
        查詢執行緒.start()

    def 執行查詢資料(self):
        if not hasattr(self, '資料框架'):
            messagebox.showwarning("警告", "請先分析Excel文件")
            是否分析 = messagebox.askyesno("提示", "是否要分析Excel文件？")
            if 是否分析:
                self.分析Excel()
            else:
                # 重新啟用按鈕
                self.查詢按鈕.config(state=tk.NORMAL)
                self.保存按鈕.config(state=tk.NORMAL)
                self.分析Excel按鈕.config(state=tk.NORMAL)
                return
            return
        try:
            self.結果文字.delete(1.0, tk.END)
            self.結果文字.insert(tk.END, "開始查詢...\n")
            self.根視窗.update()

            所有結果 = {
                "公司資料": [],
                "企業社商行資料": [],
                "其他資料": []
            }

            總數量 = len(self.公司列表) + len(self.商行列表)
            if not isinstance(總數量, (int, float)) or 總數量 <= 0:
                總數量 = 1
            目前進度 = 0

            # 查詢公司資料
            if self.公司列表:
                self.結果文字.insert(tk.END, "\n===== 查詢公司資料 =====\n")
                for 公司 in self.公司列表:
                    公司結果 = 查詢公司資料([公司], text_callback=self.append_text)
                    所有結果["公司資料"].extend(公司結果)
                    目前進度 += 1
                    self.更新進度條(目前進度, 總數量)

            # 查詢企業社/商行資料
            if self.商行列表:
                self.結果文字.insert(tk.END, "\n===== 查詢企業社/商行資料 =====\n")
                for 商行 in self.商行列表:
                    商行結果 = 查詢商行資料([商行], self.地區代碼表, text_callback=self.append_text)
                    所有結果["企業社商行資料"].extend(商行結果)
                    目前進度 += 1
                    self.更新進度條(目前進度, 總數量)

            # 查詢其他類型資料
            if self.其他列表:
                self.結果文字.insert(tk.END, "\n===== 查詢其他類型資料 =====\n")
                for 名稱, 縣市, 統編 in self.其他列表:
                    self.結果文字.insert(tk.END, f"{統編} {名稱} ({縣市})\n")
                    所有結果["其他資料"].append((名稱, 縣市, 統編))
                    目前進度 += 1
                    self.更新進度條(目前進度, 總數量)

            self.結果文字.insert(tk.END, "\n查詢完成！")
            self.狀態變數.set("查詢完成")
            self.查詢結果 = 所有結果

            self.更新營業狀態()

            # 查詢完成後重新啟用按鈕
            self.查詢按鈕.config(state=tk.NORMAL)
            self.保存按鈕.config(state=tk.NORMAL)
            self.分析Excel按鈕.config(state=tk.NORMAL)
            
            if messagebox.askyesno("保存結果", "是否要保存查詢結果？"):
                self.保存結果()
            else:
                messagebox.showinfo("提示", "查詢結果未保存")
                self.狀態變數.set("查詢完成")
        except Exception as 錯誤:
            # 發生錯誤時也要重新啟用按鈕
            self.查詢按鈕.config(state=tk.NORMAL)
            self.保存按鈕.config(state=tk.NORMAL)
            self.分析Excel按鈕.config(state=tk.NORMAL)
            messagebox.showerror("錯誤", f"查詢資料時發生錯誤: {str(錯誤)}")
            print(f"查詢資料時發生錯誤: {str(錯誤)}")
            self.狀態變數.set("查詢失敗")
    
    def append_text(self, message):
        self.結果文字.insert(tk.END, message)
        self.結果文字.see(tk.END)
        self.根視窗.update_idletasks()

    def 更新營業狀態(self):
        for 公司 in self.查詢結果["公司資料"]:
            掩碼 = self.資料框架["統一編號"].astype(str) == str(公司["統編"])

            狀態 = 公司["營業狀態描述"]
            self.資料框架.loc[掩碼, "是否營業"] = 取得營業狀態(狀態)
        
        for 商行 in self.查詢結果["企業社商行資料"]:
            掩碼 = self.資料框架["統一編號"].astype(str) == str(商行["統編"])

            狀態 = 商行["營業狀態描述"]
            self.資料框架.loc[掩碼, "是否營業"] = 取得營業狀態(狀態)
        
        無結果掩碼 = self.資料框架["是否營業"] == "尚未查詢"
        self.資料框架.loc[無結果掩碼, "是否營業"] = "查無資料"


   
    def 重新儲存(self):
        """重新儲存查詢結果"""
        if hasattr(self, '查詢結果'):
            self.保存結果()
        else:
            messagebox.showwarning("警告", "沒有查詢結果可供儲存")
    
    def 保存結果(self):
        """保存查詢結果到檔案，根據設定自動選擇儲存方式"""
        if not hasattr(self, '查詢結果'):
            messagebox.showwarning("警告", "沒有查詢結果可供儲存")
            return

        # 檢查是否同時勾選顯示網址和輸出詳細資料

        輸出詳細 = self.詳細資料結構.get()
        
        if 輸出詳細:
            # 使用詳細保存功能
            if self.自動存選擇位置.get():
                # 自動保存
                儲存目錄 = Path(self.輸出位置變數.get())
                儲存目錄.mkdir(parents=True, exist_ok=True)
                時間戳 = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                檔案名稱 = f"詳細查詢結果_{時間戳}.json"
                路徑 = 儲存目錄 / 檔案名稱
                
                success, message = 詳細保存(self.資料框架, self.查詢結果, str(路徑))
                
                if success:
                    self.狀態變數.set(f"詳細結果已自動保存到: {路徑}")
                    messagebox.showinfo("自動保存完成", f"詳細結果已自動保存到:\n{路徑}")
                else:
                    messagebox.showerror("自動保存失敗", message)
            else:
                # 手動選擇保存位置
                路徑 = filedialog.asksaveasfilename(
                    defaultextension=".json",
                    filetypes=[("JSON 檔案", "*.json")],
                    title="保存詳細查詢結果"
                )
                
                if 路徑:
                    success, message = 詳細保存(self.資料框架, self.查詢結果, 路徑)
                    if success:
                        messagebox.showinfo("保存完成", message)
                    else:
                        messagebox.showerror("保存失敗", message)
            return
        # 自動儲存邏輯
        if self.自動存選擇位置.get():
            # 使用預設位置自動保存
            儲存目錄 = Path(self.輸出位置變數.get())
            
            # 確保目錄存在
            儲存目錄.mkdir(parents=True, exist_ok=True)
            
            # 生成帶時間戳的檔案名稱
            時間戳 = datetime.datetime.now().strftime("%H%M%S")
            檔案名稱 = f"查詢結果_{時間戳}.xlsx"
            路徑 = 儲存目錄 / 檔案名稱
            
            # 執行保存
            success, message = 保存結果到檔案(self.資料框架, self.查詢結果, str(路徑))
            
            if success:
                self.狀態變數.set(f"結果已自動保存到: {路徑}")
                messagebox.showinfo("自動保存完成", f"結果已自動保存到:\n{路徑}")
            else:
                messagebox.showerror("自動保存失敗", message)
                self.狀態變數.set("自動保存失敗")
        else:
            # 手動選擇保存位置
            路徑 = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel 檔案", "*.xlsx"), ("JSON 檔案", "*.json"), ("所有檔案", "*.*")],
                title="保存查詢結果"
            )
            
            if 路徑:  # 用戶沒有取消
                success, message = 保存結果到檔案(self.資料框架, self.查詢結果, 路徑)
                
                if success:
                    messagebox.showinfo("保存完成", message)
                    self.狀態變數.set(message)
                else:
                    messagebox.showerror("保存失敗", message)
                    self.狀態變數.set("保存失敗")


    def 執行單筆查詢(self):
        名稱 = self.單筆名稱.get().strip()
        統編 = self.單筆統編.get().strip()
        類型 = self.單筆類型.get()
        縣市 = self.單筆縣市.get()

        self.單筆結果文字.delete(1.0, tk.END)

        if not 名稱 and not 統編:
            messagebox.showwarning("輸入錯誤", "請至少輸入「名稱」或「統一編號」")
            return

        try:
            if 類型 == "公司":
                結果列表 = 查詢公司資料([(名稱, "", 統編)])
            else:
                結果列表 = 查詢商行資料([(名稱, 縣市, 統編)], self.地區代碼表)

            if not 結果列表:
                self.單筆結果文字.insert(tk.END, "查無結果。\n")
                return

            for 結果 in 結果列表:
                self.單筆結果文字.insert(tk.END, "===========================\n")
                for key, value in 結果.items():
                    self.單筆結果文字.insert(tk.END, f"{key}: {value}\n")
        except Exception as 錯誤:
            messagebox.showerror("錯誤", f"查詢過程中發生錯誤：{錯誤}")







################################################################################################



























    def 處理分頁(self, event):
        當前分頁 = event.widget.tab(event.widget.index("current"))["text"]
        if 當前分頁 == "商業司網址設定":
            if not getattr(self, "登入狀態變數", tk.IntVar(value=0)).get():
                messagebox.showwarning("警告", "請先登入")
                self.顯示登入介面()
                return
            self.顯示吉娃娃文字()
    def 顯示登入介面(self):
        self.登入狀態變數.set(0)
        for 登入子元件 in self.登入框架.winfo_children():
            登入子元件.destroy()

        tk.Label(self.登入框架, text="登入系統", font=('Arial', 16)).pack(pady=20)

        tk.Label(self.登入框架, text="使用者名稱:").pack()
        self.使用者名稱輸入框 = tk.Entry(self.登入框架)
        self.使用者名稱輸入框.pack(pady=5)

        tk.Label(self.登入框架, text="密碼:").pack()
        self.密碼輸入框 = tk.Entry(self.登入框架, show="*")
        self.密碼輸入框.pack(pady=5)

        # 如果有記住帳密，就自動填入
        if self.記住我變數.get():
            self.使用者名稱輸入框.insert(0, self.登入帳號)
            self.密碼輸入框.insert(0, self.登入密碼)

        tk.Button(
            self.登入框架,
            text="登入",
            command=self.嘗試登入,
            bg="#4CAF50",
            fg="white"
        ).pack(pady=20)

        tk.Checkbutton(
            self.登入框架,
            text="記住我",
            variable=self.記住我變數,
            command=self.及時寫入設定
        ).pack(pady=5)

    def 嘗試登入(self):
        使用者名稱 = self.使用者名稱輸入框.get()
        密碼 = self.密碼輸入框.get()

        if 使用者名稱 == "1" and 密碼 == "1":
            self.登入狀態變數.set(1)

            # 若勾選記住我，就存入設定
            if self.記住我變數.get():
                self.設定["使用者名稱"] = 使用者名稱
                self.設定["密碼"] = 密碼
                self.設定["記住我"] = 1
            else:
                self.設定["使用者名稱"] = ""
                self.設定["密碼"] = ""
                self.設定["記住我"] = 0

            寫入設定(**self.設定)
            self.顯示吉娃娃文字()
            messagebox.showinfo("登入成功", "歡迎回來！")
        else:
            messagebox.showerror("登入失敗", "使用者名稱或密碼錯誤")


    def 顯示吉娃娃文字(self):
        for 登入子元件 in self.登入框架.winfo_children():
            登入子元件.destroy()
        self.登入狀態變數.set(1)
        tk.Label(self.登入框架, text="🎉 歡迎！你已登入！\n\n\n 本功能開發中")\
        .grid(pady=20, column=0,row=0)
        tk.Button(self.登入框架,  text="登出", command=self.顯示登入介面, bg="#f44336", fg="white")\
        .grid(pady=20, column=0,row=0)
        self.登入狀態變數.set(1)
# column、row 
    def 暫停(self):
        self.設定["暫停"] = 0 if self.設定.get("暫停", 0) == 1 else 1
        self.暫停參數 = self.設定["暫停"]
        # 假設你有定義這個函式，這裡只是模擬
        寫入設定(**self.設定)
        if self.暫停參數 == 0:
            self.暫停按鈕.config(text="暫停")
        else:
            self.暫停按鈕.config(text="開始")

    def 安全退出(self):
        self.設定功能區()  # 保存当前设置
        os._exit(0)



