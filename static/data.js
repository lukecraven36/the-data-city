// Compare only the fields already rendered from the saved response. No network calls.
const cards = [...document.querySelectorAll('.company')];
const choices = cards.map(card => card.querySelector('input'));
const status = document.querySelector('#selection-status');
const comparison = document.querySelector('#comparison');
const content = document.querySelector('#comparison-content');

function cell(tag, text) {
  const element = document.createElement(tag);
  element.textContent = text;
  return element;
}

function update() {
  const selected = cards.filter((card, i) => choices[i].checked);
  choices.forEach(choice => { choice.disabled = selected.length === 2 && !choice.checked; });
  status.textContent = selected.length === 2
    ? 'Two companies selected. Their returned details appear below.'
    : `${selected.length} of 2 selected. Select two companies to compare the returned fields.`;
  comparison.hidden = selected.length !== 2;
  content.replaceChildren();
  if (selected.length !== 2) return;
  const wrap = document.createElement('div');
  wrap.className = 'table-wrap';
  const table = document.createElement('table');
  const caption = cell('caption', 'Comparison of two companies from the saved API response');
  caption.className = 'sr-only';
  table.append(caption);
  const head = document.createElement('thead');
  const heading = document.createElement('tr');
  for (const title of ['Returned field', ...selected.map(card => card.dataset.name)]) {
    const th = cell('th', title); th.scope = 'col'; heading.append(th);
  }
  head.append(heading); table.append(head);
  const body = document.createElement('tbody');
  for (const [label, key] of [['Company number', 'number'], ['Website', 'website'], ['Similarity score', 'similarity']]) {
    const row = document.createElement('tr');
    const title = cell('th', label); title.scope = 'row'; row.append(title);
    for (const card of selected) {
      const value = card.dataset[key];
      const td = cell('td', value || 'Not returned');
      if (key === 'website' && value) {
        const link = cell('a', value.replace(/^https?:\/\//, '') + ' ↗');
        link.href = value; link.target = '_blank'; link.rel = 'noopener noreferrer';
        td.replaceChildren(link);
      }
      row.append(td);
    }
    body.append(row);
  }
  table.append(body); wrap.append(table); content.append(wrap);
}
if (status) {
  document.querySelector('.compare-toolbar').hidden = false;
  document.querySelectorAll('.compare-choice').forEach(label => { label.hidden = false; });
  choices.forEach(choice => choice.addEventListener('change', update));
  document.querySelector('#clear-comparison').addEventListener('click', () => {
    choices.forEach(choice => { choice.checked = false; }); update();
  });
}
