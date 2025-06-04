import tkinter as tk
from mods.gui import 公司查詢系統GUI

    
if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = 公司查詢系統GUI(root)
        root.mainloop()
    except Exception as e:
        import traceback
        print("發生錯誤：", e)
        traceback.print_exc()
        input("按下 Enter 鍵以結束...")
 
