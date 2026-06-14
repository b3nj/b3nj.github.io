---
layout: page
title: Books
permalink: /books/
---

<h2>Books that I read</h2>
<h1>My Library</h1>
<div class="book-grid">
  {% for entry in site.data.books %}
    {% assign isbn = entry | first %}
    {% assign book = entry[isbn] %}
    <a href="/books/{{ book.identifiers.isbn_13[0] }}/" class="book-card">
      {% if book.cover %}
        <img src="{{ book.cover.medium }}" alt="{{ book.title }}">
      {% endif %}
      <h3>{{ book.title }}</h3>
      {% if book.authors %}
        <p>{{ book.authors | map: "name" | join: ", " }}</p>
      {% endif %}
    </a>
  {% endfor %}
</div>