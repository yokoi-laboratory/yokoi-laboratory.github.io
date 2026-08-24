---
layout: splash
title: "EMNLP 2026 採択"
category: News
excerpt: "本研究室のメンバーが関わる1件の論文が EMNLP 2026 に採択されました。"
header:
  show_overlay_excerpt: false
  show_date: true
  overlay_color: "#404040"
---

自然言語処理の国際会議 [The 2026 Conference on Empirical Methods in Natural Language Processing (EMNLP 2026)](https://2026.emnlp.org/) に、
本研究室のメンバーが関わる1件の論文が採択されました。

<div>
  <ol>
    {% assign pubs = site.internationalConferences
        | where_exp: "item", "item.slug contains '202610-emnlp'" %}
    {% for publication in pubs %}
    <li>
    {% include pub-international-conf.html publication=publication %}
    </li>
    {% endfor %}

  </ol>

</div>

-> [Publications](/publications/#international-conferences)
