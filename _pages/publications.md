---
layout: splash
title: "Publications / 研究成果"
permalink: /publications/
author_profile: false
excerpt: ""
header:
  show_overlay_excerpt: false
  overlay_color: "#404040"
---

研究活動の成果・出版物・トーク・動画などをリストしてあります．  
載せられていない研究成果もまだ色々あるのですが，暫定的に公開します (2025-11)．  

研究内容についての質問があれば，著者や発表者まで気軽にご連絡ください：[ラボメンバー一覧 (Members)](/members/)．

## International Conferences

<div>
  <ol>
    {% for publication in site.internationalConferences reversed %}
      <li>
        {% include pub-apa-international-conf.html  %}
      </li>
    {% endfor %}

  </ol>

</div>




## Domestic Conferences

<div>
  <ol>
    {% for publication in site.domesticConferences reversed %}
    <li>
        {% include pub-anlp-domestic-conf.html  %}
      </li>
    {% endfor %}

  </ol>

</div>


## Invited Talks
<div>
  <ol>
    {% for talk in site.invitedTalks reversed %}
    <li>
        {% include pub-talks.html  %}
      </li>
    {% endfor %}

  </ol>

</div>
