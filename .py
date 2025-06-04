import subprocess

def check_for_update():
    try:
        # 更新 GitHub 狀態
        subprocess.run(['git', 'remote', 'update'], check=True)
        # 查看是否落後遠端（有新版本）
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

# 你原本的主程式放在這邊
print("✅ 程式啟動！")
