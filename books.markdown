---
layout: page
title: My Library
permalink: /books/
---
<link rel="stylesheet" href="{{ '/assets/css/books.css' | relative_url }}">
<p>{{ site.data.books.size }} books</p>
<input type="text" id="book-search" placeholder="Search by title or author..." class="book-search">
<div class="book-grid" id="book-grid">
{% assign sorted_books = site.data.books | sort: "title" %}
{% for book in sorted_books %}
{% assign authors = book.authors | join: ", " %}
{% assign slug = book.title | downcase | replace: " ", "-" | replace: "'", "" %}
<div class="book-card" data-title="{{ book.title | downcase }}" data-authors="{{ authors | downcase }}">
<a href="/books/{{ slug }}/">
{% if book.cover_local %}
<img src="{{ book.cover_local }}" alt="{{ book.title }}" loading="lazy"
onerror="this.src='{{ book.imageLinks.thumbnail | replace: "http://", "https://" }}'">
{% elsif book.imageLinks.thumbnail %}
<img src="{{ book.imageLinks.thumbnail | replace: "http://", "https://" }}" alt="{{ book.title }}" loading="lazy">
{% else %}
<div class="book-cover-placeholder">No cover</div>
{% endif %}
<h3>{{ book.title }}</h3>
{% if authors != "" %}
<p class="book-author">{{ authors }}</p>
{% endif %}
</a>
</div>
{% endfor %}
</div>
<p id="no-results" style="display:none">No books match your search.</p>
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
      card.dataset.authors.includes(query)