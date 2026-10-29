# Yokoi-Lab 

## Web ページの編集の仕方

1. 正しいブランチに移動する
    - 新しく編集を行う場合は `main`ブランチに移動する
    - すでに編集をし始めていてそれに上書きをする場合は、編集中のブランチに移動する
    - ※ すでにマージされたブランチはそれ以上編集しない
1. GitHub上でテキストファイルを直接編集する
    - `collections/_posts` 内: news, blog, 等 (編集というより追加が主)
    - `collections/_domesticConferences` 内: 国内会議の論文 (ANLP, 言語処理学会, 情報処理学会 等)
    - `collections/_internationalConferences` 内: 国際会議の論文 (ACL, EMNLP, NAACL 等)
    - `collections/_invitedTalks` 内: 招待講演
    - `collections/_members` 内: メンバー情報
    - `_pages` 内: Research, Publications, Join Us などのメインページのフォーマット
    - 画像を埋め込む場合は、履歴に残らないようにラボのGyazoを利用する。
1. 新しいブランチにコミットする
    - `Commit changes` ボタンをクリックする
    - Commit message を埋める (任意)
    - `Create a new branch for this commit and start a pull request` を選択
    - ブランチ名はそのままで、`Propose changes` ボタンをクリックする
1. Pull Requestを作成する
    - マージ先が `main` ブランチになっていることを確認する
    - `Create pull request` ボタンをクリックする
1. 自動 check & preview 確認
    - `github-actions` から、`Preview ready` というコメントがつく
    - リンクをクリックして、プレビューを確認する
        - リンクが表示されても、裏では準備ができていない場合があるので、しばらく待つ
    - 確認して問題がなかった場合
        - 他の人にレビューを依頼する
        - (他の人?:) 問題がなければ `Set ready for review` ボタンをクリックする
    - 確認して問題があった場合
        - すぐに修正できそうであれば、そのブランチ内で修正する
        - 修正方法がわからない場合は他の人に気軽に相談する
1. レビューが済んだら `Squash and merge` で公開処理を開始する

AI コーディング agent（Claude Code・Codex・GitHub Copilot 等）で編集する場合の注意点（本番の Sass が古い Ruby Sass であること、見た目の確認方法など）は [AGENTS.md](AGENTS.md) にまとめています。

　　初心者向け Webページ更新マニュアルはこちら  
　　<https://app.notion.com/p/yokoi-lab/Web-news-blog-3b18436103218041b001e4e87a55b508?source=copy_link>  
  
  

## セミナー記事のプログラム表の書き方

セミナー告知のプログラムは、Markdown の箇条書きで書くだけで「左に時刻・右に講演」の表になり、各講演の概要は ▶ で開く折りたたみになります（HTML を書く必要はありません）。例: `collections/_posts/2026-12-03-watanabesan-nakamutasan-kobayashisan-seminar.md`

```markdown
- **プログラム**：
  - 13:30–14:30 渡邉大師
    「講演タイトル」（仮）
    - 概要：TBA
  - 14:30–15:00 休憩
  - 15:00–16:00 中牟田旭
    「講演タイトル」（仮）
    - 概要：ここに概要を書きます。
```

- `**プログラム**：`（英語の記事では `**Program**:`）という項目の下に、字下げ（半角スペース 2 つ）した箇条書きで書く。番号付き（`1. `）でもよい。項目名の前に emoji を付けてもよい（`📝 **プログラム**：`）。
- 各項目は時刻で始める。`13:30–14:30`、`13:30-14:30`、`13:30〜14:30`、全角の `１３：３０－１４：３０`、開始時刻だけの `15:00〜`、単独の `17:30` はどれでも可。時刻を太字（`**13:30–14:30**`）にしてもよい。`17:30 - 閉会` のように前後に空白のあるダッシュは区切りとみなされ、時刻の欄には `17:30` と表示される。
- 講演者の次の行に改行してタイトルを書くと、表の中でも改行される。項目の間に空行を入れてもよい。
- さらに字下げした `- ` の項目が、▶ で開く折りたたみの中身（概要）になる。概要の無い項目（休憩・閉会など）は薄い色の行になる。
- リンクは概要の側に書く（▶ の行に書くと、開閉とリンクのどちらが動くか分かりにくくなるため）。
- 表にならず普通の箇条書きのまま表示されたら、次の 3 点を確認する: (1) 親の項目が `**プログラム**：` または `**Program**:` で始まっているか（前に置いてよいのは emoji・記号だけ）、(2) 項目が 2 つ以上あるか、(3) すべての項目の先頭が時刻か。
- 仕組み: `assets/js/program.js` が変換し、見た目は `assets/css/main.scss` の `.program` で決まる。

## 導入方法 (備忘録)
1. Personal Access Tokenを取得する
   - GitHubの設定から、[Developer settings] -> [Personal access tokens] -> [Tokens (classic)] -> [Generate new token]
   - `repo` 権限を付与する
2. Personal Access Tokenを登録する
   - GitHubの設定から、[Settings] -> [Secrets and variables] -> [Actions] -> [New repository secret]
   - 名前は `GH_PAT` とする
   - 先ほど取得したPersonal Access Tokenを値として登録する 
3. Github Actions の権限を設定する
   - GitHub Organization -> [Settings] -> [Actions] -> [General]
   - `Workflow permissions` を `Read and write permissions` に設定する
4. Github Actions `Build and Deploy` を実行する
   - main に Push すると自動で実行されるが、失敗している場合は手動で再実行する
5. GitHub Pages の設定を行う
   - GitHubの設定から、[Settings] -> [Pages]
   - `Source` を `Deployment branch` に設定する
   - `Branch` は `gh-pages` を選択する
   - `Folder` は `/docs` を選択する
   - `Save` をクリックする



## Awards の追加

Publications の Awards には、すべての collection から `awards` が空でない記事を集め、
`date` の新しい順に表示します。既存の論文などは、その記事の `awards` に追加するだけで反映されます。
同じ受賞を専用 collection にも登録すると重複するので、どちらか一方に記載してください。

論文や講演に紐づかない受賞は `collections/_awards/` に Markdown ファイルを追加します。
以下は記入形式の例です（内容は実際の受賞情報に置き換えてください）。

```yaml
---
title: "受賞対象の活動・業績"
date: 2026-10-23
authors:
  - 受賞者名
awards:
  - name: "賞の名称"
    year_month: "2026年10月"
    url: "https://example.com/awards/"
    rank: "選考件数など（任意）"
links:
  - name: "関連情報"
    url: "https://example.com/"
---
```

`title`、`date`、`awards`（各要素の `name`・`year_month`）を指定してください。
`year_month` は受賞年月で、賞名の横に表示します（例：`2026年10月`）。
記事の日付や査読サイクルの年月とは区別して指定してください。
`authors`、受賞の `url`・`rank`、`links` は任意です。
受賞情報は front matter の構造化データのみで管理し、本文は記載しません。
他 collection の記事も同じ `awards` の形式を使えます。
各賞を1項目として、賞名・著者・対象業績の順に表示します。

筆頭著者個人に贈られる賞で、その受賞者が受賞時に研究室外所属の場合は、
該当する賞に `include_in_awards: false` を指定してください。
Awards 一覧のみから除外され、論文などの受賞情報は残ります。
未指定の賞は掲載されます。所属は現在のメンバー一覧から自動判定せず、受賞時点の情報で指定します。

```yaml
awards:
  - name: "若手奨励賞"
    include_in_awards: false
    recipient_note: "筆頭著者が受賞"
```

この指定は賞ごとに適用されるため、同じ論文の別の賞は引き続き掲載できます。
`date` を省略した既存記事は Jekyll がファイル名などから決める日付で並びます。

## Local development

- (todo)
- Run local server for debugging and development
   ```bash
   bundle exec jekyll serve
   ```


## About this repo.
This site uses [Minimal Mistakes Jekyll theme](https://github.com/mmistakes/minimal-mistakes)

[![LICENSE](https://img.shields.io/badge/license-MIT-lightgrey.svg)](https://raw.githubusercontent.com/mmistakes/minimal-mistakes/master/LICENSE)
