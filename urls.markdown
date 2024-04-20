---
layout: page
title: URLs
permalink: /urls/
---

<ul>
    {% for url in site.data.urls %}
    <li><a href="{{url.url}}">{{ url.name }}</a> <small>Added {{ url.date }}</small> Comments: {{ url.comments }}</li>
    {% endfor %}
</ul>