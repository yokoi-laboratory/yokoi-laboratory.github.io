---
layout: home
permalink: /
title: Yokoi Lab @ NINJAL / 横井研究室 @ 国語研
author_profile: false
excerpt: ""
header:
  overlay_image: /assets/img/bg.png
  overlay_filter: 0.0 # same as adding an opacity of 0.5 to a black background
---

**横井研究室**のウェブページです．東京は立川にある[国立国語研究所](https://www.ninjal.ac.jp/)を主な活動拠点として，広く**自然言語の数理**に関わる研究をおこなっています．

何らかの方法でジョインしてみたいというかたは，[当研究室での活動に興味があるかたへ (join us)](/join-us/) を参照ください．<br/>一般的な研究室よりもおそらくやや広めの選択肢があります．博士課程学生としての進学，他大学の学部生・修士学生・博士学生として研究活動に来る，ポスドクとしての参加，企業に在籍しつつ研究活動に来る，バックオフィスのお仕事，などなどの例があります．まずは横井まで気軽にコンタクトをください．
<!-- <br/>[現在のメンバー一覧 (members)](/members/) に，多様な所属・専門を持ったラボメンバーの一覧があります． -->


<h3 class="archive__subtitle">{{ site.data.ui-text[site.locale].recent_posts | default: "Recent Posts" }}</h3>

{% assign entries_layout = page.entries_layout | default: 'list' %}


<style>
  /* タブメニューのスタイル */
  .tab-menu {
    list-style: none;
    padding: 0;
    flex-wrap: wrap;
  }

  .tab-menu li {
    padding: 10px 20px;
    background-color: #f0f0f0;
    cursor: pointer;
    margin-right: 5px;
    text-align: start;
    justify-content: center !important;
    display: inline;
    flex: none !important;
    width: 120px;

  }

  .tab-menu li a {
    text-decoration: none;
    color: #333;
    text-align: start;
  }

  .tab-menu li a:hover {
    text-decoration: none;
  }

  .tab-menu li.active {
    background-color: #e0e0e0;
    color: white;
  }

  /* タブコンテンツのスタイル */
  .tab-content {
    margin-top: 20px;
  }

</style>



<div class="tab-container">
  <ul class="tab-menu greedy-nav">
    <li class="active visible-links">
      <a class="btn">All</a>
    </li>
    <li class="visible-links">
      <a class="btn">News</a>
    </li>
    <li class="visible-links">
      <a class="btn">Talks</a>
    </li>
    <li class="visible-links">
      <a class="btn">Blogs</a>
    </li>
  </ul>
  <div class="tab-content">

    <div>
      <div class="entries-{{ entries_layout }}">
        {% assign posts = site.posts | slice: 0, site.pagination.per_page %}
        {% include documents-collection.html entries=posts type=entries_layout %}
      </div>
      {% if site.posts.size > site.pagination.per_page %}
        <a href="/post/" class="btn btn--primary">See all</a>
      {% endif %}
    </div>

    <div style="display:none;">
      <!-- Only where category is "News" -->
      {% assign news = site.posts | where: "category", "News" %}
      {% assign news_filtered = news | slice: 0, site.pagination.per_page %}
      <div class="entries-{{ entries_layout }}">
        {% include documents-collection.html entries=news_filtered type=entries_layout %}
      </div>
      {% if news.size > site.pagination.per_page %}
        <a href="/news/" class="btn btn--primary">See all</a>
      {% endif %}
    </div>
    <div style="display:none;">
      <!-- Only where category is "Talk" -->
      {% assign talks = site.posts | where: "category", "Talk" %}
      {% assign talks_filtered = talks | slice: 0, site.pagination.per_page %}
      <div class="entries-{{ entries_layout }}">
        {% include documents-collection.html entries=talks_filtered type=entries_layout %}
      </div>

      {% if talks.size > site.pagination.per_page %}
        <a href="/talk/" class="btn btn--primary">See all</a>
      {% endif %}
    </div>
    <div style="display:none;">
      <!-- Only where category is "Blog" -->
      {% assign blogs = site.posts | where: "category", "Blog" %}
      {% assign blogs_filtered = blogs | slice: 0, site.pagination.per_page %}
      <div class="entries-{{ entries_layout }}">
        {% include documents-collection.html entries=blogs_filtered type=entries_layout %}
      </div>

      {% if blogs.size > site.pagination.per_page %}
        <a href="/blog/" class="btn btn--primary">See all</a>
      {% endif %}

    </div>
  </div>
</div>



<script>
  const tabs = document.querySelectorAll('.tab-menu li');
  const contents = document.querySelector('.tab-content').children;

  console.log(contents)


  tabs.forEach((tab, index) => {
    tab.addEventListener('click', () => {
      // すべてのタブからactiveクラスを削除
      tabs.forEach(t => t.classList.remove('active'));
      // クリックしたタブにactiveクラスを追加
      tab.classList.add('active');

      // すべてのコンテンツを非表示に
      Array.from(contents).forEach(c => c.style.display = 'none');
      // 選択されたタブに対応するコンテンツを表示
      contents[index].style.display = 'block';
    });
  });
</script>

