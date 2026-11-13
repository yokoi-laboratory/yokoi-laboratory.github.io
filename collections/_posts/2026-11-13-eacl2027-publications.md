---
layout: splash
title: "EACL 2027 採択"
category: News
excerpt: "本研究室のメンバーが関わる2件の論文が EACL 2027（本会議・Findings）に採択されました。"
header:
  show_overlay_excerpt: false
  show_date: true
  overlay_color: "#404040"
---

自然言語処理の国際会議 [The 20th Conference of the European Chapter of the Association for Computational Linguistics (EACL 2027)](https://2027.eacl.org/) の本会議に1件、Findings に1件、計2件の本研究室のメンバーが関わる論文が採択されました。

<div>
  <ol>
    {% assign pubs = site.internationalConferences
        | where_exp: "item", "item.slug contains '202703-eacl-'" %}
    {% for publication in pubs %}
    <li>
    {% include pub-international-conf.html publication=publication %}
    </li>
    {% endfor %}

  </ol>

</div>

-> [Publications](/publications/#international-conferences)
