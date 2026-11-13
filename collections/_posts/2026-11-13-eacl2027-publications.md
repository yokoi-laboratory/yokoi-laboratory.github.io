---
layout: splash
title: "Findings of EACL 2027 採択"
category: News
excerpt: "本研究室のメンバーが関わる1件の論文が Findings of EACL 2027 に採択されました。"
header:
  show_overlay_excerpt: false
  show_date: true
  overlay_color: "#404040"
---

本研究室のメンバーが関わる1件の論文が Findings of the Association for Computational Linguistics: EACL 2027 に採択されました。

<div>
  <ol>
    {% assign pubs = site.internationalConferences
        | where_exp: "item", "item.slug == '202703-eacl-sasaki'" %}
    {% for publication in pubs %}
    <li>
    {% include pub-international-conf.html publication=publication %}
    </li>
    {% endfor %}

  </ol>

</div>

-> [Publications](/publications/#international-conferences)
