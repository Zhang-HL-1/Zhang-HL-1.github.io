'use strict';
const themeButton = document.querySelector('#theme');
if (themeButton) themeButton.addEventListener('click', () => {
  const theme = document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark';
  document.documentElement.dataset.theme = theme;
  try { localStorage.setItem('theme', theme); } catch (_) {}
});
const year = document.querySelector('#year');
if (year) year.textContent = new Date().getFullYear();
const postsElement = document.querySelector('#posts');
if (postsElement) initJournal();
function node(tag, text, className) {
  const el = document.createElement(tag);
  if (text !== undefined) el.textContent = text;
  if (className) el.className = className;
  return el;
}
async function initJournal() {
  try {
    const response = await fetch('/posts.json');
    if (!response.ok) throw new Error('Unable to load posts');
    const posts = await response.json();
    let category = '全部';
    const search = document.querySelector('#search');
    const filters = document.querySelector('#filters');
    document.querySelector('#post-count').textContent = ' / ' + String(posts.length).padStart(2, '0');
    ['技术笔记', '留学记录', '日常随笔', ...posts.map(p => p.category)].filter((v, i, a) => a.indexOf(v) === i).forEach(name => {
      const button = node('button', name);
      button.type = 'button'; button.dataset.category = name; button.setAttribute('aria-pressed', 'false'); filters.append(button);
    });
    function render() {
      const q = search.value.trim().toLocaleLowerCase();
      const selected = posts.filter(p => (category === '全部' || p.category === category) && [p.title, p.description, p.category, p.text].join(' ').toLocaleLowerCase().includes(q));
      postsElement.replaceChildren();
      if (!selected.length) {
        const empty = node('div', undefined, 'empty');
        empty.append(node('span', '✳', 'empty-symbol'), node('h3', posts.length ? '还没有找到这篇记录' : '新的一页，留给下一次灵感'), node('p', posts.length ? '换个关键词，或选择其他分类试试。' : '博客已经重新启程，第一篇正式记录正在路上。'));
        postsElement.append(empty);
      }
      selected.forEach(p => {
        const link = node('a', undefined, 'post'); link.href = p.url;
        const time = node('time', p.date); time.dateTime = p.date;
        const body = node('div'); body.append(node('small', p.category), node('h3', p.title), node('p', p.description));
        link.append(time, body, node('span', '↗')); postsElement.append(link);
      });
    }
    filters.addEventListener('click', e => {
      const button = e.target.closest('button'); if (!button) return;
      category = button.dataset.category;
      filters.querySelectorAll('button').forEach(b => { b.classList.toggle('selected', b === button); b.setAttribute('aria-pressed', String(b === button)); }); render();
    });
    search.addEventListener('input', render);
    const archive = document.querySelector('#archive-list');
    if (!posts.length) archive.append(node('p', '还没有文章。每一篇新的记录，都会收进这里。', 'muted'));
    const years = [...new Set(posts.map(p => p.date.slice(0, 4)))];
    years.forEach(y => {
      archive.append(node('h3', y)); const list = node('ul');
      posts.filter(p => p.date.startsWith(y)).forEach(p => { const li = node('li'); const a = node('a', p.title); a.href = p.url; const t = node('time', p.date.slice(5)); t.dateTime = p.date; li.append(t, a); list.append(li); }); archive.append(list);
    });
    function route() { document.querySelector('#archive').hidden = location.hash !== '#archive'; }
    window.addEventListener('hashchange', route); route(); render();
  } catch (error) {
    postsElement.replaceChildren(node('p', '文章暂时未能加载，请刷新页面重试。', 'empty'));
  }
}

const progress = document.querySelector('.reading-progress');
if (progress) {
  let scheduled = false;
  function updateProgress() {
    const distance = document.documentElement.scrollHeight - innerHeight;
    progress.style.transform = 'scaleX(' + (distance > 0 ? Math.min(1, Math.max(0, scrollY / distance)) : 0) + ')';
    scheduled = false;
  }
  addEventListener('scroll', () => { if (!scheduled) { scheduled = true; requestAnimationFrame(updateProgress); } }, { passive: true });
  addEventListener('resize', updateProgress);
  updateProgress();
}
