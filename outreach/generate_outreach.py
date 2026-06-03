#!/usr/bin/env python3
"""
Beautiful Life — 営業DM・メール 自動生成ツール
使い方: python3 generate_outreach.py
"""

import csv
import os
from datetime import datetime

SALON_LIST_PATH = os.path.join(os.path.dirname(__file__), "salon_list.csv")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "generated")

SAMPLE_VIDEO_URL = "https://www.instagram.com/beautifullife.movie/"  # 完成後サンプルURLに差し替え

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# テンプレート（編集してカスタマイズ可能）
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TEMPLATE_INSTAGRAM_DM = """はじめまして！Beautiful Life（ビューティフルライフ）と申します。
{salon_name}さんのInstagramをいつも拝見しており、わんちゃんへの愛情が伝わる投稿にとても惹かれてご連絡しました。

私たちはペット事業者さま向けに、シネマティックな映像でお店の魅力をSNS素材として制作するサービスを提供しています。

月1回の訪問で、1ヶ月分のInstagram投稿素材（Reels動画・写真）をまとめて制作・納品します。
オーナーさまは投稿するだけ。撮影・編集はすべてお任せください。

先日、DOG SALON ANELAさまでサンプル動画を制作しました。
よろしければご覧ください👇
{sample_url}

導入いただいたサロンさまには、Beautiful Lifeのサイト・SNSから優先的にご紹介もさせていただいています。

最初の1ヶ月は特別価格でお試しいただけます。
ご興味があればお気軽にご返信ください！
"""

TEMPLATE_EMAIL = """件名：【Beautiful Life】{salon_name}さまへ — ペット専門映像制作のご提案

{salon_name} ご担当者様

はじめてご連絡させていただきます。
ペット事業者さま向けシネマティック映像制作サービス「Beautiful Life」の{owner_name}と申します。

━━ ご提案内容 ━━━━━━━━━━━━━━━━━━━━━━

月1回の訪問で、1ヶ月分のSNS投稿素材を制作・納品するサービスです。

【Beautiful Lifeができること】
✔ わんちゃんのトリミングシーンをシネマティックな映像で記録
✔ Reels動画・写真をまとめて納品（投稿するだけでOK）
✔ スタッフの想い・お店の雰囲気を採用・ブランディングに活かせる映像制作
✔ Beautiful Lifeのサイト・SNSから貴サロンへ顧客紹介

【料金プラン】
・ライトプラン：¥29,800/月（写真20枚・Reels1本）
・スタンダード：¥49,800/月（写真50枚・Reels3本）※最も人気
・プレミアム　：¥79,800/月（写真100枚・Reels5本・SNSサポート）

━━ サンプル動画 ━━━━━━━━━━━━━━━━━━━━━━
{sample_url}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

まずは一度、お話を聞いていただけますか？
30分程度のオンライン or 対面でのご説明も対応しております。

ご検討のほど、よろしくお願いいたします。

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Beautiful Life
Instagram: @beautifullife.movie
{owner_name}
"""

TEMPLATE_FOLLOWUP_DM = """先日ご連絡させていただいたBeautiful Lifeです。
ご多忙のところ失礼いたします。

先日送ったサンプル動画、ご覧いただけましたでしょうか？

「まずはお話だけでも」という形でも大歓迎です。
ご都合のよいタイミングがあればお気軽にご返信ください！"""


def load_salons():
    salons = []
    try:
        with open(SALON_LIST_PATH, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                salons.append(row)
    except FileNotFoundError:
        print(f"❌ salon_list.csv が見つかりません: {SALON_LIST_PATH}")
    return salons


def generate_messages(salon: dict, owner_name: str = "オーナー") -> dict:
    name = salon.get("salon_name", "サロン")
    return {
        "instagram_dm": TEMPLATE_INSTAGRAM_DM.format(
            salon_name=name,
            sample_url=SAMPLE_VIDEO_URL,
        ).strip(),
        "email": TEMPLATE_EMAIL.format(
            salon_name=name,
            owner_name=owner_name,
            sample_url=SAMPLE_VIDEO_URL,
        ).strip(),
        "followup": TEMPLATE_FOLLOWUP_DM.strip(),
    }


def save_output(salons: list, owner_name: str):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M")
    output_path = os.path.join(OUTPUT_DIR, f"{timestamp}_outreach_messages.md")

    lines = [
        "# Beautiful Life — 営業メッセージ一覧",
        f"生成日時: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"対象件数: {len([s for s in salons if s.get('status', '') not in ('提携済み',)])} 件",
        "",
        "---",
        "",
    ]

    for s in salons:
        if s.get("status") in ("提携済み",):
            continue
        msgs = generate_messages(s, owner_name)
        lines += [
            f"## {s['id']}. {s['salon_name']}（{s['area']}）",
            f"- 連絡方法: {s.get('contact_method', '未設定')}",
            f"- Instagram: {s.get('instagram_handle', '—')}",
            f"- メモ: {s.get('notes', '—')}",
            "",
            "### Instagram DM 文章",
            "```",
            msgs["instagram_dm"],
            "```",
            "",
            "### メール文章",
            "```",
            msgs["email"],
            "```",
            "",
            "### フォローアップ（3〜5日後）",
            "```",
            msgs["followup"],
            "```",
            "",
            "---",
            "",
        ]

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"✅ 生成完了: {output_path}")
    print(f"📋 {len([s for s in salons if s.get('status') not in ('提携済み',)])} 件のメッセージを出力しました")
    return output_path


def main():
    print("🐾 Beautiful Life 営業メッセージ生成ツール")
    print("=" * 50)

    owner_name = input("オーナーのお名前（省略可・Enterでスキップ）: ").strip() or "オーナー"

    salons = load_salons()
    if not salons:
        return

    targets = [s for s in salons if s.get("status") not in ("提携済み",)]
    print(f"\n📋 対象サロン: {len(targets)} 件")
    for s in targets:
        print(f"  - {s['salon_name']}（{s['area']}）[{s.get('contact_method', '—')}]")

    print("\n📝 メッセージを生成中...")
    output_path = save_output(salons, owner_name)

    print("\n💡 次のステップ:")
    print("  1. 上のファイルを開いてメッセージを確認")
    print("  2. サロンのInstagramを開いてDMに貼り付け")
    print("  3. 送信後、salon_list.csv の status を「送信済み」に更新")
    print("  4. 3〜5日後にフォローアップを送信")


if __name__ == "__main__":
    main()
