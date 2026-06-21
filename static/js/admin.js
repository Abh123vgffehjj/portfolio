/* ================================================================
   Admin Dashboard JavaScript
   ================================================================ */

'use strict';

// ── Confirm deletions ─────────────────────────────────────────────
document.querySelectorAll('form[data-confirm]').forEach(form => {
  form.addEventListener('submit', e => {
    if (!confirm(form.dataset.confirm || 'Are you sure?')) {
      e.preventDefault();
    }
  });
});

// ── Auto-dismiss flash alerts ─────────────────────────────────────
function autoDismissAlerts() {
  document.querySelectorAll('.alert').forEach(alert => {
    setTimeout(() => {
      alert.style.transition = 'opacity 0.5s ease';
      alert.style.opacity = '0';
      setTimeout(() => alert.remove(), 500);
    }, 4000);
  });
}

// ── Mobile sidebar ────────────────────────────────────────────────
function initMobileSidebar() {
  const toggle = document.getElementById('sidebar-toggle');
  const sidebar = document.getElementById('sidebar');
  if (!toggle || !sidebar) return;

  // Show toggle on small screens
  if (window.innerWidth <= 768) {
    toggle.style.display = 'block';
  }

  toggle.addEventListener('click', () => {
    sidebar.classList.toggle('open');
  });

  // Close sidebar when clicking outside on mobile
  document.addEventListener('click', e => {
    if (window.innerWidth <= 768 &&
        sidebar.classList.contains('open') &&
        !sidebar.contains(e.target) &&
        !toggle.contains(e.target)) {
      sidebar.classList.remove('open');
    }
  });
}

// ── Proficiency range input label ─────────────────────────────────
function initRangeInputs() {
  document.querySelectorAll('input[type="range"]').forEach(input => {
    const labelId = input.getAttribute('data-label') || input.id + '-val';
    const label = document.getElementById(labelId);
    if (label) {
      label.textContent = input.value + '%';
      input.addEventListener('input', () => {
        label.textContent = input.value + '%';
      });
    }
  });
}

// ── Table row click to expand message ────────────────────────────
function initExpandableRows() {
  document.querySelectorAll('tr[data-message]').forEach(row => {
    row.style.cursor = 'pointer';
    row.addEventListener('click', () => {
      const msg = row.dataset.message;
      if (msg) alert(msg);
    });
  });
}

// ── Skill proficiency range display ───────────────────────────────
(function() {
  const range = document.getElementById('prof-range');
  const val = document.getElementById('prof-val');
  if (range && val) {
    range.addEventListener('input', () => {
      val.textContent = range.value + '%';
    });
  }
})();

// ── File drag-and-drop highlight ─────────────────────────────────
function initDragDrop() {
  const area = document.getElementById('upload-area');
  if (!area) return;

  ['dragenter', 'dragover'].forEach(evt => {
    area.addEventListener(evt, e => {
      e.preventDefault();
      area.classList.add('drag-over');
    });
  });

  ['dragleave', 'drop'].forEach(evt => {
    area.addEventListener(evt, () => area.classList.remove('drag-over'));
  });
}

// ── Copy-to-clipboard for email addresses ─────────────────────────
document.querySelectorAll('[data-copy]').forEach(el => {
  el.addEventListener('click', () => {
    navigator.clipboard.writeText(el.dataset.copy).then(() => {
      const original = el.textContent;
      el.textContent = 'Copied!';
      setTimeout(() => { el.textContent = original; }, 1500);
    });
  });
});

// ── Charts for analytics page ─────────────────────────────────────
function initAnalyticsChart() {
  const canvas = document.getElementById('visitor-chart');
  if (!canvas) return;

  // Data is embedded by the template
  const labels = window.CHART_LABELS || [];
  const data = window.CHART_DATA || [];

  if (!labels.length) return;

  // Simple SVG bar chart (no external lib needed)
  const max = Math.max(...data, 1);
  const width = canvas.offsetWidth || 600;
  const height = 200;
  const barW = Math.floor((width - 40) / labels.length) - 4;

  let svg = `<svg viewBox="0 0 ${width} ${height}" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:${height}px">`;

  data.forEach((val, i) => {
    const barH = Math.floor((val / max) * (height - 40));
    const x = 20 + i * (barW + 4);
    const y = height - 20 - barH;

    svg += `<rect x="${x}" y="${y}" width="${barW}" height="${barH}" rx="3"
      fill="url(#grad)" opacity="0.85"/>`;
    svg += `<text x="${x + barW / 2}" y="${height - 4}" text-anchor="middle"
      font-size="9" fill="#888">${labels[i].slice(5)}</text>`;
    if (val > 0) {
      svg += `<text x="${x + barW / 2}" y="${y - 3}" text-anchor="middle"
        font-size="9" fill="#FF3040">${val}</text>`;
    }
  });

  svg += `<defs>
    <linearGradient id="grad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#E11D2E"/>
      <stop offset="100%" stop-color="#8B0000"/>
    </linearGradient>
  </defs></svg>`;

  canvas.innerHTML = svg;
}

// ── Init ──────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  autoDismissAlerts();
  initMobileSidebar();
  initRangeInputs();
  initExpandableRows();
  initDragDrop();
  initAnalyticsChart();
});
