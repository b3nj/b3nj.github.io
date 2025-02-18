---
layout: page
title: 
permalink: /stuff/
---

<h1>Stuff I read, watch and listen to</h1>

<h2>Books that I read</h2>
<table>
<thead>
    <tr>
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
        <td>"{{book.Title}}"</td>
        <td>
        {% for Author in book.Authors %}
            "{{Author}}"
        {% endfor %}
        </td>
        <td>"{{ book.ISBN-13 }}"</td>
        <td>"{{ book.Language }}"</td>
        <td>"{{ book.Publisher }}"</td>
        <td>"{{ book.Year }}"</td>
        <td>
            <img width="16px" src="{{book.Cover}}" alt="Cover for {{book.Title}}" />
        </td>
    </tr>
    {% endfor %}
</tbody>

</table>
