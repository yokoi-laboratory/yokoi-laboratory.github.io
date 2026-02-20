---
layout: splash
title: "Members / ラボメンバー一覧"
seo_title: "Members / ラボメンバー一覧"
permalink: /members/
author_profile: false
excerpt: ""
header:
  show_overlay_excerpt: false
  overlay_color: "#404040"
---

<!-- Sort members by last name en -->

{% assign members = site.members | sort: "last_name_en" %}

<div class="member_cards_wrapper">
  {% for member in members %}
  {% if member.end_year == nil or member.end_year == "" %}
    <div class="member_card">
      {% if member.image %}
      <div class="member_image" style="background-image: url('{{ member.image | relative_url }}');"></div>
      {% else %}
      <div class="member_image" style="background-image: url({{ '/assets/img/members/default.svg' | relative_url }});"></div>
      {% endif %}
      
      {% if member.image %}
      {% endif %}
      <div class="member_info">
        <p class="member_name">
          {% if member.website %}
            <a href="{{ member.website }}">{{ member.first_name_en }} {{ member.last_name_en }} | {{member.last_name_ja}} {{ member.first_name_ja }}</a>
          {% else %}
            {{ member.first_name_en }} {{ member.last_name_en }} | {{member.last_name_ja}} {{ member.first_name_ja }}
            {% endif %}
        </p>
        <p class="member_positions">
          {{ member.positions | join: "<br>" }}
        </p>
        <p class="member_email">
          {{ member.email }}
        </p>
        {% if member.main_position %}
        <p class="member_positions">
          From {{ member.main_position }}
        </p>
        {% endif %}
      </div>
    </div>
  {% endif %}
  {% endfor %}

</div>

## Alumni

<div>
<ul>
  {% for member in members | sort: "end_year" %}
  {% if member.end_year != nil and member.end_year != "" %}
    <li>
      {{ member.first_name_en }} {{ member.last_name_en }} | {{ member.last_name_ja }} {{ member.first_name_ja }}
      <span class="period">
      {% if member.begin_year %}
        &nbsp;[{{ member.begin_year }}/{{ member.begin_month | default: "??" }}
      {% endif %}
      {% if member.end_year %}
        – {{ member.end_year }}/{{ member.end_month | default: "??" }}
      {%- endif -%}]
      </span>
      <br>
      as 
      {{ member.positions | join: ", " }}
    </li>
{% endif %}
{% endfor %}

</ul>
</div>
