# 会社運営ルール（RULES）

**制定日**: 2026-04-30  
**制定者**: Jobs (CEO)  
**適用範囲**: 全AIエージェント

---

## 絶対ルール（違反禁止）

### Rule 1: 活動記録の義務
AIエージェントが何らかの活動（分析・提案・資料作成・判断など）を行った場合、  
**必ず** `activity_logs/YYYY-MM-DD_HHMM_activity.md` に記録すること。  
記録フォーマット: `| 時刻 | 実施者 | 活動内容 | 結果 |`

### Rule 2: CEO報告の義務
各エージェントは活動の成果物を必ず Jobs (CEO) に報告すること。  
報告フォーマット: `reports/YYYY-MM-DD_HHMM_[agent]_[topic].md`  
Jobs はオーナーへの統合報告書を必ず作成すること。

### Rule 3: AI間コミュニケーションの記録義務
AIエージェント同士がコミュニケーション（情報連携・依頼・フィードバック）を行った場合、  
**必ず** `ai_communications/YYYY-MM-DD_HHMM_[from]_to_[to].md` に記録すること。

### Rule 4: ファイル命名規則（日時の正確な記録）
全ファイルの名前には **作成時点の実際の日付と時刻** を使うこと。  
フォーマット: `YYYY-MM-DD_HHMM_` （例: `2026-05-06_0453_jobs_verdict.md`）  
- ハードコードした日付は使用禁止
- 日本時間（JST, UTC+9）を基準とする
- 同日に複数ファイルを作成する場合、時刻で区別する

---

## エージェント一覧

| エージェント | 役割 | 報告先 |
|------------|------|--------|
| Jobs | CEO・最終意思決定 | オーナー |
| Aggressive Marketer | 攻めのマーケティング実行 | Jobs |
| Data Analyst | データ分析・市場調査 | Jobs |
| Business Strategist | 事業戦略立案 | Jobs |
| Creative Director | 映像品質管理 | Jobs |
| SNS Manager | SNS運用 | Jobs |
| Biz Dev | 営業・パートナー開拓 | Jobs |
| Operations | 撮影オペレーション | Jobs |
| Finance | 財務・価格戦略 | Jobs |

---

## 報告サイクル

- **即時**: 重要な発見・意思決定が必要な事項
- **活動後**: 各タスク完了時に記録
- **統合報告**: Jobs → オーナーへの報告（主要活動完了時）

---
_Jobs (CEO) 制定_
