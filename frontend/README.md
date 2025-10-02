画面は3ページを想定する。
- トップページ
- シナリオ作成ページ
- 動画作成ページ

## ローカルで画面を確認する方法

### 1. 依存関係のインストール
```bash
npm install
```

### 2. 開発サーバーの起動
```bash
npm run dev
```

開発サーバーが起動したら、ブラウザで以下のURLにアクセスしてください:
- http://localhost:5173

### 3. バックエンドの起動（オプション）
フロントエンドのAPI連携機能を確認する場合は、バックエンドサーバーも起動してください:
```bash
cd ../backend
source .venv/bin/activate  # Unix/Mac
# または
.venv\Scripts\activate  # Windows
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Dockerでの起動確認

### フロントエンドのみDockerで起動する場合
```bash
# frontend/Dockerfileを使ってビルド
docker build -t video-frontend .

# コンテナを起動
docker run -p 5173:5173 -v $(pwd):/app -v /app/node_modules video-frontend

# ブラウザでアクセス
# http://localhost:5173
```

### docker-composeで全体を起動する場合
```bash
# プロジェクトルートで実行
cd ..
docker-compose up

# フロントエンド: http://localhost:5173
# バックエンド: http://localhost:8000
```

## 画面設計
### トップページ
- 概要説明
  - このアプリケーションは、ユーザーがシナリオを作成し、それに基づいて動画を生成するためのものです。
- 1.シナリオ作成ページへのリンク
- 2.動画作成ページへのリンク

### シナリオ作成ページ
- シナリオ作成フォーム
  - ページタイトル：シナリオ作成
  - 入力フィールド：geminiに渡すシナリオテキスト（テキストエリア）https://mui.com/material-ui/react-text-field/#multiline
  - ボタン：generate(入力フィールドの内容を元にシナリオを生成するトリガー)https://mui.com/material-ui/react-button/#loading-2
- シナリオ作成画面 - 成功：
  - https://mui.com/material-ui/react-alert/
  - 表示内容：シナリオが正常に作成されました。
  - 生成されたシナリオテキストを表示するエリア
- シナリオ作成画面 - 失敗：
  - https://mui.com/material-ui/react-alert/
  - 表示内容：エラーが発生しました。
- ボトムナビゲーション：推移をイメージしやすいようなデザイン
    - シナリオ作成（現在のページを強調表示）
    - 動画作成（動画作成ページへのリンク）

### 動画作成ページ
- 動画作成フォーム
- ページタイトル：動画作成
- 入力フィールド：シナリオテキスト（テキストエリア）
- オプション：
    - 字幕をつける：チェックボックス（デフォルト有効）
    - 動画の長さ：スライダー（0~20秒、デフォルト10秒）
  - ボタン：create video(入力フィールドの内容を元に動画を生成するトリガー)
- ロード中表示：
  - 実行中なのがわかるようにする（進捗率は入れないもの）
- 動画作成画面 - 成功：
  - https://mui.com/material-ui/react-alert/
  - 表示内容：動画が正常に作成されました。
  - 生成された動画を表示するエリア
- 動画作成画面 - 失敗：
  - https://mui.com/material-ui/react-alert/
  - 表示内容：エラーが発生しました。
  - ボトムナビゲーション：推移をイメージしやすいようなデザイン
    - シナリオ作成（シナリオ作成ページへのリンク）
    - 動画作成（現在のページを強調表示）
