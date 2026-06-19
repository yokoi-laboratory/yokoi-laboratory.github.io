---
layout: splash
title: "ACL 2026 採択"
category: News
excerpt: "本研究室のメンバーが関わる2件の論文が ACL 2026 に採択されました。"
header:
  show_overlay_excerpt: false
  show_date: true
  overlay_color: "#404040"
---

自然言語処理の国際会議 [The 64th Annual Meeting of the Association for Computational Linguistics (ACL 2026)](https://2026.aclweb.org/) に、
本研究室のメンバーが関わる2件の論文が採択されました。

<div>
  <ol>
    {% assign pubs = site.internationalConferences
        | where_exp: "item", "item.slug contains '202607-acl'" %}
    {% for publication in pubs %}
    <li>
    {% include pub-international-conf.html publication=publication %}
    </li>
    {% endfor %}

  </ol>

</div>

-> [Publications](/publications/#international-conferences)
