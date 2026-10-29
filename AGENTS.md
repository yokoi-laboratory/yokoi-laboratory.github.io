# AGENTS.md

このリポジトリ（Yokoi Lab の Web サイト）を編集する AI コーディング agent（Claude Code・Codex・GitHub Copilot 等）向けの作業メモ。人向けの編集フロー（ブランチ → PR → プレビュー確認 → Squash and merge）は [README.md](README.md) を参照。

## 構成

- Jekyll サイト。テーマ minimal-mistakes（4.26.2）の本体（`_sass/`・`_layouts/`・`_includes/`・`assets/js/`）をリポジトリに同梱している。テーマ本体のファイルは直接編集せず、サイト独自のスタイルは `assets/css/main.scss` に足す。
- 本番: `main` への push で `.github/workflows/build.yml` がビルドし、https://yokoi-lab.net/ に公開される。
- PR プレビュー: `.github/workflows/preview.yaml` が PR ごとにビルドし、`https://yokoi-lab.net/preview/pr-<PR 番号>/` に公開して、PR にリンクをコメントする。

## スタイル（SCSS）を変更するとき

- **本番の Sass は古い Ruby Sass 3.x**（`github-pages` 232 → `jekyll-sass-converter` 1.5.2 → `sass ~> 3.4`）。新しい Sass でしか通らない書き方は使わない。
  - `@use`／`@forward`、`math.div` などのモジュール関数は使えない。
  - `calc()` の中で変数を使うときは `calc(100% - #{$x})` のように `#{}` で埋め込む。
- 設定値は名前つきの変数にして、規則のブロックの前に置く（既存の `$program-*`・`$h4-rule-*` に倣う）。
- テーマ部品に巻き込まない。
  - `.page__content h4` のような子孫セレクタは、本文内の目次タイトル（`.nav__title`）や notice の中の見出しにも当たる。本文の見出しだけを狙うなら `.page__content > h4` のように直下に限定する。
  - 画面用の装飾は `@media screen` に入れ、テーマの印刷用スタイルを上書きしない。
- 色はサイトのモノトーン（文字色・背景色・罫線色と、それらの `mix()`）から作る。リンク色などのアクセント色を装飾に転用しない（h4 の下線をリンク色からグレーに変えた経緯がある）。
- 現在の見出しの見た目: h2 は全幅の細い下線（テーマ既定）、h3 は装飾なし、h4 は本文サイズで、文字幅の下線が右へフェードする（`assets/css/main.scss`）。h5・h6 は使っていない。

## 見た目の確認

- 最終確認は PR プレビューで行う。本番と同じ Ruby Sass でコンパイルされるのはここだけ。
- ローカルで確かめる場合:
  - Ruby が使えるなら、`bundle install && bundle exec jekyll serve` で実ビルドを見る（CI は Ruby 3.2）。
  - Jekyll が無いときは、Dart Sass で `main.scss` だけをコンパイルし、モック HTML に当てて headless Chrome で撮る。Dart Sass は本番の Ruby Sass と別の実装なので、ここで分かるのは見た目だけで、本番でコンパイルが通るかはプレビューで確かめる。
    ```bash
    TMP="$(mktemp -d)"
    # front matter を除き、Liquid の skin 指定を _config.yml の値（default）に置換してコンパイルする
    awk 'NR==1 && /^---$/ {f=1; next} f && /^---$/ {f=0; next} !f' assets/css/main.scss \
      | sed "s/{{ site.minimal_mistakes_skin | default: 'default' }}/default/" > "$TMP/test.scss"
    npx -y sass --load-path=_sass --quiet "$TMP/test.scss" "$TMP/out.css"
    # $TMP/mock.html に <link rel="stylesheet" href="out.css"> と、本番と同じ構造（section.page__content 直下に本文）のマークアップを書いてから撮る
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --user-data-dir="$TMP/chrome-prof" \
      --window-size=800,700 --virtual-time-budget=3000 --screenshot="$TMP/shot.png" "file://$TMP/mock.html"
    ```
    - テーマの `assets/js/_main.js` は、見出しの末尾にパーマリンクのアイコン（`a.header-link`）を実行時に足す。見出しの幅や配置を変えるときは、モックにも手で足して確かめる。
    - テーマのフェードインのアニメーションが撮影時点で終わっていないと、画面が真っ白に写る。`--virtual-time-budget` で待つ。
    - agent のサンドボックス内では、headless Chrome が起動できないことがある（プロファイルやソケットのディレクトリを作れない）。その場合はユーザーの承認を得て、サンドボックス外で実行する。
- 「プレビュー（または本番）に反映されていない」と言われたとき:
  1. 未 merge の PR なら、本番には出ていない。プレビューの URL を見ているか確かめる。
  2. 配信中の CSS に規則が入っているか、`curl -fsSL https://yokoi-lab.net/preview/pr-<PR 番号>/assets/css/main.css | grep -F '<セレクタ>'` で確かめる（`yokoi-laboratory.github.io` は `yokoi-lab.net` へ 301 リダイレクトするので `-L` を付ける）。
  3. 入っているなら、ブラウザのキャッシュを疑う。GitHub Pages は `cache-control: max-age=600` を返すので、最大 10 分は古い CSS が使われうる。スーパーリロード（Mac: ⌘ + Shift + R）を案内する。
