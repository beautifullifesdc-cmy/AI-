# Beautiful Life 営業ツール

## 起動方法

```bash
cd /home/user/AI-/outreach
python3 outreach.py
```

---

## コマンド一覧

| コマンド | 内容 |
|---------|------|
| `add` | サロン名・HP URLを入力 → テンプレを即生成 |
| `search` | おすすめサロン一覧 → 選んでリストに追加 |
| `generate` | 未送信サロン全件のメッセージをファイル出力 |
| `list` | 登録サロンと送信状況を一覧表示 |
| `status` | 送信状況を更新（送信済み・商談中・提携済みなど） |

---

## 基本的な使い方の流れ

```
① python3 outreach.py search
   → おすすめサロンを見てリストに追加

② python3 outreach.py add
   → 自分で見つけたサロンを追加

③ python3 outreach.py generate
   → 全メッセージを一括生成・ファイルに保存

④ DMを送ったら python3 outreach.py status で「送信済み」に更新
```

---

## サンプルURLの更新

サンプル動画が完成したら `outreach.py` の以下を変更：

```python
SAMPLE_URL = "https://www.instagram.com/p/XXXXXXXX/"  # ← 実際のURLに
```

---

## salon_list.csv について

手動で編集しても OK。フィールドは以下：

| フィールド | 内容 |
|-----------|------|
| id | 自動採番 |
| salon_name | サロン名 |
| area | エリア（例: 渋谷区） |
| hp_url | HP の URL |
| salon_type | premium / standard / small / chain |
| status | 未送信 / 送信済み / 返信あり / 商談中 / 提携済み / 見込みなし |
| notes | メモ |
