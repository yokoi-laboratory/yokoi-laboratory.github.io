---
# 旧 URL /post/page/3/（全投稿一覧の 3 ページ目）から /posts/ への転送（jekyll-redirect-from）
# gh-pages は keep_files: true でデプロイされ旧ファイルが残り続けるため、転送ページで上書きする
# 現在の投稿数では 3 ページ目が生成されないため、一覧の先頭へ転送する
permalink: /post/page/3/
redirect_to: /posts/
sitemap: false
---
