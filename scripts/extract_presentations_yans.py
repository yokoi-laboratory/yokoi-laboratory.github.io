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
       タイトル・著者欄はいずれも項目の境界（`</p>` や次の `<li>`）を跨がないので、
       `<br>` を欠いた項目があっても隣の項目の著者を吸い込むことはない。
    3. 著者欄を「括弧の外にある」カンマ類（, 、 ，）で分割し、各要素の
       「括弧の外で最初に現れる開き括弧」より前を名前とする（所属括弧の
       入れ子・連続にも対応）。対象著者リスト（TARGET_AUTHORS.tsv）の名前と
       「空白をすべて除去した文字列」が完全一致する著者を含む項目を抽出し、
       TSV（セッション ID / タイトル / 著者）で標準出力へ書き出す。
       完全一致にしているのは、部分一致だと「中石海」が「中石海斗」に、
       あるいは所属文字列に当たって誤検出するため。ただし、括弧の対応が
       崩れている項目や、所属括弧の後ろに想定外の文字が残る項目（未知の
       区切り文字の可能性がある）は著者単位の分割を信用できないので、
       WARNING を出してその項目だけ部分一致にフォールバックする
       （取りこぼしより過検出側に倒す）。
    4. 取りこぼし検査（スイープ）: ページ全体のテキスト（タグを潰し、実体参照は
       文字へ戻したもの）を走査して対象著者名の出現箇所をすべて洗い出し、
       いずれも解析済み項目の著者欄の内側にあることを確認する。外側の出現
       （別セクションへの掲載、解析に失敗した項目など）があれば警告を標準エラーへ
       出し、標準出力には何も書かずに終了コード 1 で終わる（誤った一覧を
       そのまま使ってしまわないようにするため）。ここで使う照合は部分一致で、
       取りこぼし側に保守的に倒してある。ただしスイープが見るのは著者欄の
       「外側」だけで、著者欄の内側での分割ミスは検知できない（そちらは
       3. のフォールバックが受け持つ）。またスイープが検知できるのは
       TSV に列挙した表記のみで、ローマ字・旧字体等の表記ゆれは
       TSV に行を足して担保する。

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
import http.client
import pathlib
import re
import sys
import time
import urllib.error
import urllib.request

# ---------------------------------------------------------------- CONFIG ----
SCRIPT_DIR = pathlib.Path(__file__).parent

# --help に出す説明（インターフェース文言は英語・ASCII）
DESCRIPTION = "Extract lab members' presentations from a conference program page."

# 既定で参照するプログラムページ（別の年・別の学会は --url で上書きする）
DEFAULT_URL = "https://yans.anlp.jp/entry/yans2026program"

# 対象著者リスト（1 行 1 名、# 始まりはコメント）
DEFAULT_AUTHORS_FILE = SCRIPT_DIR / "TARGET_AUTHORS.tsv"

# HTTP 取得の設定
HTTP_USER_AGENT = "Mozilla/5.0 (compatible; lab-site-presentation-extractor/1.0)"
HTTP_TIMEOUT_SEC = 30
RETRY_COUNT = 3
RETRY_BACKOFF_SEC = 2.0  # 2s, 4s, ... と指数的に待つ
RETRIABLE_HTTP_STATUS = {408, 429}  # 4xx のうち一時的なもの（これらはリトライする）

# 発表項目の書式:
#   <li><p>[S3-P07] タイトル<br/>著者 (所属), 著者 (所属)</p></li>
#
# セッション ID は英数字始まりの「英数字とハイフンのみ」（最大 16 文字）とする。
# コロンを含まないので「13:00-13:30」のような時刻表記は誤ってマッチしない。
# 学会側の ID 体系（例: 記号を含む、より長い）が変わったらこの文字クラスを調整する。
# (?-i: ...) は ITEM_PATTERN 全体の IGNORECASE をここだけ無効にする
# （Unicode ケースフォールドで [A-Za-z] にケルビン記号等が紛れ込むのを防ぐ）。
SESSION_ID_SUBPATTERN = r"(?-i:[A-Za-z0-9][A-Za-z0-9-]{0,15})"
# タイトル・著者欄はそれぞれ項目の境界を跨げないよう tempered subpattern にする
# （タイトルは `</p>`・`<br`・`<li` の手前まで、著者欄は `</p>`・`<li` の手前まで）。
# これにより `<br>` や `</p>` を欠いた項目があっても次の項目へ食い込まない。
ITEM_PATTERN = re.compile(
    r"<li>\s*<p>\s*\[(" + SESSION_ID_SUBPATTERN + r")\]\s*"
    r"((?:(?!</p>|<br|<li)[\s\S])*?)"
    r"<br\s*/?>"
    r"((?:(?!</p>|<li)[\s\S])*?)"
    r"</p>\s*</li>",
    re.IGNORECASE,  # <BR> や </P> のような大文字表記にも対応する
)

TAG_PATTERN = re.compile(r"<[^>]*>")
SCRIPT_STYLE_PATTERN = re.compile(r"<(script|style)\b.*?</\1>", re.DOTALL | re.IGNORECASE)
# 数値参照・名前付き参照の両方（スイープで実体参照書きの氏名を見つけるため）。
# セミコロン付きのみ対象（html.unescape はセミコロンなしも復号するが、
# パターンを緩めると通常の文字列を誤食するため、スイープはこの範囲に限る）。
ENTITY_PATTERN = re.compile(r"&(?:#x[0-9A-Fa-f]+|#[0-9]+|[A-Za-z][A-Za-z0-9]*);")

# 著者欄の区切り（半角カンマ・読点・全角カンマ）。括弧の外にあるものだけを
# 区切りとして扱う。中黒「・」はカタカナ氏名の中に現れるため意図的に含めない
# （未知の区切りが使われた項目は split_authors が検出してフォールバックする）。
# セミコロン区切りの学会に流用するときは ";；" を足す。
AUTHOR_SEPARATORS = ",、，"

# デコード失敗を示す置換文字（charset 誤りの検出に使う）
REPLACEMENT_CHARACTER = "�"
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
        except (OSError, http.client.HTTPException, ValueError) as error:
            # ValueError は不正な URL（スキームなし等）。urlopen が送出する
            if isinstance(error, ValueError):
                raise SystemExit("ERROR: invalid URL {0}: {1}".format(url, error))
            # 4xx はページ側の恒久的な問題（URL 間違い・削除）なのでリトライしない
            # （408/429 のような一時的なものは除く）
            if (
                isinstance(error, urllib.error.HTTPError)
                and 400 <= error.code < 500
                and error.code not in RETRIABLE_HTTP_STATUS
            ):
                raise SystemExit(
                    "ERROR: {0} returned HTTP {1} {2}; not retrying".format(
                        url, error.code, error.reason
                    )
                )
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
    """対象著者リストを読み込む（1 列目のみ使用、空行と # 始まりの行は無視）。"""
    try:
        # utf-8-sig: 表計算ソフトが書き出した BOM 付き TSV でも先頭名を落とさない
        lines = pathlib.Path(path).read_text(encoding="utf-8-sig").splitlines()
    except OSError as error:
        raise SystemExit("ERROR: could not read authors file {0}: {1}".format(path, error))
    authors = []
    for line in lines:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        name = line.split("\t")[0].strip()  # 2 列目以降はメモ欄として無視する
        if not name:
            continue
        if any(not character.isprintable() for character in name):
            raise SystemExit(
                "ERROR: author name contains a non-printable character in {0}: {1!r}".format(
                    path, name
                )
            )
        authors.append(name)
    if not authors:
        raise SystemExit("ERROR: no target authors found in {0}".format(path))
    return authors


def clean_text(fragment):
    """HTML 片からタグを除き、実体参照を戻し、空白を 1 個に正規化する。"""
    return re.sub(r"\s+", " ", html.unescape(TAG_PATTERN.sub("", fragment))).strip()


def compact(text):
    """空白をすべて除去する（ページ側の「横井 祥」と TSV の「横井祥」を照合するため）。"""
    return re.sub(r"\s+", "", text)


def split_authors(authors_text):
    """著者欄を 1 名ずつに分け、所属（括弧書き）を除いた名前の一覧を返す。

    区切り文字は括弧の外にあるものだけを区切りとして扱う（所属の括弧内に
    カンマを含む著者欄が実在するため。例: YANS 2026 の S4-P44）。各著者の
    名前は「括弧の外で最初に現れる開き括弧」より前の部分とする（入れ子や
    連続の所属括弧にも対応するため）。括弧の対応が崩れている場合と、
    所属括弧の後ろに空白以外の文字が残る場合（AUTHOR_SEPARATORS にない
    未知の区切り文字が使われた可能性があり、後続の著者を黙って捨てる
    おそれがある）は分割を信用できないので、(names, False) を返して
    判断を呼び出し元に委ねる。
    """
    names = []
    name_chars = []
    in_affiliation = False  # この著者の名前部分を読み終えた（所属括弧に入った）か
    depth = 0
    balanced = True

    def flush():
        nonlocal name_chars, in_affiliation
        name = "".join(name_chars).strip()
        if name:
            names.append(name)
        name_chars = []
        in_affiliation = False

    for character in authors_text:
        if character in "(（":
            if depth == 0:
                in_affiliation = True
            depth += 1
        elif character in ")）":
            if depth == 0:
                balanced = False  # 開きより先に閉じが来た
            depth = max(0, depth - 1)
        elif depth == 0 and character in AUTHOR_SEPARATORS:
            flush()
        elif depth == 0 and not in_affiliation:
            name_chars.append(character)
        elif depth == 0 and not character.isspace():
            balanced = False  # 所属括弧の後ろに想定外の文字が残った（未知の区切り？）
    flush()
    if depth != 0:
        balanced = False  # 閉じられていない括弧が残った
    return names, balanced


def item_matches(item, target_authors):
    """項目の著者のいずれかが対象著者と（空白を無視して）完全一致するか判定する。

    著者単位の分割を信用できない項目（括弧の不整合・未知の区切り文字）は、
    取りこぼし回避を優先して部分一致で判定し、WARNING を出す。部分一致は
    「中石海」が「中石海斗」や所属文字列に当たる過検出を許すが、無警告の
    取りこぼしよりは安全側なので許容する。
    """
    names, balanced = split_authors(item["authors"])
    if not balanced:
        print(
            "WARNING: item {0} has an author column that cannot be split reliably; "
            "falling back to substring matching for it".format(item["session"]),
            file=sys.stderr,
        )
        return any(compact(author) in compact(item["authors"]) for author in target_authors)
    compact_names = {compact(name) for name in names}
    return any(compact(author) in compact_names for author in target_authors)


def parse_items(page_html):
    """発表項目を解析し、セッション ID・タイトル・著者・著者欄の位置範囲を返す。"""
    items = []
    for match in ITEM_PATTERN.finditer(page_html):
        items.append(
            {
                "session": match.group(1),
                "title": clean_text(match.group(2)),
                "authors": clean_text(match.group(3)),
                "authors_raw": match.group(3),
                "authors_span": match.span(3),
            }
        )
    return items


def _blank_entity(match):
    """実体参照を、同じ長さの空白詰めフィールドに右詰めした復号文字へ置き換える。"""
    width = match.end() - match.start()
    decoded = html.unescape(match.group(0))
    if len(decoded) >= width:
        # 復号できない（未知の実体参照）等の場合は位置だけ保って潰す
        return " " * width
    return decoded.rjust(width)


def blank_out_markup(page_html):
    """タグと script/style を同じ長さの空白へ置換し、実体参照は文字へ戻す（位置を保つ）。"""
    blanked = SCRIPT_STYLE_PATTERN.sub(lambda m: " " * (m.end() - m.start()), page_html)
    blanked = TAG_PATTERN.sub(lambda m: " " * (m.end() - m.start()), blanked)
    # 「&#x6A2A;」のように実体参照で書かれた氏名もスイープで見つけられるようにする
    return ENTITY_PATTERN.sub(_blank_entity, blanked)


def find_stray_occurrences(page_html, items, target_authors):
    """解析済み項目の著者欄の外側に現れる対象著者名を洗い出す（部分一致・保守的）。"""
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
        if not needle:
            continue
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
    parser = argparse.ArgumentParser(description=DESCRIPTION)
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
        if args.url != DEFAULT_URL:
            print("NOTE: --url is ignored because --html is given", file=sys.stderr)
        try:
            page_html = pathlib.Path(args.html).read_text(encoding="utf-8", errors="replace")
        except OSError as error:
            raise SystemExit("ERROR: could not read HTML file {0}: {1}".format(args.html, error))
        print("source: local file {0}".format(args.html), file=sys.stderr)
    else:
        page_html = fetch_html(args.url)
        print("source: {0}".format(args.url), file=sys.stderr)

    if REPLACEMENT_CHARACTER in page_html:
        print(
            "WARNING: decoding produced replacement characters; charset may be wrong",
            file=sys.stderr,
        )

    items = parse_items(page_html)
    print("parsed: {0} presentations".format(len(items)), file=sys.stderr)
    if not items:
        print("WARNING: no presentation items parsed; the page layout may have changed", file=sys.stderr)
        return 1

    for item in items:
        # 著者欄に更に <br> が残る＝1 項目に複数行あり、著者欄の切り出しが怪しい
        if "<br" in item["authors_raw"].lower():
            print(
                "NOTE: item {0} contains an extra <br>; verify its author column".format(
                    item["session"]
                ),
                file=sys.stderr,
            )

    matched = [item for item in items if item_matches(item, target_authors)]
    print("matched: {0} presentations".format(len(matched)), file=sys.stderr)
    if not matched:
        print("NOTE: no presentation matched; check TARGET_AUTHORS.tsv", file=sys.stderr)
    # 出力は取りこぼし検査に通ってから書く（不完全な一覧を標準出力に流さない）
    output_lines = ["\t".join([item["session"], item["title"], item["authors"]]) for item in matched]

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

    for line in output_lines:
        print(line)
    return 0


if __name__ == "__main__":
    sys.exit(main())
