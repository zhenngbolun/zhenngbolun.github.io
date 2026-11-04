/* Publication rendering. Data source: data/papers.json
   Edit that JSON to add a paper — no build step needed. */

(function () {
  'use strict';

  var ME = 'Bolun Zheng';

  /* venues rendered in solid blue; everything else falls back to grey */
  var TIER1 = [
    'IEEE TPAMI', 'IEEE TIP', 'IEEE TCSVT', 'IEEE TMM', 'IEEE TCyb',
    'IEEE TIFS', 'IEEE TGRS', 'IJCV', 'CVPR', 'AAAI', 'ACM MM',
    'IEEE TCI', 'ACM TOMM'
  ];

  function esc(s) {
    return String(s).replace(/[&<>"]/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c];
    });
  }

  function authorLine(authors) {
    return authors.map(function (a) {
      return a === ME ? '<b>' + esc(a) + '</b>' : esc(a);
    }).join(', ');
  }

  function badgeClass(p) {
    if (p.type === 'preprint') return 'venue-badge pre';
    return TIER1.indexOf(p.venue) !== -1 ? 'venue-badge' : 'venue-badge tier2';
  }

  function badge(p) {
    var cls = badgeClass(p);
    var label = esc(p.venue);
    if (!p.url) return '<span class="' + cls + '">' + label + '</span>';
    return '<a class="' + cls + '" href="' + p.url + '" target="_blank" rel="noopener">' + label + '</a>';
  }

  function actionLabel(p) {
    return p.venue === 'arXiv' ? 'arXiv' : 'DOI';
  }

  function pubHTML(p) {
    var title = p.url
      ? '<a href="' + p.url + '" target="_blank" rel="noopener">' + esc(p.title) + '</a>'
      : esc(p.title);

    var actions = p.url
      ? '<div class="actions"><a class="btn" href="' + p.url + '" target="_blank" rel="noopener">' +
        actionLabel(p) + '</a></div>'
      : '';

    return '<li class="pub">' +
        '<div>' + badge(p) + '</div>' +
        '<div class="pub-body">' +
          '<div class="title">' + title + '</div>' +
          '<div class="authors">' + authorLine(p.authors) + '</div>' +
          '<div class="periodical"><em>' + esc(p.venue_full) + '</em>, ' + p.year + '</div>' +
          actions +
        '</div>' +
      '</li>';
  }

  function load(cb) {
    fetch('data/papers.json')
      .then(function (r) {
        if (!r.ok) throw new Error(r.status);
        return r.json();
      })
      .then(cb)
      .catch(function () {
        ['selected-pubs', 'pub-list'].forEach(function (id) {
          var el = document.getElementById(id);
          if (el) el.innerHTML = '<p class="list-meta">Publication list could not be loaded. ' +
            'Serve this site over HTTP — see README.</p>';
        });
      });
  }

  /* ---------------- homepage: selected only ---------------- */
  function initSelected(papers) {
    var el = document.getElementById('selected-pubs');
    if (!el) return;
    el.innerHTML = papers.filter(function (p) { return p.selected; }).map(pubHTML).join('');
  }

  /* ---------------- publications page: grouped + filter ---------------- */
  function initFull(papers) {
    var host = document.getElementById('pub-list');
    if (!host) return;

    var note = document.getElementById('pub-count');
    var bar = document.getElementById('pub-filter');
    var state = 'all';

    function apply() {
      var list = papers.filter(function (p) {
        if (state === 'all') return true;
        if (state === 'selected') return p.selected;
        return p.type === state;
      });

      if (!list.length) {
        host.innerHTML = '<p class="list-meta">No entries in this category.</p>';
        note.textContent = '0 entries';
        return;
      }

      var years = [];
      list.forEach(function (p) {
        if (years.indexOf(p.year) === -1) years.push(p.year);
      });
      years.sort(function (a, b) { return b - a; });

      host.innerHTML = years.map(function (y) {
        var items = list.filter(function (p) { return p.year === y; });
        return '<div class="year-head">' + y + '</div><ol class="bib">' +
          items.map(pubHTML).join('') + '</ol>';
      }).join('');

      note.textContent = list.length + (list.length === 1 ? ' entry' : ' entries');
    }

    if (bar) {
      bar.addEventListener('click', function (e) {
        var b = e.target.closest('button');
        if (!b) return;
        bar.querySelectorAll('button').forEach(function (x) { x.classList.remove('on'); });
        b.classList.add('on');
        state = b.dataset.filter;
        apply();
      });
    }
    apply();
  }

  load(function (papers) {
    initSelected(papers);
    initFull(papers);
  });
})();
