import time

from pypresence import Presence

# DiscordのアプリケーションID（Discord Developer Portalで取得したもの）
client_id = "CLIENT_ID"

# Presenceオブジェクトを作成
RPC = Presence(client_id)

# Discordに接続
RPC.connect()

# Rich Presenceを更新
RPC.update(
    state="Playing Solo",  # プレイヤーの状態
    details="Level 5",  # 詳細情報
    start=time.time(),  # 開始時間（現在の時刻）
    # end=time.time() + 30,  # 終了時間（1時間後）
    # large_image="large_image_key",  # 大きい画像のキー（Discord Developer Portalで設定したもの）
    # large_text="Game Logo",  # 大きい画像のテキスト
    # small_image="small_image_key",  # 小さい画像のキー
    # small_text="Player Status",  # 小さい画像のテキスト
    # buttons=[  # ボタン（最大2つまで）
    #     {"label": "Join Game", "url": "https://example.com/join"},
    #     {"label": "Watch", "url": "https://example.com/watch"},
    # ],
)

print("Rich Presence is running...")

# 無限ループでプログラムを走らせ続ける（Rich Presenceを維持）
try:
    while True:
        time.sleep(15)  # 15秒ごとに更新
except KeyboardInterrupt:
    print("Rich Presence stopped.")
    RPC.clear()  # Rich Presenceをクリア
    RPC.close()  # Discordから切断
