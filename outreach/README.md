# Beautiful Life — 営業自動化ツール

## 使い方（3ステップ）

### Step 1: サロンリストに追加
`salon_list.csv` を開いて、営業したいサロンの情報を追加する。

```csv
id,salon_name,area,instagram_handle,email,contact_method,status,notes
3,トリミングサロンOO,渋谷区,@oo_salon,,instagram,未送信,
4,Dog Salon PP,世田谷区,,info@pp.com,email,未送信,
```

`contact_method` は `instagram` か `email` を入力。

### Step 2: メッセージ生成
```bash
cd /home/user/AI-/outreach
python3 generate_outreach.py
```

`generated/` フォルダに日付入りのファイルが生成される。

### Step 3: 送信 & ステータス更新
生成されたファイルを開いてメッセージをコピー → Instagram DMに貼り付けて送信。
送信後、`salon_list.csv` の `status` を `送信済み` に更新。

---

## サンプルURLの更新方法

サンプル動画が完成したら `generate_outreach.py` の以下の行を更新：

```python
SAMPLE_VIDEO_URL = "https://www.instagram.com/p/XXXXXXXX/"  # ← 実際のURLに変更
```

---

## ステータス管理

| status値 | 意味 |
|---------|------|
| 未送信 | まだ連絡していない |
| 送信済み | DM/メール送信完了 |
| 返信あり | 返信が来た |
| 商談中 | アポ・交渉中 |
| 提携済み | 契約成立 |
| 見込みなし | 断られた or 合わない |

---

## テンプレートのカスタマイズ

`generate_outreach.py` 内の以下の変数を編集：
- `TEMPLATE_INSTAGRAM_DM` — Instagram DM文
- `TEMPLATE_EMAIL` — メール文
- `TEMPLATE_FOLLOWUP_DM` — フォローアップ文
