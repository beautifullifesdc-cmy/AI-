# AI Company — CEO: Jobs

## 会社概要

| 項目 | 内容 |
|------|------|
| オーナー | あなた（創業者） |
| AI CEO | Jobs（スティーブ・ジョブズ型AIリーダー） |
| 設立日 | 2026-04-30 |

## ディレクトリ構成

```
AI-/
├── README.md                  # 本ファイル
├── communications/            # オーナー ↔ Jobs の対話ログ
│   └── YYYY-MM-DD_session.md
├── jobs/                      # Jobs CEO システム定義
│   ├── persona.md             # Jobsのペルソナ・思想
│   ├── directives.md          # 現在の経営方針・指示
│   └── decisions_log.md       # Jobs の意思決定記録
├── departments/               # 各部門（Jobsの部下）
│   ├── engineering/           # エンジニアリング部門
│   ├── design/                # デザイン部門
│   ├── marketing/             # マーケティング部門
│   └── operations/            # オペレーション部門
└── activity_logs/             # 全活動の統合記録
    └── YYYY-MM-DD_activity.md
```

## 使い方

1. **対話**: `communications/` に日付付きファイルを作成し、オーナーとJobsの会話を記録
2. **指示**: Jobsが各部門に指示を出し、`departments/*/` に記録
3. **活動記録**: すべての活動は `activity_logs/` に必ず残す
