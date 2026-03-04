---
layout: splash
title: "言語処理学会第32回年次大会"
category: News
excerpt: "本研究室のメンバーが関わる8件の研究発表があります。"
header:
  show_overlay_excerpt: false
  show_date: true
  overlay_color: "#404040"
---

2026年3月9日から13日にかけて宇都宮（栃木）で開催される [言語処理学会第32回年次大会 (NLP 2026)](https://anlp.jp/nlp2026/index.html)にて、
本研究室のメンバーが関わる以下8件の研究発表が行われます。

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
