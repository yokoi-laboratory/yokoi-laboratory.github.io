---
layout: splash
title: "NLP 2026 発表"
category: News
excerpt: "自然言語処理分野の国内会議 NLP 2026 にて、本研究室のメンバーが関わる8件の研究発表がおこなわれます。"
redirect_from:
  - /posts/nlp2026-publications/
header:
  show_overlay_excerpt: false
  show_date: true
  overlay_color: "#404040"
---

2026年3月9日（月）から13日（金）にかけて宇都宮（栃木）で開催される [言語処理学会第32回年次大会 (NLP 2026)](https://anlp.jp/nlp2026/) にて、
本研究室のメンバーが関わる以下8件の研究発表がおこなわれます。

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
