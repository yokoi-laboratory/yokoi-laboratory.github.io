#!/usr/bin/env python3
"""学会プログラムページから研究室メンバーの発表を抽出する。

背景:
    YANS（NLP 若手の会）などのシンポジウムは、発表一覧を 1 枚の HTML
    プログラムページで公開する。研究室サイトの News 記事や
    collections/_domesticConferences/ のエントリを書く際、この一覧から
    研究室メンバーが著者に含まれる発表だけを手作業で拾うのは漏れが出やすい。
    本スクリプトはその抽出を再現可能にし、記事作成の元データを作る。

処理の流れ:
    1. プログラムページを取得する（リトライ + 指数バックオフ）。
       --html を指定した場合は保存済みの HTML ファイルを読む（オフライン/キャッシュ用）。
    2. `<li><p>[S3-P07] タイトル<br/>著者 (所属), 著者 (所属)</p></li>` 形式の
       発表項目をすべて解析し、セッション ID・タイトル・著者欄に分ける。
    3. 対象著者リスト（TARGET_AUTHORS.tsv）の各名前について、空白をすべて
       除去した文字列が著者欄（同じく空白除去）に含まれる項目を抽出し、
       TSV（セッション ID / タイトル / 著者）で標準出力へ書き出す。
    4. 取りこぼし検査: ページ全体のテキストを走査して対象著者名の出現箇所を
       すべて洗い出し、いずれも解析済み項目の著者欄の内側にあることを確認する。
       外側の出現（別セクションへの掲載、解析に失敗した項目など）があれば
       警告を標準エラーへ出して終了コード 1 で終わる。

使い方:
    python3 scripts/extract_presentations.py
    python3 scripts/extract_presentations.py --url https://yans.anlp.jp/entry/yans2027program
    python3 scripts/extract_presentations.py --html /tmp/yans2026.html
    python3 scripts/extract_presentations.py --authors-file /path/to/OTHER_AUTHORS.tsv

    対象著者を増減するときはコードではなく scripts/TARGET_AUTHORS.tsv を編集する。

依存:
    Python 3 標準ライブラリのみ（外部パッケージ不要）。
"""

import argparse
import html
import pathlib
import re
import sys
import time
import urllib.error
import urllib.request

# ---------------------------------------------------------------- CONFIG ----
SCRIPT_DIR = pathlib.Path(__file__).parent

# 既定で参照するプログラムページ（別の年・別の学会は --url で上書きする）
DEFAULT_URL = "https://yans.anlp.jp/entry/yans2026program"

# 対象著者リスト（1 行 1 名、# 始まりはコメント）
DEFAULT_AUTHORS_FILE = SCRIPT_DIR / "TARGET_AUTHORS.tsv"

# HTTP 取得の設定
HTTP_USER_AGENT = "Mozilla/5.0 (compatible; lab-site-presentation-extractor/1.0)"
HTTP_TIMEOUT_SEC = 30
RETRY_COUNT = 3
RETRY_BACKOFF_SEC = 2.0  # 2s, 4s, ... と指数的に待つ

# 発表項目の書式:
#   <li><p>[S3-P07] タイトル<br/>著者 (所属), 著者 (所属)</p></li>
ITEM_PATTERN = re.compile(
    r"<li>\s*<p>\s*\[(S\d+-[A-Z]*\d+)\]\s*(.*?)<br\s*/?>(.*?)</p>\s*</li>",
    re.DOTALL,
)

TAG_PATTERN = re.compile(r"<[^>]*>")
SCRIPT_STYLE_PATTERN = re.compile(r"<(script|style)\b.*?</\1>", re.DOTALL | re.IGNORECASE)
# -----------------------------------------------------------------------------


def fetch_html(url):
    """プログラムページを取得する（指数バックオフでリトライ）。"""
    last_error = None
    for attempt in range(1, RETRY_COUNT + 1):
        try:
            request = urllib.request.Request(url, headers={"User-Agent": HTTP_USER_AGENT})
            with urllib.request.urlopen(request, timeout=HTTP_TIMEOUT_SEC) as response:
                charset = response.headers.get_content_charset() or "utf-8"
                return response.read().decode(charset, errors="replace")
        except (urllib.error.URLError, OSError) as error:
            last_error = error
            if attempt < RETRY_COUNT:
                wait = RETRY_BACKOFF_SEC * (2 ** (attempt - 1))
                print(
                    "fetch failed (attempt {0}/{1}): {2}; retrying in {3:.0f}s".format(
                        attempt, RETRY_COUNT, error, wait
                    ),
                    file=sys.stderr,
                )
                time.sleep(wait)
    raise SystemExit("ERROR: could not fetch {0}: {1}".format(url, last_error))


def load_target_authors(path):
    """対象著者リストを読み込む（空行と # 始まりの行は無視）。"""
    try:
        lines = pathlib.Path(path).read_text(encoding="utf-8").splitlines()
    except OSError as error:
        raise SystemExit("ERROR: could not read authors file {0}: {1}".format(path, error))
    authors = [line.strip() for line in lines if line.strip() and not line.lstrip().startswith("#")]
    if not authors:
        raise SystemExit("ERROR: no target authors found in {0}".format(path))
    return authors


def clean_text(fragment):
    """HTML 片からタグを除き、実体参照を戻し、空白を 1 個に正規化する。"""
    return re.sub(r"\s+", " ", html.unescape(TAG_PATTERN.sub("", fragment))).strip()


def compact(text):
    """空白をすべて除去する（ページ側の「横井 祥」と TSV の「横井祥」を照合するため）。"""
    return re.sub(r"\s+", "", text)


def parse_items(page_html):
    """発表項目を解析し、(セッション ID, タイトル, 著者, 著者欄の位置範囲) の一覧を返す。"""
    items = []
    for match in ITEM_PATTERN.finditer(page_html):
        items.append(
            {
                "session": match.group(1),
                "title": clean_text(match.group(2)),
                "authors": clean_text(match.group(3)),
                "authors_span": match.span(3),
            }
        )
    return items


def blank_out_markup(page_html):
    """タグと script/style の中身を同じ長さの空白へ置換する（元の文字位置を保つ）。"""
    blanked = SCRIPT_STYLE_PATTERN.sub(lambda m: " " * (m.end() - m.start()), page_html)
    return TAG_PATTERN.sub(lambda m: " " * (m.end() - m.start()), blanked)


def find_stray_occurrences(page_html, items, target_authors):
    """解析済み項目の著者欄の外側に現れる対象著者名を洗い出す。"""
    text = blank_out_markup(page_html)
    # 空白除去した文字列と、元の文字位置への対応表を同時に作る
    compact_chars = []
    origin_index = []
    for position, character in enumerate(text):
        if not character.isspace():
            compact_chars.append(character)
            origin_index.append(position)
    compact_text = "".join(compact_chars)

    author_spans = [item["authors_span"] for item in items]
    strays = []
    for author in target_authors:
        needle = compact(author)
        search_from = 0
        while True:
            found = compact_text.find(needle, search_from)
            if found < 0:
                break
            search_from = found + 1
            start = origin_index[found]
            end = origin_index[found + len(needle) - 1] + 1
            if not any(span_start <= start and end <= span_end for span_start, span_end in author_spans):
                context = re.sub(r"\s+", " ", text[max(0, start - 60):end + 60]).strip()
                strays.append((author, start, context))
    return strays


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--url", default=DEFAULT_URL, help="program page URL (default: %(default)s)")
    parser.add_argument(
        "--authors-file",
        default=str(DEFAULT_AUTHORS_FILE),
        help="target author list, one name per line (default: %(default)s)",
    )
    parser.add_argument(
        "--html",
        default=None,
        help="read a saved HTML file instead of fetching the URL (offline/cache mode)",
    )
    args = parser.parse_args()

    target_authors = load_target_authors(args.authors_file)

    if args.html:
        try:
            page_html = pathlib.Path(args.html).read_text(encoding="utf-8", errors="replace")
        except OSError as error:
            raise SystemExit("ERROR: could not read HTML file {0}: {1}".format(args.html, error))
        print("source: local file {0}".format(args.html), file=sys.stderr)
    else:
        page_html = fetch_html(args.url)
        print("source: {0}".format(args.url), file=sys.stderr)

    items = parse_items(page_html)
    print("parsed: {0} presentations".format(len(items)), file=sys.stderr)
    if not items:
        print("WARNING: no presentation items parsed; the page layout may have changed", file=sys.stderr)
        return 1

    matched = [
        item
        for item in items
        if any(compact(author) in compact(item["authors"]) for author in target_authors)
    ]
    for item in matched:
        print("\t".join([item["session"], item["title"], item["authors"]]))
    print("matched: {0} presentations".format(len(matched)), file=sys.stderr)

    strays = find_stray_occurrences(page_html, items, target_authors)
    if strays:
        for author, position, context in strays:
            print(
                "WARNING: '{0}' occurs outside any parsed author list at offset {1}: {2}".format(
                    author, position, context
                ),
                file=sys.stderr,
            )
        print("WARNING: {0} occurrence(s) may be missing from the output".format(len(strays)), file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
