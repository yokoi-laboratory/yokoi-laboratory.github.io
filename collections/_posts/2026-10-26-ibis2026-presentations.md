---
layout: splash
title: "IBIS 2026 発表"
category: News
excerpt: "第29回情報論的学習理論ワークショップ IBIS 2026 にて、本研究室のメンバーが関わる2件の研究発表がおこなわれます。"
header:
  show_overlay_excerpt: false
  show_date: true
  overlay_color: "#404040"
---

2026年10月26日（月）から29日（木）にかけてソニックシティ（埼玉）で開催される [第29回情報論的学習理論ワークショップ (IBIS 2026)](https://ibisml.org/ibis2026/) にて、
本研究室のメンバーが関わる以下2件の研究発表がおこなわれます。

<div>
  <ol>
    {% assign pubs = site.domesticConferences
        | where_exp: "item", "item.slug contains '202610-ibis'" %}
    {% for publication in pubs %}
    <li>
    {% include pub-domestic-conf.html publication=publication %}
    </li>
    {% endfor %}

  </ol>

</div>

-> [Publications](/publications/#domestic-conferences)
