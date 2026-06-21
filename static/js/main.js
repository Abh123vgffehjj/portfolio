/* ================================================================
   Spider-Verse Portfolio – Main JavaScript
   ================================================================ */

'use strict';

// ── Canvas Web Animation ──────────────────────────────────────────
class SpiderWebCanvas {
  constructor(canvasId) {
    this.canvas = document.getElementById(canvasId);
    if (!this.canvas) return;
    this.ctx = this.canvas.getContext('2d');
    this.particles = [];
    this.mouse = { x: null, y: null };
    this.animFrame = null;
    this.init();
  }

  init() {
    this.resize();
    this.createParticles();
    this.bindEvents();
    this.animate();
  }

  resize() {
    this.canvas.width = window.innerWidth;
    this.canvas.height = window.innerHeight;
  }

  createParticles() {
    const count = Math.floor((window.innerWidth * window.innerHeight) / 12000);
    this.particles = [];
    for (let i = 0; i < Math.min(count, 80); i++) {
      this.particles.push({
        x: Math.random() * this.canvas.width,
        y: Math.random() * this.canvas.height,
        vx: (Math.random() - 0.5) * 0.4,
        vy: (Math.random() - 0.5) * 0.4,
        r: Math.random() * 2 + 1,
        alpha: Math.random() * 0.5 + 0.2,
      });
    }
  }

  draw() {
    const ctx = this.ctx;
    ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

    // Move and draw particles
    this.particles.forEach(p => {
      p.x += p.vx;
      p.y += p.vy;

      if (p.x < 0 || p.x > this.canvas.width) p.vx *= -1;
      if (p.y < 0 || p.y > this.canvas.height) p.vy *= -1;

      ctx.beginPath();
      ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(225,29,46,${p.alpha})`;
      ctx.fill();
    });

    // Draw web lines between close particles
    for (let i = 0; i < this.particles.length; i++) {
      for (let j = i + 1; j < this.particles.length; j++) {
        const dx = this.particles[i].x - this.particles[j].x;
        const dy = this.particles[i].y - this.particles[j].y;
        const dist = Math.sqrt(dx * dx + dy * dy);
        if (dist < 130) {
          const alpha = (1 - dist / 130) * 0.25;
          ctx.beginPath();
          ctx.moveTo(this.particles[i].x, this.particles[i].y);
          ctx.lineTo(this.particles[j].x, this.particles[j].y);
          ctx.strokeStyle = `rgba(225,29,46,${alpha})`;
          ctx.lineWidth = 0.6;
          ctx.stroke();
        }
      }
    }

    // Mouse interaction
    if (this.mouse.x !== null) {
      this.particles.forEach(p => {
        const dx = this.mouse.x - p.x;
        const dy = this.mouse.y - p.y;
        const dist = Math.sqrt(dx * dx + dy * dy);
        if (dist < 150) {
          const alpha = (1 - dist / 150) * 0.5;
          ctx.beginPath();
          ctx.moveTo(p.x, p.y);
          ctx.lineTo(this.mouse.x, this.mouse.y);
          ctx.strokeStyle = `rgba(255,48,64,${alpha})`;
          ctx.lineWidth = 0.8;
          ctx.stroke();
        }
      });
    }
  }

  animate() {
    this.draw();
    this.animFrame = requestAnimationFrame(() => this.animate());
  }

  bindEvents() {
    window.addEventListener('resize', () => {
      this.resize();
      this.createParticles();
    }, { passive: true });

    window.addEventListener('mousemove', e => {
      this.mouse.x = e.clientX;
      this.mouse.y = e.clientY;
    }, { passive: true });
  }

  destroy() {
    if (this.animFrame) cancelAnimationFrame(this.animFrame);
  }
}


// ── Typing Animation ──────────────────────────────────────────────
class Typer {
  constructor(el, words, speed = 100, pause = 2000) {
    this.el = el;
    this.words = words;
    this.speed = speed;
    this.pause = pause;
    this.wordIdx = 0;
    this.charIdx = 0;
    this.deleting = false;
    if (this.el) this.tick();
  }

  tick() {
    const word = this.words[this.wordIdx];
    this.el.textContent = this.deleting
      ? word.substring(0, this.charIdx - 1)
      : word.substring(0, this.charIdx + 1);

    this.charIdx += this.deleting ? -1 : 1;

    let delay = this.deleting ? this.speed / 2 : this.speed;

    if (!this.deleting && this.charIdx === word.length) {
      delay = this.pause;
      this.deleting = true;
    } else if (this.deleting && this.charIdx === 0) {
      this.deleting = false;
      this.wordIdx = (this.wordIdx + 1) % this.words.length;
    }

    setTimeout(() => this.tick(), delay);
  }
}


// ── Scroll Reveal ─────────────────────────────────────────────────
function initScrollReveal() {
  const observer = new IntersectionObserver(
    entries => entries.forEach(e => {
      if (e.isIntersecting) {
        e.target.classList.add('visible');
      }
    }),
    { threshold: 0.1, rootMargin: '0px 0px -50px 0px' }
  );

  document.querySelectorAll('.reveal, .reveal-left, .timeline-item').forEach(el => observer.observe(el));
}


// ── Skill Bars Animation ──────────────────────────────────────────
function animateSkillBars(container) {
  container.querySelectorAll('.skill-bar-fill').forEach(fill => {
    const pct = fill.dataset.pct || '75';
    fill.style.width = pct + '%';
  });
}

function initSkillBars() {
  // Called after dynamic render; animate any already-visible bars
  const section = document.getElementById('skills');
  if (!section) return;

  const observer = new IntersectionObserver(
    entries => entries.forEach(e => {
      if (e.isIntersecting) animateSkillBars(e.target);
    }),
    { threshold: 0.05 }
  );
  observer.observe(section);
  // Also animate immediately if already in view
  if (section.getBoundingClientRect().top < window.innerHeight) {
    animateSkillBars(section);
  }
}


// ── Scroll Progress ───────────────────────────────────────────────
function initScrollProgress() {
  const bar = document.getElementById('scroll-progress');
  const btt = document.getElementById('back-to-top');
  const nav = document.getElementById('navbar');

  window.addEventListener('scroll', () => {
    const scrollTop = window.scrollY;
    const docHeight = document.documentElement.scrollHeight - window.innerHeight;
    const pct = docHeight > 0 ? (scrollTop / docHeight) * 100 : 0;

    if (bar) bar.style.width = pct + '%';
    if (btt) btt.classList.toggle('show', scrollTop > 300);
    if (nav) nav.classList.toggle('scrolled', scrollTop > 50);
  }, { passive: true });

  if (btt) {
    btt.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));
  }
}


// ── Counter Animation ─────────────────────────────────────────────
function animateCounter(el) {
  const target = parseInt(el.dataset.target, 10);
  const duration = 1800;
  const step = target / (duration / 16);
  let current = 0;

  const timer = setInterval(() => {
    current += step;
    if (current >= target) {
      el.textContent = target.toLocaleString();
      clearInterval(timer);
    } else {
      el.textContent = Math.floor(current).toLocaleString();
    }
  }, 16);
}

function initCounters() {
  const observer = new IntersectionObserver(
    entries => entries.forEach(e => {
      if (e.isIntersecting) {
        animateCounter(e.target);
        observer.unobserve(e.target);
      }
    }),
    { threshold: 0.3 }
  );

  document.querySelectorAll('[data-target]').forEach(el => observer.observe(el));
}


// ── Navigation ────────────────────────────────────────────────────
function initNav() {
  const hamburger = document.getElementById('hamburger');
  const mobileMenu = document.getElementById('mobile-menu');
  const overlay = document.getElementById('overlay');
  const closeBtn = document.getElementById('mobile-close');

  function openMenu() {
    mobileMenu?.classList.add('open');
    overlay?.classList.add('show');
    document.body.style.overflow = 'hidden';
  }

  function closeMenu() {
    mobileMenu?.classList.remove('open');
    overlay?.classList.remove('show');
    document.body.style.overflow = '';
  }

  hamburger?.addEventListener('click', openMenu);
  closeBtn?.addEventListener('click', closeMenu);
  overlay?.addEventListener('click', closeMenu);

  document.querySelectorAll('.mobile-nav-links a').forEach(a => {
    a.addEventListener('click', closeMenu);
  });
}


// ── Theme Toggle ──────────────────────────────────────────────────
function initTheme() {
  const btn = document.getElementById('theme-toggle');
  const saved = localStorage.getItem('theme') || 'dark';
  if (saved === 'light') document.documentElement.setAttribute('data-theme', 'light');

  btn?.addEventListener('click', () => {
    const current = document.documentElement.getAttribute('data-theme');
    const next = current === 'light' ? 'dark' : 'light';
    document.documentElement.setAttribute('data-theme', next);
    localStorage.setItem('theme', next);
    btn.innerHTML = next === 'light' ? '🌙' : '☀️';
  });

  if (saved === 'light' && btn) btn.innerHTML = '🌙';
}


// ── API Loader ────────────────────────────────────────────────────
async function apiFetch(endpoint) {
  try {
    const res = await fetch('/api' + endpoint);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return await res.json();
  } catch (e) {
    console.warn('API error:', endpoint, e.message);
    return null;
  }
}


// ── Projects Section ──────────────────────────────────────────────
let allProjects = [];
let activeFilter = 'All';

async function loadProjects() {
  const data = await apiFetch('/projects');
  if (!data) return;
  allProjects = data;
  renderProjectFilters();
  renderProjects(data);
}

function renderProjectFilters() {
  const container = document.getElementById('project-filters');
  if (!container) return;

  const categories = ['All', ...new Set(allProjects.map(p => p.category).filter(Boolean))];
  container.innerHTML = categories.map(cat =>
    `<button class="filter-btn ${cat === 'All' ? 'active' : ''}" data-cat="${cat}">${cat}</button>`
  ).join('');

  container.querySelectorAll('.filter-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      container.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      activeFilter = btn.dataset.cat;
      const filtered = activeFilter === 'All'
        ? allProjects
        : allProjects.filter(p => p.category === activeFilter);
      renderProjects(filtered);
    });
  });
}

function renderProjects(projects) {
  const grid = document.getElementById('projects-grid');
  if (!grid) return;

  if (!projects.length) {
    grid.innerHTML = '<div class="col-12 text-center"><p style="color:var(--gray);padding:2rem">No projects found.</p></div>';
    return;
  }

  grid.innerHTML = projects.map(p => {
    const techs = Array.isArray(p.technologies)
      ? p.technologies
      : (p.technologies || '').split(',').map(t => t.trim()).filter(Boolean);

    const features = Array.isArray(p.features)
      ? p.features
      : (p.features || '').split('\n').map(f => f.trim()).filter(Boolean).slice(0, 4);

    const techTags = techs.slice(0, 5).map(t =>
      `<span class="tech-tag">${t}</span>`
    ).join('');

    const featureItems = features.map(f =>
      `<li>${f}</li>`
    ).join('');

    const achievement = p.achievement
      ? `<div class="project-achievement">${p.achievement}</div>` : '';

    const links = [
      p.github_url ? `<a href="${p.github_url}" target="_blank" rel="noopener" class="btn-ghost btn-sm">GitHub</a>` : '',
      p.live_url ? `<a href="${p.live_url}" target="_blank" rel="noopener" class="btn-primary btn-sm">Live Demo</a>` : '',
    ].filter(Boolean).join('');

    return `
      <div class="col-lg-4 col-md-6 mb-4 reveal">
        <div class="project-card">
          <div class="project-card-header">
            <div class="project-category-badge">${p.category || 'Project'}</div>
            <div class="project-title">${p.title}</div>
            ${p.is_featured ? '<span class="featured-badge">Featured</span>' : ''}
          </div>
          <div class="project-card-body">
            <p class="project-description">${p.description}</p>
            <div class="tech-tags">${techTags}</div>
            ${featureItems ? `<ul class="project-features">${featureItems}</ul>` : ''}
            ${achievement}
          </div>
          ${links ? `<div class="project-card-footer">${links}</div>` : ''}
        </div>
      </div>`;
  }).join('');

  // Re-observe reveal elements
  document.querySelectorAll('.reveal:not(.visible)').forEach(el => {
    if (el.getBoundingClientRect().top < window.innerHeight) {
      el.classList.add('visible');
    }
  });
  initScrollReveal();
}

// Search
function initProjectSearch() {
  const searchInput = document.getElementById('project-search');
  if (!searchInput) return;

  searchInput.addEventListener('input', () => {
    const q = searchInput.value.toLowerCase().trim();
    const filtered = allProjects.filter(p =>
      (p.title || '').toLowerCase().includes(q) ||
      (p.description || '').toLowerCase().includes(q) ||
      (p.technologies || '').toLowerCase().includes(q)
    );
    if (activeFilter !== 'All') {
      renderProjects(filtered.filter(p => p.category === activeFilter));
    } else {
      renderProjects(filtered);
    }
  });
}


// ── Skills Section ────────────────────────────────────────────────
async function loadSkills() {
  const data = await apiFetch('/skills');
  if (!data) return;

  const { grouped } = data;
  const tabsContainer = document.getElementById('skill-tabs');
  const gridContainer = document.getElementById('skills-grid');
  if (!tabsContainer || !gridContainer) return;

  const categories = Object.keys(grouped);
  tabsContainer.innerHTML = ['All', ...categories].map((cat, i) =>
    `<button class="skill-tab ${i === 0 ? 'active' : ''}" data-cat="${cat}">${cat}</button>`
  ).join('');

  function renderSkills(category) {
    let skills = category === 'All'
      ? Object.values(grouped).flat()
      : (grouped[category] || []);

    gridContainer.innerHTML = `<div class="row g-3">
      ${skills.map(s => `
        <div class="col-lg-3 col-md-4 col-sm-6 reveal">
          <div class="skill-card">
            <div class="skill-name">${s.name}</div>
            <div class="skill-bar">
              <div class="skill-bar-fill" data-pct="${s.proficiency}" style="width:${s.proficiency}%"></div>
            </div>
            <div class="skill-pct">${s.proficiency}%</div>
          </div>
        </div>
      `).join('')}
    </div>`;
    initScrollReveal();
  }

  renderSkills('All');

  tabsContainer.querySelectorAll('.skill-tab').forEach(btn => {
    btn.addEventListener('click', () => {
      tabsContainer.querySelectorAll('.skill-tab').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      renderSkills(btn.dataset.cat);
    });
  });

  // Animate bars already in view after first render
  setTimeout(() => animateSkillBars(gridContainer), 100);
}


// ── Certifications ────────────────────────────────────────────────
async function loadCertifications() {
  const data = await apiFetch('/certifications');
  if (!data) return;

  const grid = document.getElementById('certs-grid');
  if (!grid) return;

  const icons = ['🏅', '🎖️', '📜', '🥇', '🎓'];
  grid.innerHTML = `<div class="row g-4">
    ${data.map((c, i) => `
      <div class="col-lg-4 col-md-6 reveal">
        <div class="cert-card">
          <span class="cert-icon">${icons[i % icons.length]}</span>
          <div class="cert-name">${c.name}</div>
          <div class="cert-issuer">${c.issuer}</div>
          ${c.issue_date ? `<div class="cert-date">${c.issue_date}</div>` : ''}
          ${c.description ? `<p style="color:var(--gray);font-size:0.85rem;margin-top:0.75rem">${c.description}</p>` : ''}
        </div>
      </div>
    `).join('')}
  </div>`;
  initScrollReveal();
}


// ── Achievements ──────────────────────────────────────────────────
async function loadAchievements() {
  const data = await apiFetch('/achievements');
  if (!data) return;

  const timeline = document.getElementById('achievements-timeline');
  if (!timeline) return;

  const icons = { award: '🏆', star: '⭐', briefcase: '💼', trophy: '🥇' };
  timeline.innerHTML = data.map(a => `
    <div class="timeline-item">
      <div class="timeline-dot"></div>
      <div class="timeline-card">
        <div class="timeline-date">${icons[a.icon] || '🎯'} ${a.date || ''}</div>
        <div class="timeline-title">${a.title}</div>
        ${a.description ? `<div class="timeline-desc">${a.description}</div>` : ''}
      </div>
    </div>
  `).join('');
  initScrollReveal();
}


// ── Profile / About ───────────────────────────────────────────────
async function loadProfile() {
  const data = await apiFetch('/profile');
  if (!data) return;

  // Typed roles
  const roles = Array.isArray(data.animated_roles)
    ? data.animated_roles
    : ['AI Developer', 'IoT Innovator', 'Data Enthusiast', 'Full-Stack Developer'];

  const typedEl = document.getElementById('typed-text');
  if (typedEl) new Typer(typedEl, roles, 80, 2200);

  // Update contact links if present
  if (data.email) {
    document.querySelectorAll('a[href^="mailto:"]').forEach(a => {
      a.href = 'mailto:' + data.email;
      const val = a.querySelector('.contact-detail-value');
      if (val) val.textContent = data.email;
    });
  }
  if (data.linkedin) {
    document.querySelectorAll('a[href*="linkedin.com"]').forEach(a => {
      a.href = data.linkedin;
    });
  }
  if (data.github) {
    document.querySelectorAll('a[href*="github.com"]').forEach(a => {
      a.href = data.github;
    });
  }
}


// ── Update hero stats from live API data ──────────────────────────
async function loadHeroStats() {
  const [projects, certs, achievements] = await Promise.all([
    apiFetch('/projects'),
    apiFetch('/certifications'),
    apiFetch('/achievements'),
  ]);

  const stats = document.querySelectorAll('.stat-number[data-target]');
  const values = [
    projects ? projects.length : 3,
    certs ? certs.length : 3,
    achievements ? achievements.length : 4,
    854, // CGPA ×100 — fixed value
  ];

  stats.forEach((el, i) => {
    if (values[i] !== undefined) {
      el.dataset.target = values[i];
      // Re-trigger counter if already visible
      if (el.getBoundingClientRect().top < window.innerHeight) {
        animateCounter(el);
      }
    }
  });
}


// ── Education ─────────────────────────────────────────────────────
async function loadEducation() {
  const data = await apiFetch('/education');
  if (!data || !data.length) return;

  const edu = data[0];
  const degreeEl = document.getElementById('edu-degree');
  const instEl = document.getElementById('edu-institution');
  const cgpaEl = document.getElementById('edu-cgpa');
  const gradEl = document.getElementById('edu-graduation');

  if (degreeEl) degreeEl.textContent = edu.degree || '';
  if (instEl) instEl.textContent = edu.institution || '';
  if (cgpaEl) cgpaEl.textContent = edu.cgpa || '';
  if (gradEl) gradEl.textContent = edu.expected_graduation || '';
}


// ── Visitor Count ─────────────────────────────────────────────────
async function loadVisitorCount() {
  const data = await apiFetch('/visitor-count');
  if (data) {
    const el = document.getElementById('visitor-count');
    if (el) el.textContent = data.count.toLocaleString();
  }

  // Record this visit
  await fetch('/api/record-visit', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ page: window.location.pathname }),
  }).catch(() => {});
}


// ── Contact Form ──────────────────────────────────────────────────
function initContactForm() {
  const form = document.getElementById('contact-form');
  if (!form) return;

  form.addEventListener('submit', async e => {
    e.preventDefault();
    const btn = form.querySelector('[type="submit"]');
    const successEl = document.getElementById('form-success');
    const errorEl = document.getElementById('form-error');

    successEl.style.display = 'none';
    errorEl.style.display = 'none';

    const name = form.querySelector('[name="name"]').value.trim();
    const email = form.querySelector('[name="email"]').value.trim();
    const message = form.querySelector('[name="message"]').value.trim();

    if (!name || !email || !message) {
      errorEl.textContent = 'Please fill in all fields.';
      errorEl.style.display = 'block';
      return;
    }

    btn.disabled = true;
    btn.innerHTML = '<span class="spinner"></span> Sending...';

    try {
      const res = await fetch('/api/contact', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, email, message }),
      });

      const data = await res.json();

      if (data.success) {
        successEl.textContent = data.message;
        successEl.style.display = 'block';
        form.reset();
      } else {
        errorEl.textContent = (data.errors || ['Error sending message.']).join(' ');
        errorEl.style.display = 'block';
      }
    } catch {
      errorEl.textContent = 'Network error. Please try again.';
      errorEl.style.display = 'block';
    } finally {
      btn.disabled = false;
      btn.innerHTML = 'Send Message ↗';
    }
  });
}


// ── Loading Screen ────────────────────────────────────────────────
function hideLoadingScreen() {
  const screen = document.getElementById('loading-screen');
  if (screen) {
    setTimeout(() => screen.classList.add('hidden'), 1500);
  }
}


// ── Init ──────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  // Loading
  hideLoadingScreen();

  // Background
  if (!window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    new SpiderWebCanvas('spider-canvas');
  }

  // Core UI
  initScrollProgress();
  initScrollReveal();
  initNav();
  initTheme();
  initCounters();
  initSkillBars();
  initContactForm();
  initProjectSearch();

  // API Data
  loadProfile();
  loadHeroStats();
  loadEducation();
  loadProjects();
  loadSkills();
  loadCertifications();
  loadAchievements();
  loadVisitorCount();
});
