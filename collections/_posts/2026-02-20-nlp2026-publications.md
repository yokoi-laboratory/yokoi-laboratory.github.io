---
layout: splash
title: "NLP2026ではN件の発表があります"
category: Blog
excerpt: "ここに書いたものがTopページのリンクしたに表示される"
header:
  show_overlay_excerpt: false
  show_date: true
  overlay_color: "#404040"
---

ここに文章


<div>
  <ol>
    {% assign pubs = site.domesticConferences
        | where_exp: "item", "item.slug contains '202603-nlp'" %}
    {% for publication in pubs %}
    <li>
    {% include pub-domestic-conf.html publication=publication %}
    </li>
    {% endfor %}

  </ol>

</div>

-> [Publications](/publications/#domestic-conferences)
