---
layout: page
title: Stuff
permalink: /stuff/
---

<h2>Books that I read</h2>
<table>
<thead>
    <tr>
        <th>Read</th>
        <th>Title</th>
        <th>Authors</th>
        <th>ISBN</th>
        <th>Language</th>
        <th>Publisher</th>
        <th>Year</th>
        <th>Cover</th>
    </tr>
</thead>
<tbody>
    {% for book in site.data.books %}
    <tr>
        <td>        
        {% if book.read %}
            <img width="16px" src="/assets/images/checklist.png" alt="true" />
        {%  else %}
            <img width="16px" src="/assets/images/remove.png" alt="false" />
        {% endif %}
        </td>
        <td><a href="https://www.google.com/search?q={{book.title}}" target="_blank">{{book.title}}</a></td>
        <td>
        {% for author in book.authors %}
            {{author}}
        {% endfor %}
        </td>
        <td>{{ book.ISBN-13 }}</td>
        <td>{{ book.language }}</td>
        <td>{{ book.publisher }}</td>
        <td>{{ book.year }}</td>
        <td>
            <img src="{{book.cover}}" alt="Cover for {{book.title}}" />
        </td>
    </tr>
    {% endfor %}
</tbody>

</table>
