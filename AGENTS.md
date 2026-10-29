# AGENTS.md

このリポジトリ（Yokoi Lab の Web サイト）を編集する AI コーディング agent（Claude Code・Codex・GitHub Copilot 等）向けの作業メモ。人向けの編集フローは [README.md](README.md) にあり、agent も同じフローに従う。

## 作業の基本

- `main` に直接 push しない（push するとすぐ本番に公開される）。ブランチを切って PR を作り、プレビューの URL（下記）をユーザーに伝えて確認してもらう。
- 画像はリポジトリに commit せず、ラボの Gyazo を使う（README 参照）。

## 構成

- Jekyll サイト。`_config.yml` の `remote_theme` で minimal-mistakes 4.26.2 を指定しつつ、同じ版のテーマのファイルをリポジトリに同梱している（同梱したファイルが優先される）。
  - テーマ由来のファイル（`_sass/minimal-mistakes/`、`_layouts/`・`_includes/` のテーマ由来のもの、`assets/js/_main.js`・`main.min.js`）は直接編集しない。サイト独自のスタイルは `assets/css/main.scss` に足す。
  - `assets/js/program.js`・`mobile-submenu.js` はサイト独自の JS。
- 本番: `main` への push で `.github/workflows/build.yml` がビルドし、https://yokoi-lab.net/ に公開される。
- PR プレビュー: `.github/workflows/preview.yaml` が PR ごとにビルドし、`https://yokoi-laboratory.github.io/preview/pr-<PR 番号>/` を PR にコメントする。この URL は `https://yokoi-lab.net/preview/pr-<PR 番号>/` にリダイレクトされる。

## スタイル（SCSS）を変更するとき

- **本番の Sass は古い Ruby Sass 3.x**（`github-pages` 232 → `jekyll-sass-converter` 1.5.2 → `sass ~> 3.4`）。新しい Sass でしか通らない書き方は使わない。
  - `@use`／`@forward`、`math.div` などのモジュール関数は使えない。割り算は `/` のまま書く。Dart Sass で確かめると `/` 除算に非推奨の警告が出るが、`math.div` に直すと本番のビルドが失敗する。
  - `calc()` の中で変数を使うときは、`calc(100% - #{$x})` のように `#{}` で埋め込む。
- 設定値は名前つきの変数にして、規則のブロックの前に置く（既存の `$program-*`・`$h4-rule-*` に倣う）。
- テーマ部品に巻き込まない。
  - `.page__content h4` のような子孫セレクタは、本文内の目次タイトル（`.nav__title`）や notice の中の見出しにも当たる。本文の見出しだけを狙うなら、`.page__content > h4` のように直下に限定する。
  - 画面用の装飾は `@media screen` に入れ、テーマの印刷用スタイルを上書きしない。
- 色はサイトのモノトーン（文字色・背景色・罫線色と、それらの `mix()`）から作る。リンク色などのアクセント色を装飾に転用しない。
- 見出しの見た目を変えるときは、h2〜h4 の段差（大きさ・装飾の強さ）が逆転しないか確かめる。

## 見た目の確認

- 最終確認は PR プレビューで行う。本番と同じ CI 環境（Ruby 3.2、同じ Gemfile）でビルドされるため。
- ローカルでは、Ruby が使えるなら `bundle install && bundle exec jekyll serve` で実ビルドを見る（本番と同じ Ruby Sass を使う）。Ruby が無い場合の手早い確認方法（Dart Sass と headless Chrome）は [docs/agents/style-check.md](docs/agents/style-check.md) を参照。
- 「反映されていない」と言われたとき:
  1. 未 merge の PR なら、本番には出ていない。プレビューの URL を見ているか確かめる。
  2. 配信中の CSS に規則が入っているか確かめる。配信される CSS は圧縮されている（`_config.yml` の `style: compressed`）ので、圧縮後の表記で検索する。
     ```bash
     PR_NUMBER=115
     curl -fsSL "https://yokoi-lab.net/preview/pr-$PR_NUMBER/assets/css/main.css" | grep -oF '.page__content>h4'
     ```
  3. 規則が入っているなら、ブラウザのキャッシュを疑う。GitHub Pages は `cache-control: max-age=600` を返すので、最大 10 分は古い CSS が使われうる。スーパーリロード（Mac: ⌘ + Shift + R、Windows/Linux: Ctrl + Shift + R）を案内する。
