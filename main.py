import tkinter as tk
from mods.gui import 公司查詢系統GUI
import subprocess
import os

def check_for_update():
    project_path = os.path.abspath(os.path.dirname(__file__))

    try:
        # 加入 safe.directory，避免 Git 權限錯誤
        subprocess.run(
            ['git', 'config', '--global', '--add', 'safe.directory', project_path],
            check=True
        )
    except Exception as e:
        print('⚠️ 設定 Git 安全目錄失敗：', e)

    try:
        # 嘗試拉取 Git 更新
        subprocess.run(['git', 'remote', 'update'], check=True)
        status = subprocess.check_output(['git', 'status', '-uno']).decode('utf-8')
        if 'Your branch is behind' in status:
            print('🔄 發現新版本，正在自動更新...')
            subprocess.run(['git', 'pull'], check=True)
        else:
            print('✅ 已是最新版本')
    except Exception as e:
        print('⚠️ 自動更新失敗：', e)

# 啟動程式時先檢查更新
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
