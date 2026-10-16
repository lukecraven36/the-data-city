// Native details remain usable without JavaScript. Bulk controls are optional.
const controls = document.querySelector('.cv-controls');
if (controls) {
  const sections = [...document.querySelectorAll('.cv-detail')];
  const status = document.querySelector('.cv-action-status');
  controls.hidden = false;
  document.querySelector('#cv-expand').addEventListener('click', () => {
    sections.forEach(section => { section.open = true; });
    status.textContent = 'All CV sections expanded.';
  });
  document.querySelector('#cv-collapse').addEventListener('click', () => {
    sections.forEach(section => { section.open = false; });
    status.textContent = 'All CV sections collapsed.';
  });
}
