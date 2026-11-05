/* Publication rendering. Data source: data/papers.json
   Edit that JSON to add a paper — no build step needed. */

(function () {
  'use strict';

  var ME = 'Bolun Zheng';

  /* 每个刊物的专属色，类名在 style.css 的 .venue-badge.vb-* 里定义 */
  var VENUE_CLASS = {
    'IEEE TPAMI': 'tpami',
    'IEEE TIP':   'tip',
    'IEEE TCSVT': 'tcsvt',
    'IEEE TMM':   'tmm',
    'IEEE TCyb':  'tcyb',
    'IEEE TIFS':  'tifs',
    'IEEE TGRS':  'tgrs',
    'IJCV':       'ijcv',
    'CVPR':       'cvpr',
    'AAAI':       'aaai',
    'ACM MM':     'acmmm',
    'IEEE TCI':   'tci',
    'ACM TOMM':   'tomm'
  };

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
    var c = VENUE_CLASS[p.venue];
    return 'venue-badge' + (c ? ' vb-' + c : '');
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

  /* DOI 按钮在前，Project 按钮紧随其后 */
  function actionsHTML(p) {
    var out = [];
    if (p.url) {
      out.push('<a class="btn" href="' + p.url + '" target="_blank" rel="noopener">' +
        actionLabel(p) + '</a>');
    }
    if (p.project) {
      out.push('<a class="btn btn-project" href="' + p.project +
        '" target="_blank" rel="noopener">Project</a>');
    }
    return out.length ? '<div class="actions">' + out.join('') + '</div>' : '';
  }

  function pubHTML(p) {
    var title = p.url
      ? '<a href="' + p.url + '" target="_blank" rel="noopener">' + esc(p.title) + '</a>'
      : esc(p.title);

    var actions = actionsHTML(p);

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

  /* ---------------- homepage: selected only, reverse chronological ---------------- */
  function initSelected(papers) {
    var el = document.getElementById('selected-pubs');
    if (!el) return;
    var list = papers.filter(function (p) { return p.selected; });
    /* rank 为手工指定顺序（1 为最新）；缺省时按年份倒序 */
    list.sort(function (a, b) {
      var ra = a.rank || 999, rb = b.rank || 999;
      if (ra !== rb) return ra - rb;
      return b.year - a.year;
    });
    el.innerHTML = list.map(pubHTML).join('');
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
