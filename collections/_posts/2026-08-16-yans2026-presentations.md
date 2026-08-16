---
layout: splash
title: "YANS 2026 発表"
category: News
excerpt: "自然言語処理分野の若手の会 YANS 2026 にて本研究室のメンバーが関わる4件の研究発表がおこなわれます。"
header:
  show_overlay_excerpt: false
  show_date: true
  overlay_color: "#404040"
---

2026年8月16日（日）〜18日（火）に仙台（宮城）で開催される [第21回言語処理若手シンポジウム (YANS 2026)](https://yans.anlp.jp/entry/yans2026) にて、
本研究室のメンバーが関わる以下4件の研究発表がおこなわれます。

<div>
  <ol>
    {% assign pubs = site.domesticConferences
        | where_exp: "item", "item.slug contains '202608-yans'" %}
    {% for publication in pubs %}
    <li>
    {% include pub-domestic-conf.html publication=publication %}
    </li>
    {% endfor %}

  </ol>

</div>

-> [Publications](/publications/#domestic-conferences)
