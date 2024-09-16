import requests

# クライアントIDを指定
client_id = "CLIENT_ID"

# Discordの内部APIエンドポイント
url = f"https://discord.com/api/v10/applications/{client_id}/rpc"

# リクエストを送信
response = requests.get(url)

if response.status_code == 200:
    app_data = response.json()
    app_name = app_data.get("name")
    print(f"アプリケーション名: {app_name}")
    print(app_data)
else:
    print(f"エラーが発生しました: {response.status_code}")
