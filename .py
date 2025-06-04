import subprocess

def check_for_update():
    try:
        subprocess.run(['git', 'remote', 'update'], check=True)
        status = subprocess.check_output(['git', 'status', '-uno']).decode('utf-8')

        if 'Your branch is behind' in status:
            print('🔄 偵測到新版本，正在自動更新...')
            subprocess.run(['git', 'pull'], check=True)
        else:
            print('✅ 已是最新版本')
    except Exception as e:
        print(f'⚠️ 更新失敗：{e}')

# 開啟程式時先檢查更新
check_for_update()

# 然後執行你原本的主程式
print("🎯 啟動主程式...")
