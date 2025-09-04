---
layout: splash
title: "Research Outputs"
permalink: /research/outputs
author_profile: false
excerpt: ""
header:
  show_overlay_excerpt: false
  overlay_image: /assets/img/bg.png
  overlay_filter: 0.0 # same as adding an opacity of 0.5 to a black background
---

## International Conferences

<div>
  <ol>
    {% for publication in site.internationalConferences reversed %}
    <li>
        <!-- APA format -->
        {% for author in publication.authors %}
          {%- if forloop.last == true -%}
            & 
          {% endif %}
          {{ author.last_name }}, {{ author.first_name | slice: 0}}.
          {%- if forloop.last == false -%}
            ,
          {% endif %}
        {% endfor %}
        ({{ publication.year }}).
        {{ publication.title }}.
        In
        <i>{{ publication.proceedings_title }}</i>
        {%- if publication.pages -%}
          , {{ publication.pages }}
        {%- endif -%}
        .
        {% if publication.links %}
          [
          {%- for link in publication.links -%}
            <a href="{{ link.url }}" target="_blank">{{ link.name}}</a>{% if forloop.last == false %}, {% endif %}
          {%- endfor -%}
          ]
        {% endif %}
      </li>
    {% endfor %}

  </ol>

</div>




## Domestic Conferences

<div>
  <ol>
    {% for publication in site.domesticConferences reversed %}
    <li>
        <!-- https://www.anlp.jp/guide/guideline.html -->
        {% for author in publication.authors %}
          {{ author.name }}
          {%- if forloop.last == false -%}
            ,
          {% endif %}
        {% endfor %}
        ({{ publication.year }}).
        {{ publication.title }}.
        {{ publication.proceedings_title }}
        {%- if publication.pages -%}
          , pp. {{ publication.pages }}
        {%- endif -%}
        .
        {% if publication.links %}
          [
          {%- for link in publication.links -%}
            <a href="{{ link.url }}" target="_blank">{{ link.name}}</a>{% if forloop.last == false %}, {% endif %}
          {%- endfor -%}
          ]
        {% endif %}
      </li>
    {% endfor %}

  </ol>

</div>


## Invited Talks


<div>
  <ol>
    {% for talk in site.invitedTalks reversed %}
    <li>
        <!-- https://www.anlp.jp/guide/guideline.html -->
        {% for speaker in talk.speakers %}
          {{ speaker.name }}
          {%- if forloop.last == false -%}
            ,
          {% endif %}
        {%- endfor -%}
        .
        {{ talk.title }}.
        {{ talk.event_name }},
        {{ talk.month }}
        {{ talk.year }}.
        {% if talk.links %}
          [
          {%- for link in talk.links -%}
            <a href="{{ link.url }}" target="_blank">{{ link.name}}</a>{% if forloop.last == false %}, {% endif %}
          {%- endfor -%}
          ]
        {% endif %}
      </li>
    {% endfor %}

  </ol>

</div>


