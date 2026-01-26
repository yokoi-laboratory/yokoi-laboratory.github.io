# Yokoi-Lab 

## Web ページの編集の仕方

1. 正しいブランチに移動する
    - 新しく編集を行う場合は `main`ブランチに移動する
    - すでに編集をし始めていてそれに上書きをする場合は、編集中のブランチに移動する
      - 同じブランチに編集するかどうかは，トピックが同じかどうかで判断する．
    - ※ すでにマージされたブランチはそれ以上編集しない
1. GitHub上でテキストファイルを直接編集する
    - `collections/_posts` 内: news, blog, 等 (編集というより追加が主)
    - `collections/_domesticConferences` 内: 国内会議の論文 (ANLP, 言語処理学会, 情報処理学会 等)
    - `collections/_internationalConferences` 内: 国際会議の論文 (ACL, EMNLP, NAACL 等)
    - `collections/_invitedTalks` 内: 招待講演
    - `collections/_books` 内: 書籍
    - `collections/_members` 内: メンバー情報
    - `_pages` 内: Research, Publications, Join Us などのメインページのフォーマット
    - 画像を埋め込む場合は、履歴に残らないようにラボのGyazoを利用する。
    - 注意点
      - 新しくファイルを作る場合は，拡張子まで指定すること (ほとんどの場合は`.md`)
      - 各ファイルの上部に `---`で囲まれた部分はyaml形式で書くこと
        - 適宜オンラインのチェッカー ([例](https://yamlchecker.com/)を使用すること))
        - もしくは，VSCodeに慣れている人は，github上で`.`を打つとブラウザ上でvscodeが立ち上がる
        - `tab`ではなくスペースを使用すること
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


## 導入方法 (備忘録)
1. Personal Access Tokenを取得する
   - GitHubの設定から、[Developer settings] -> [Personal access tokens] -> [Tokens (classic)] -> [Generate new token]
   - `repo` 権限を付与する
2. Personal Access Tokenを登録する
   - GitHubの設定から、[Settings] -> [Secrets and variables] -> [Actions] -> [New repository secret]
   - 名前は `GH_PAT` とする
   - 先ほど取得したPersonal Access Tokenを値として登録する 
3. Github Actions の権限を設定する
   - GitHubの設定から、[Settings] -> [Actions] -> [General]
   - `Workflow permissions` を `Read and write permissions` に設定する
4. Github Actions `Build and Deploy` を実行する
   - main に Push すると自動で実行されるが、失敗している場合は手動で再実行する
5. GitHub Pages の設定を行う
   - GitHubの設定から、[Settings] -> [Pages]
   - `Source` を `Deployment branch` に設定する
   - `Branch` は `gh-pages` を選択する
   - `Folder` は `/docs` を選択する
   - `Save` をクリックする



## Local development

- (todo)
- Run local server for debugging and development
   ```bash
   bundle exec jekyll serve
   ```


## About this repo.
This site uses [Minimal Mistakes Jekyll theme](https://github.com/mmistakes/minimal-mistakes)

[![LICENSE](https://img.shields.io/badge/license-MIT-lightgrey.svg)](https://raw.githubusercontent.com/mmistakes/minimal-mistakes/master/LICENSE)
