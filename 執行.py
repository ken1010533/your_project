import tkinter as tk
from tkinter import messagebox
from mods.gui import 公司查詢系統GUI
import subprocess
import sys
import os

def check_for_update():
    repo_path = os.path.abspath(os.path.dirname(__file__))
    try:
        subprocess.run(['git', 'remote', 'update'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        status = subprocess.check_output(['git', 'status', '-uno']).decode('utf-8')
        if 'Your branch is behind' in status:
            print('🔄 發現新版本，正在自動更新...')
            subprocess.run(['git', 'reset', '--hard'], check=True)
            subprocess.run(['git', 'pull'], check=True)

            root = tk.Tk()
            root.withdraw()
            messagebox.showinfo("更新完成", "已自動更新到最新版本。\n請重新啟動程式。")
            sys.exit()
        else:
            print('✅ 已是最新版本')

    except subprocess.CalledProcessError as e:
        output = e.stderr.decode() if e.stderr else str(e)
        if 'detected dubious ownership' in output:
            print("⚠️ 偵測到安全目錄錯誤，正在加入 safe.directory...")
            subprocess.run(['git', 'config', '--global', '--add', 'safe.directory', repo_path], check=True)
            check_for_update()
        else:
            print('⚠️ 自動更新失敗：', output)
    except Exception as e:
        print('⚠️ 自動更新失敗：', e)

check_for_update()

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
