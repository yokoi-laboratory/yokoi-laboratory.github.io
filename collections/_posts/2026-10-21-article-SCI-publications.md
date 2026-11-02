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

システム制御情報学会の学会誌[「システム／制御／情報」](https://www.iscie.or.jp/pub/journal/toc#journal) に、横井先生の解説記事が掲載されました。

<div>
  <ol>
    {% assign pubs = site.books
        | where_exp: "item", "item.slug contains '202609-article-SCI'" %}
    {% for publication in pubs %}
    <li>
    {% include pub-international-conf.html publication=publication %}
    </li>
    {% endfor %}

  </ol>

</div>

-> [Publications](https://yokoi-lab.net/preview/pr-97/publications/#books)
