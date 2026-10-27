---
layout: splash
title: "ARR Outstanding Reviewer 受賞"
category: News
excerpt: "本研究室のメンバーが、Outstanding Reviewer, EMNLP 2026 に選出されました。"
header:
  show_overlay_excerpt: false
  show_date: true
  overlay_color: "#404040"
---

本研究室のメンバーが、[ACL Rolling Review (ARR)](https://aclrollingreview.org/) の2026年5月サイクルにおける査読活動に対して、Outstanding Reviewer, EMNLP 2026 に選出されました。

{% assign arr2026_awards = site.awards
    | where: "slug", "emnlp-outstanding-reviewer-kamoda" %}

<div>
  <ul>
    {% for document in arr2026_awards %}
      {% include pub-awards.html document=document %}
    {% endfor %}
  </ul>
</div>

-> [Publications](/publications/#awards)
