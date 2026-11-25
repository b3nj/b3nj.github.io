---
layout: page
title: My Library
permalink: /books/
---
<style>
.lib-toolbar { display: flex; flex-wrap: wrap; gap: .6rem; margin: 1rem 0 .8rem; }
.lib-toolbar input, .lib-toolbar select { padding: .55rem .8rem; font: inherit; color: inherit; background: transparent; border: 1px solid color-mix(in srgb, currentColor 25%, transparent); border-radius: .6rem; }
.lib-toolbar input { flex: 1 1 14rem; }
.lib-count { margin: 0 0 .8rem; font-size: .9rem; opacity: .7; }
.lib-list { list-style: none; margin: 0; padding: 0; display: grid; gap: .7rem; }
.lib-item { margin: 0; padding: 0; }
.lib-item a { display: flex; gap: 1rem; align-items: center; padding: .8rem 1rem; color: inherit; text-decoration: none; border: 1px solid color-mix(in srgb, currentColor 14%, transparent); border-radius: .8rem; box-shadow: none; transition: transform .15s, border-color .15s, background .15s; }
.lib-item a:hover { transform: translateY(-1px); border-color: hsl(var(--h) 55% 50%); background: color-mix(in srgb, hsl(var(--h) 55% 50%) 8%, transparent); }
.lib-badge { flex: none; width: 2.8rem; height: 3.6rem; display: grid; place-items: center; font-size: 1.3rem; font-weight: 700; color: #fff; background: hsl(var(--h) 55% 45%); border-radius: .3rem .6rem .6rem .3rem; box-shadow: inset .3rem 0 0 rgb(0 0 0 / .2); }
.lib-body { flex: 1; min-width: 0; }
.lib-title { margin: 0; font-size: 1.05rem; line-height: 1.3; }
.lib-author { margin: .15rem 0 0; opacity: .8; }
.lib-meta { display: flex; flex-wrap: wrap; gap: .35rem; margin: .45rem 0 0; font-size: .78rem; }
.lib-meta span { padding: .1rem .55rem; border-radius: 999px; background: color-mix(in srgb, currentColor 10%, transparent); }
.lib-empty { opacity: .7; }
@media (min-width: 52rem) { .lib-list { grid-template-columns: 1fr 1fr; } }
</style>
{% assign n = site.data.books.size %}
{% assign books = site.data.books | reverse %}
<div class="lib-toolbar">
<input type="search" id="lib-search" placeholder="Search title, author, publisher…" aria-label="Search books" autocomplete="off">
<select id="lib-sort" aria-label="Sort books">
<option value="added">Recently added</option>
<option value="title">Title A–Z</option>
<option value="author">Author A–Z</option>
<option value="year">Year (newest first)</option>
</select>
</div>
<p class="lib-count" id="lib-count">{{ n }} books</p>
<ul class="lib-list" id="lib-list">
{% for book in books %}
{%- assign authors = book.authors | join: ", " -%}
{%- assign last = book.authors.first | split: " " | last -%}
{%- assign year = book.publishedDate | slice: 0, 4 -%}
{%- assign hue = book.title.size | times: 37 | modulo: 360 -%}
{%- assign initial = book.title | slice: 0 | upcase -%}
<li class="lib-item" data-added="{{ n | minus: forloop.index0 }}" data-title="{{ book.title | downcase | escape }}" data-author="{{ last | downcase | escape }}" data-year="{{ year }}" data-search="{{ book.title | append: ' ' | append: authors | append: ' ' | append: book.publisher | append: ' ' | append: year | downcase | escape }}">
<a href="/books/{{ book.slug }}/" style="--h: {{ hue }}">
<span class="lib-badge" aria-hidden="true">{{ initial }}</span>
<div class="lib-body">
<h3 class="lib-title">{{ book.title }}</h3>
{% if authors != "" %}<p class="lib-author">{{ authors }}</p>{% endif %}
<div class="lib-meta">
{% if book.publisher %}<span>{{ book.publisher }}</span>{% endif %}
{% if year != "" %}<span>{{ year }}</span>{% endif %}
{% if book.pageCount %}<span>{{ book.pageCount }} p.</span>{% endif %}
{% if book.language %}<span>{{ book.language | upcase }}</span>{% endif %}
</div>
</div>
</a>
</li>
{% endfor %}
</ul>
<p class="lib-empty" id="lib-empty" style="display:none">No books match your search.</p>
<script>
(function () {
  const list = document.getElementById('lib-list');
  const items = Array.from(list.children);
  const search = document.getElementById('lib-search');
  const sort = document.getElementById('lib-sort');
  const count = document.getElementById('lib-count');
  const empty = document.getElementById('lib-empty');
  const total = items.length;
  const norm = s => s.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase();
  const strip = s => norm(s).replace(/^(l['’]|le |la |les |un |une |des |the |a |an )/, '');
  const cmp = new Intl.Collator('fr', { sensitivity: 'base' }).compare;
  const byTitle = (a, b) => cmp(strip(a.dataset.title), strip(b.dataset.title));
  const sorters = {
    added: (a, b) => b.dataset.added - a.dataset.added,
    title: byTitle,
    author: (a, b) => cmp(a.dataset.author, b.dataset.author) || byTitle(a, b),
    year: (a, b) => (parseInt(b.dataset.year) || 0) - (parseInt(a.dataset.year) || 0) || byTitle(a, b)
  };
  function render() {
    const q = norm(search.value.trim());
    let visible = 0;
    items.sort(sorters[sort.value]).forEach(li => {
      const match = !q || norm(li.dataset.search).includes(q);
      li.hidden = !match;
      if (match) visible++;
      list.appendChild(li);
    });
    count.textContent = q ? visible + ' of ' + total + ' books' : total + ' books';
    empty.style.display = visible ? 'none' : '';
  }
  search.addEventListener('input', render);
  sort.addEventListener('change', render);
  render();
})();
</script>
