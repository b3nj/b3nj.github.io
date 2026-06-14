---
layout: page
title: My Library
permalink: /books/
---
<link rel="stylesheet" href="{{ '/assets/css/books.css' | relative_url }}">

<p>{{ site.data.books.size }} books</p>

<input type="text" id="book-search" placeholder="Search by title or author..." class="book-search">

<div class="book-grid" id="book-grid">
  {% assign sorted_books = "" | split: "" %}
  {% for entry in site.data.books %}
    {% for pair in entry %}
      {% assign sorted_books = sorted_books | push: pair[1] %}
    {% endfor %}
  {% endfor %}
  {% assign sorted_books = sorted_books | sort: "title" %}

  {% for book in sorted_books %}
    {% assign isbn = book.identifiers.isbn_13[0] | default: book.identifiers.isbn_10[0] %}
    {% assign authors = book.authors | map: "name" | join: ", " %}
    <a href="/books/{{ isbn }}/"
       class="book-card"
       data-title="{{ book.title | downcase }}"
       data-authors="{{ authors | downcase }}">
      {% if book.cover %}
        <img src="{{ book.cover.medium }}" alt="{{ book.title }}" loading="lazy">
      {% else %}
        <div class="book-cover-placeholder">No cover</div>
      {% endif %}
      <h3>{{ book.title }}</h3>
      {% if authors != "" %}
        <p class="book-author">{{ authors }}</p>
      {% endif %}
    </a>
  {% endfor %}
</div>

<p id="no-results" style="display:none;">No books match your search.</p>

<script>
  const searchInput = document.getElementById('book-search');
  const cards = document.querySelectorAll('.book-card');
  const noResults = document.getElementById('no-results');

  searchInput.addEventListener('input', () => {
    const query = searchInput.value.trim().toLowerCase();
    let visibleCount = 0;

    cards.forEach(card => {
      const matches =
        card.dataset.title.includes(query) ||
        card.dataset.authors.includes(query);
      card.style.display = matches ? '' : 'none';
      if (matches) visibleCount++;
    });

    noResults.style.display = visibleCount === 0 ? '' : 'none';
  });
</script>