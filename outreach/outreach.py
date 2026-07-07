#!/usr/bin/env python3
"""
Beautiful Life — トリミングサロン営業ツール
========================================
使い方:
  python3 outreach.py          # メニューを表示
  python3 outreach.py add      # サロンを追加してテンプレート生成
  python3 outreach.py generate # 全サロンのメッセージを一括生成
  python3 outreach.py search   # おすすめサロン一覧を表示
  python3 outreach.py list     # 登録済みサロン一覧を表示
"""

import csv
import os
import sys
import urllib.request
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SALON_CSV = os.path.join(BASE_DIR, "salon_list.csv")
OUTPUT_DIR = os.path.join(BASE_DIR, "generated")
SAMPLE_URL = "https://youtube.com/playlist?list=PLScmpAnKOU2o&si=_Bo1gsP7vS3RlUDA"  # トリミング撮影サンプル

CSV_FIELDS = ["id", "salon_name", "area", "hp_url", "salon_type", "status", "notes"]

# ──────────────────────────────────────────────────────────────────
# サロンタイプ判定キーワード
# ──────────────────────────────────────────────────────────────────

PREMIUM_KEYWORDS = [
    "高級", "プレミアム", "完全予約制", "完全個室", "マンツーマン",
    "ラグジュアリー", "表参道", "麻布", "白金", "恵比寿", "青山",
    "トイプードル専門", "完全貸切", "芸能人",
]
SMALL_KEYWORDS = [
    "個人", "アットホーム", "家庭的", "こじんまり", "1頭ずつ",
    "完全マンツーマン", "手作り", "自宅",
]
CHAIN_KEYWORDS = [
    "全国", "チェーン", "フランチャイズ", "多店舗", "グループ",
    "〇〇店", "各店", "FC",
]

def detect_salon_type_from_text(text: str) -> str:
    """HPテキストからサロンタイプを判定"""
    text_lower = text.lower()
    if any(k in text for k in CHAIN_KEYWORDS):
        return "chain"
    if any(k in text for k in PREMIUM_KEYWORDS):
        return "premium"
    if any(k in text for k in SMALL_KEYWORDS):
        return "small"
    return "standard"

def fetch_hp_text(url: str) -> str:
    """HPのテキストを取得（失敗時は空文字）"""
    if not url or not url.startswith("http"):
        return ""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=5) as res:
            raw = res.read().decode("utf-8", errors="ignore")
        # タグを除去して本文だけ取得
        import re
        text = re.sub(r"<[^>]+>", " ", raw)
        text = re.sub(r"\s+", " ", text)
        return text[:3000]
    except Exception:
        return ""

# ──────────────────────────────────────────────────────────────────
# テンプレート
# ──────────────────────────────────────────────────────────────────

TEMPLATES = {
    "premium": {
        "label": "高級・完全予約制サロン向け",
        "dm": """\
はじめまして。Beautiful Life（ビューティフルライフ）と申します。

{salon_name}さまの世界観と、一頭一頭に向き合う丁寧なグルーミングに惹かれてご連絡いたしました。

私どもは、トリミングサロンさま専門に、施術シーンや店舗の雰囲気を"映画のような映像"として撮影し、そのままSNSでお使いいただける形で納品しております。

実際に制作したサンプル映像がこちらです。
▶ {sample_url}

撮影・編集はすべてお任せいただけますので、オーナーさまのお手間はかかりません。

今、東京・神奈川で一緒に作品を作らせていただくサロンさまを数店限定で募集しており、よろしければ今月中に一度、オンラインでも直接でもお話しできれば嬉しいです。

ご興味をお持ちいただけましたら、お気軽にご返信ください。

Beautiful Life
""",
    },
    "standard": {
        "label": "一般的なトリミングサロン向け",
        "dm": """\
はじめまして！Beautiful Life（ビューティフルライフ）と申します🎬

{salon_name}さんの投稿を拝見して、わんちゃんへの愛情と仕上がりの美しさが伝わってきて、ぜひご連絡したいと思いました。

私たちは、トリミングサロンさま専門に、施術シーンや店内の雰囲気を"映画のような映像"で撮影し、そのままSNSに使える形で納品しています。

先日撮影したサンプルがこちらです👇
▶ {sample_url}

撮影・編集はすべてお任せいただけるので、オーナーさまは投稿するだけ。「SNSを更新したいけど時間がない」を丸ごと解決します。

今、東京・神奈川で一緒に作品を作らせていただくサロンさまを探しており、今月中に一度お話しできれば嬉しいです。先着で数サロンさま限定の初回特別プランもご案内できます。

ご興味あれば、お気軽にご返信ください☺️

Beautiful Life
""",
    },
    "small": {
        "label": "個人・小規模サロン向け",
        "dm": """\
はじめまして！Beautiful Life（ビューティフルライフ）と申します🐾

{salon_name}さんのこだわりのあるお仕事ぶり、投稿から伝わってきて素敵だなと思っていました。

私たちは、サロンにお伺いして、わんちゃんたちの様子や店舗の雰囲気を"映画のような映像"として残すサービスをしています。

先日撮影したサンプルがこちらです👇
▶ {sample_url}

「SNSを更新したいけど撮影・編集が大変…」を、まるごとお任せいただけます。

今、東京・神奈川で一緒に作品を作らせていただくサロンさまを探していて、今月中に一度お話しできたら嬉しいです。先着数サロンさま限定で、初回をお試ししやすい特別プランもご用意しています。

お気軽にお声がけください☺️

Beautiful Life
""",
    },
    "chain": {
        "label": "チェーン・多店舗向け（法人提案）",
        "dm": """\
はじめまして。Beautiful Life（ビューティフルライフ）と申します。

{salon_name}さまの取り組みを拝見し、ぜひご提案したくご連絡いたしました。

私どもは、トリミングサロンさま専門に、施術シーンや店舗の魅力を"映画のような映像"として制作し、SNS・ブランディング・採用にご活用いただくサービスを提供しております。

実際に制作したサンプル映像がこちらです。
▶ {sample_url}

各店舗の個性を映像で表現することで、集客・採用・ブランド価値の向上につながります。

まずは今月中に一度、貴社に合わせたご提案の機会をいただけますと幸いです。
ご検討のほど、よろしくお願いいたします。

Beautiful Life
""",
    },
}

FOLLOWUP_TEMPLATE = """\
先日ご連絡させていただいたBeautiful Lifeです。
ご多忙のところ失礼いたします。

先日お送りしたサンプル映像、ご覧いただけましたでしょうか？

もしご興味をお持ちいただけましたら、今月中に一度、
オンラインでも直接でも、5分ほどお話しできれば嬉しいです。

「まずは話を聞くだけ」でも大歓迎です。
お気軽にご返信くださいませ。

Beautiful Life
"""

# ──────────────────────────────────────────────────────────────────
# おすすめサロンデータ（調査済み）
# ──────────────────────────────────────────────────────────────────

RECOMMENDED_SALONS = [
    # 東京・高級エリア
    {"salon_name": "Dog Salon V.I.D. 表参道",     "area": "渋谷区表参道", "hp_url": "https://dogsalonvid.com/",       "salon_type": "premium",  "notes": "トイプードル人気・Instagram強い"},
    {"salon_name": "Doggie-Do 麻布十番・広尾",    "area": "港区麻布十番", "hp_url": "https://doggie-do.com/",        "salon_type": "premium",  "notes": "撮影・動画送付サービスあり・競合注意"},
    # 東京・一般エリア
    {"salon_name": "渋谷区サロン（EPARKから選定）","area": "渋谷区",       "hp_url": "https://petlife.asia/salon/search/tokyo/shibuya-ku/", "salon_type": "standard", "notes": "EPARKで63件掲載・個別確認が必要"},
    {"salon_name": "世田谷区サロン（TrimTrimから選定）","area": "世田谷区", "hp_url": "https://trimtrim.jp/salons?prefecture_id%5B0%5D=13", "salon_type": "standard", "notes": "TrimTrimで一覧あり・個別確認が必要"},
    # 神奈川
    {"salon_name": "神奈川サロン（EPARKから選定）","area": "神奈川県",     "hp_url": "https://petlife.asia/salon/search/kanagawa/",         "salon_type": "standard", "notes": "998件掲載・エリア絞り込みで選定"},
]

# ──────────────────────────────────────────────────────────────────
# CSV 操作
# ──────────────────────────────────────────────────────────────────

def load_salons() -> list:
    if not os.path.exists(SALON_CSV):
        return []
    with open(SALON_CSV, encoding="utf-8") as f:
        return list(csv.DictReader(f))

def save_salons(salons: list):
    with open(SALON_CSV, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        writer.writeheader()
        writer.writerows(salons)

def next_id(salons: list) -> int:
    ids = [int(s["id"]) for s in salons if s["id"].isdigit()]
    return max(ids, default=0) + 1

# ──────────────────────────────────────────────────────────────────
# メッセージ生成
# ──────────────────────────────────────────────────────────────────

def build_message(salon: dict) -> str:
    salon_type = salon.get("salon_type", "standard")
    tmpl = TEMPLATES.get(salon_type, TEMPLATES["standard"])
    dm = tmpl["dm"].format(
        salon_name=salon["salon_name"],
        sample_url=SAMPLE_URL,
    ).strip()
    return f"""## {salon['salon_name']}（{salon['area']}）
タイプ: {tmpl['label']}
HP: {salon.get('hp_url', '—')}
メモ: {salon.get('notes', '—')}

### 📩 DM・メール文章
```
{dm}
```

### 🔁 フォローアップ（3〜5日後）
```
{FOLLOWUP_TEMPLATE.strip()}
```
"""

# ──────────────────────────────────────────────────────────────────
# コマンド
# ──────────────────────────────────────────────────────────────────

def cmd_add():
    """サロンを追加 → テンプレートをその場で表示"""
    print("\n━━ サロンを追加 ━━━━━━━━━━━━━━━━━━")
    salon_name = input("サロン名: ").strip()
    if not salon_name:
        print("サロン名は必須です。")
        return
    area = input("エリア（例: 渋谷区）: ").strip()
    hp_url = input("HP の URL（省略可）: ").strip()

    # HP解析でタイプ自動判定
    print("HPを解析中..." if hp_url else "URLなし→タイプを手動選択します")
    detected_type = "standard"
    if hp_url:
        hp_text = fetch_hp_text(hp_url)
        if hp_text:
            detected_type = detect_salon_type_from_text(hp_text)
            print(f"→ 自動判定: {detected_type}")
        else:
            print("→ HP取得できず。手動で選択してください。")

    type_labels = {
        "1": ("premium",  "高級・完全予約制サロン"),
        "2": ("standard", "一般的なトリミングサロン"),
        "3": ("small",    "個人・小規模サロン"),
        "4": ("chain",    "チェーン・多店舗（法人）"),
    }
    print("\nサロンのタイプを選んでください:")
    for k, (_, label) in type_labels.items():
        marker = " ← 自動判定" if type_labels[k][0] == detected_type else ""
        print(f"  {k}: {label}{marker}")
    choice = input("番号（Enterで自動判定を採用）: ").strip()
    salon_type = type_labels.get(choice, (detected_type,))[0]

    notes = input("メモ（省略可）: ").strip()

    salons = load_salons()
    new_salon = {
        "id": str(next_id(salons)),
        "salon_name": salon_name,
        "area": area,
        "hp_url": hp_url,
        "salon_type": salon_type,
        "status": "未送信",
        "notes": notes,
    }
    salons.append(new_salon)
    save_salons(salons)

    print("\n✅ 追加しました！\n")
    print("━━ 生成されたテンプレート ━━━━━━━━━━━━━━━━━━")
    print(build_message(new_salon))

def cmd_generate():
    """全サロン（未送信）のメッセージをファイルに出力"""
    salons = load_salons()
    targets = [s for s in salons if s.get("status") == "未送信"]
    if not targets:
        print("未送信のサロンがありません。'add' で追加してください。")
        return

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    ts = datetime.now().strftime("%Y-%m-%d_%H%M")
    out_path = os.path.join(OUTPUT_DIR, f"{ts}_messages.md")

    lines = [
        "# Beautiful Life — 営業メッセージ一覧",
        f"生成日時: {datetime.now().strftime('%Y-%m-%d %H:%M')}  |  対象: {len(targets)}件",
        "", "---", "",
    ]
    for s in targets:
        lines.append(build_message(s))
        lines.append("---\n")

    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"✅ {len(targets)}件のメッセージを生成しました")
    print(f"📄 ファイル: {out_path}")

def cmd_search():
    """おすすめサロン一覧を表示 → 選んでリストに追加"""
    print("\n━━ おすすめサロン一覧（東京・神奈川）━━━━━━━━━━━━━━━━━━")
    salons = load_salons()
    registered_names = {s["salon_name"] for s in salons}

    for i, s in enumerate(RECOMMENDED_SALONS, 1):
        tag = "（登録済み）" if s["salon_name"] in registered_names else ""
        type_label = TEMPLATES.get(s["salon_type"], {}).get("label", s["salon_type"])
        print(f"\n  [{i}] {s['salon_name']} {tag}")
        print(f"      エリア: {s['area']}")
        print(f"      HP: {s['hp_url']}")
        print(f"      タイプ: {type_label}")
        print(f"      メモ: {s['notes']}")

    choice = input("\nリストに追加する番号（複数可: 1,3,5 / Enterでスキップ）: ").strip()
    if not choice:
        return

    to_add = []
    for c in choice.split(","):
        c = c.strip()
        if c.isdigit() and 1 <= int(c) <= len(RECOMMENDED_SALONS):
            rec = RECOMMENDED_SALONS[int(c) - 1]
            if rec["salon_name"] not in registered_names:
                to_add.append(rec)

    if not to_add:
        print("追加するサロンがありませんでした。")
        return

    for rec in to_add:
        new_salon = {
            "id": str(next_id(salons)),
            "salon_name": rec["salon_name"],
            "area": rec["area"],
            "hp_url": rec["hp_url"],
            "salon_type": rec["salon_type"],
            "status": "未送信",
            "notes": rec["notes"],
        }
        salons.append(new_salon)
        print(f"✅ 追加: {rec['salon_name']}")

    save_salons(salons)
    print(f"\n{len(to_add)}件を salon_list.csv に追加しました。")
    print("'generate' コマンドでメッセージを生成できます。")

def cmd_list():
    """登録済みサロン一覧を表示"""
    salons = load_salons()
    if not salons:
        print("まだサロンが登録されていません。")
        return
    print(f"\n━━ 登録済みサロン（{len(salons)}件）━━━━━━━━━━━━━━━━━━")
    STATUS_EMOJI = {
        "未送信": "⬜", "送信済み": "📨", "返信あり": "💬",
        "商談中": "🤝", "提携済み": "✅", "見込みなし": "❌",
    }
    for s in salons:
        emoji = STATUS_EMOJI.get(s.get("status", ""), "❓")
        print(f"  {emoji} [{s['id']}] {s['salon_name']}（{s['area']}）— {s.get('status','—')}")

def cmd_update_status():
    """サロンのステータスを更新"""
    salons = load_salons()
    cmd_list()
    sid = input("\n更新するID: ").strip()
    target = next((s for s in salons if s["id"] == sid), None)
    if not target:
        print("IDが見つかりません。")
        return
    statuses = ["未送信", "送信済み", "返信あり", "商談中", "提携済み", "見込みなし"]
    for i, st in enumerate(statuses, 1):
        print(f"  {i}: {st}")
    choice = input("新しいステータス番号: ").strip()
    if choice.isdigit() and 1 <= int(choice) <= len(statuses):
        target["status"] = statuses[int(choice) - 1]
        save_salons(salons)
        print(f"✅ {target['salon_name']} → {target['status']}")

def print_menu():
    print("""
╔══════════════════════════════════════════╗
║   Beautiful Life 営業ツール              ║
╠══════════════════════════════════════════╣
║  1. add      サロンを追加してテンプレ生成 ║
║  2. generate 全サロンのメッセージを出力   ║
║  3. search   おすすめサロンを探す         ║
║  4. list     登録サロン一覧を見る         ║
║  5. status   送信状況を更新              ║
║  q. 終了                                ║
╚══════════════════════════════════════════╝""")

# ──────────────────────────────────────────────────────────────────
# エントリポイント
# ──────────────────────────────────────────────────────────────────

COMMANDS = {
    "add": cmd_add,
    "generate": cmd_generate,
    "search": cmd_search,
    "list": cmd_list,
    "status": cmd_update_status,
    "1": cmd_add,
    "2": cmd_generate,
    "3": cmd_search,
    "4": cmd_list,
    "5": cmd_update_status,
}

def main():
    if len(sys.argv) > 1:
        cmd = sys.argv[1].lower()
        if cmd in COMMANDS:
            COMMANDS[cmd]()
            return
        print(f"不明なコマンド: {cmd}")

    # インタラクティブメニュー
    while True:
        print_menu()
        choice = input("番号またはコマンド: ").strip().lower()
        if choice in ("q", "quit", "exit"):
            break
        if choice in COMMANDS:
            COMMANDS[choice]()
        else:
            print("番号またはコマンドを入力してください。")

if __name__ == "__main__":
    main()
