---
layout: splash
title: "Publications"
permalink: /publications/
author_profile: false
excerpt: ""
header:
  show_overlay_excerpt: false
  overlay_color: "#404040"
---

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
