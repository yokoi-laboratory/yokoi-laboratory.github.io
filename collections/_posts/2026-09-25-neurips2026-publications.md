---
layout: splash
title: "NeurIPS 2026 Position Paper Track 採択"
category: News
excerpt: "本研究室のメンバーが関わる1件の論文が NeurIPS 2026 Position Paper Track に採択されました。"
header:
  show_overlay_excerpt: false
  show_date: true
  overlay_color: "#404040"
---

機械学習の国際会議 [The Fortieth Annual Conference on Neural Information Processing Systems (NeurIPS 2026)](https://neurips.cc/Conferences/2026) の Position Paper Track に、
本研究室のメンバーが関わる1件の論文が採択されました。

<div>
  <ol>
    {% assign pubs = site.internationalConferences
        | where_exp: "item", "item.slug contains '202612-neurips'" %}
    {% for publication in pubs %}
    <li>
    {% include pub-international-conf.html publication=publication %}
    </li>
    {% endfor %}

  </ol>

</div>

-> [Publications](/publications/#international-conferences)
