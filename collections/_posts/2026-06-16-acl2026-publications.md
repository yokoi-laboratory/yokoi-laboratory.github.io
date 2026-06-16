---
layout: splash
title: "ACL 2026"
category: News
excerpt: "本研究室のメンバーが関わる2件の研究発表があります。"
header:
  show_overlay_excerpt: false
  show_date: true
  overlay_color: "#404040"
---

2026年7月2日から7日にかけてカリフォルニア州サンディエゴで開催される [The 64th Annual Meeting of the Association for Computational Linguistics (ACL 2026)](https://2026.aclweb.org/) にて、
本研究室のメンバーが関わる以下2件の研究発表が行われます。

<div>
  <ol>
    {% assign pubs = site.domesticConferences
        | where_exp: "item", "item.slug contains '202607-acl'" %}
    {% for publication in pubs %}
    <li>
    {% include pub-international-conf.html publication=publication %}
    </li>
    {% endfor %}

  </ol>

</div>

-> [Publications](/publications/#international-conferences)
