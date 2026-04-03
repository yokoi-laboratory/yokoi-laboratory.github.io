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
    - 画像を埋め込む場合は、履歴に残らないようにラボのGyazoを利用する。(Notionを参照すること)
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


## Local development

- (todo)
- Run local server for debugging and development
   ```bash
   bundle exec jekyll serve
   ```


## About this repo.
This site uses [Minimal Mistakes Jekyll theme](https://github.com/mmistakes/minimal-mistakes)

[![LICENSE](https://img.shields.io/badge/license-MIT-lightgrey.svg)](https://raw.githubusercontent.com/mmistakes/minimal-mistakes/master/LICENSE)
