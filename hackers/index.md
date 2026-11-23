---
layout: page
title: Hackers digest
permalink: /hackers/
---

{% assign digests = site.hackers | sort: "date" | reverse %}
<ul>
{% for d in digests %}
  <li>
    <a href="{{ d.url | relative_url }}">{{ d.title }}</a>
    <small>{{ d.date | date: "%Y-%m-%d" }}</small>
  </li>
{% endfor %}
</ul>
