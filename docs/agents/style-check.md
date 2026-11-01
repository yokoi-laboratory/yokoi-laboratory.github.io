# Ruby が無い環境で SCSS の見た目を確かめる

Jekyll（Ruby）が使えないときに、`assets/css/main.scss` だけを Dart Sass でコンパイルし、モック HTML に当てて headless Chrome で撮る手順。本番は Ruby Sass 3.x でコンパイルされるので、ここで分かるのは見た目の目安だけ。本番でコンパイルが通るかは PR プレビューで確かめる（[AGENTS.md](../../AGENTS.md) 参照）。

前提: Node.js/npm（初回は npm registry へのネットワーク接続が要る）、Google Chrome（または Chromium）、`awk`・`sed` が使えるシェル（Windows なら WSL か Git Bash）。

## 1. コンパイルする

リポジトリのルートで実行する。

```bash
TMP="$(mktemp -d)"
SASS_VERSION=1.107.0   # 動作を確認したバージョン。上げるときは警告の出方が変わらないか確かめる
# front matter を除き、Liquid の skin 指定を _config.yml の値（default）に置換する
awk 'NR==1 && /^---$/ {f=1; next} f && /^---$/ {f=0; next} !f' assets/css/main.scss \
  | sed "s/{{ site.minimal_mistakes_skin | default: 'default' }}/default/" > "$TMP/test.scss"
npx -y "sass@$SASS_VERSION" --load-path=_sass --quiet "$TMP/test.scss" "$TMP/out.css"
```

- `--quiet` は、既存の `/` 除算に対する Dart Sass の非推奨警告を抑えるために付けている。警告に従って `math.div` に書き換えてはいけない（本番の Ruby Sass で失敗する）。
- 出力された `$TMP/out.css` を `grep -F` で検索し、変数が意図した値に展開されているか確かめる。

## 2. モック HTML を書く

`$TMP/mock.html` に、コンパイルした CSS と、本番と同じ構造（`section.page__content` の直下に本文）のマークアップを置く。

```html
<html><head><meta charset="utf-8"><link rel="stylesheet" href="out.css"></head>
<body><div id="main"><section class="page__content" style="max-width:700px;margin:0 auto;padding:1em">
  <h2>見出し 2</h2><p>本文</p>
  <h3>見出し 3</h3>
  <h4>見出し 4<a class="header-link" href="#x"><i class="fas fa-link"></i></a></h4>
  <ul><li>箇条書き</li></ul>
</section></div></body></html>
```

- テーマの JS（配信されるのは `assets/js/main.min.js`、ソースは `_main.js`）は、見出しの末尾にパーマリンクのアイコン `a.header-link` を実行時に足す。見出しの幅や配置を変えるときは、モックにも手で足して確かめる。
- 前後の要素の並び（h3 直後の h4、段落の後の h4 など）と、折り返すほど長い見出しも入れておく。

## 3. headless Chrome で撮る

```bash
CHROME="${CHROME:-google-chrome}"   # macOS では "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
"$CHROME" --headless=new --user-data-dir="$TMP/chrome-prof" --window-size=800,700 \
  --virtual-time-budget=3000 --screenshot="$TMP/shot.png" "file://$TMP/mock.html"
```

- テーマのフェードインのアニメーションが撮影時点で終わっていないと、画面が真っ白に写る。`--virtual-time-budget` はそのための待ち時間。
- agent の実行環境の制限（サンドボックス等）で Chrome が起動できないことがある。制限を勝手に回避せず、ユーザーに報告する（承認が得られれば制限の外で実行する）。

## 4. 狭い画面で横スクロールが出ないか確かめる

headless Chrome はウィンドウ幅に下限があることがあり、`--window-size=320,...` でも 320px で描画されない場合がある。iframe で幅を固定し、`scrollWidth` と `clientWidth` を比べる。

```bash
cat > "$TMP/check.html" <<'EOF'
<iframe id="f" src="mock.html" style="width:320px;height:800px;border:0"></iframe>
<script>
const f = document.getElementById("f");
f.onload = () => {
  const d = f.contentDocument.documentElement;
  document.body.dataset.result = `client=${d.clientWidth} scroll=${d.scrollWidth}`;
};
</script>
EOF
"$CHROME" --headless=new --user-data-dir="$TMP/chrome-prof" --allow-file-access-from-files \
  --virtual-time-budget=3000 --dump-dom "file://$TMP/check.html" | grep -o 'data-result="[^"]*"'
```

- `client` と `scroll` が同じなら、横スクロールは出ていない。
- `--allow-file-access-from-files` は、file:// のページから他のローカルファイルを読めるようにする開発用フラグ。自分で書いた HTML を、一時ディレクトリの中で、専用プロファイルを使って開くときだけ使う。
