---
layout: page
title: URLs
permalink: /urls/
---

<table>
<thead>
    <tr>
        <th>Read</th>
        <th>What</th>
        <th>Date</th>
        <th>Comments</th>
    </tr>
</thead>
<tbody>
    {% for url in site.data.urls %}
    <tr>
        <td>
        {% if url.done %}
            <img sizes="16x16" src="/assets/images/checklist.png" alt="true" />
        {%  else %}
            <img sizes="16x16" src="/assets/images/remove.png" alt="true" />
        {% endif %}
        </td>
        <td><a href="{{url.url}}">{{ url.name }}</a></td>
        <td>{{ url.date }}</td>
        <td>{{ url.comments }}</td>
    </tr>
    {% endfor %}
</tbody>

</table>