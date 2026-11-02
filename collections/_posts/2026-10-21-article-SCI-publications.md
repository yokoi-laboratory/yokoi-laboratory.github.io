---
layout: splash
title: "学会誌「システム／制御／情報」寄稿"
category: News
excerpt: "学会誌「システム／制御／情報」に、横井先生の解説記事が掲載されました。"
header:
  show_overlay_excerpt: false
  show_date: true
  overlay_color: "#404040"
---

システム制御情報学会の学会誌[「システム／制御／情報」](https://www.iscie.or.jp/pub/journal/toc)に、横井先生の解説記事が掲載されました。

<div>
  <ol>
    {% assign pubs = site.books | where_exp: "item", "item.slug contains '202609-article-SCI'" %}
    {% for publication in pubs %}
      <li>
        {% include pub-books.html book=publication %}
      </li>
    {% endfor %}
  </ol>
</div>

-> [Publications](/publications/#books)
