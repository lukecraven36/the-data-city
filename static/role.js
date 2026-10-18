// A browser-local tour. No requests, storage or invented performance results.
(() => {
  const tabs = [...document.querySelectorAll('.role-stage-tabs [role="tab"]')];
  if (!tabs.length) return;
  const panels = tabs.map(tab => document.getElementById(tab.getAttribute('aria-controls')));
  function select(index, focus = false) {
    tabs.forEach((tab, i) => {
      tab.setAttribute('aria-selected', String(i === index));
      tab.tabIndex = i === index ? 0 : -1;
      panels[i].hidden = i !== index;
    });
    if (focus) tabs[index].focus();
  }
  tabs.forEach((tab, index) => {
    tab.addEventListener('click', () => select(index));
    tab.addEventListener('keydown', event => {
      let target;
      if (event.key === 'ArrowRight') target = (index + 1) % tabs.length;
      if (event.key === 'ArrowLeft') target = (index + tabs.length - 1) % tabs.length;
      if (event.key === 'Home') target = 0;
      if (event.key === 'End') target = tabs.length - 1;
      if (target !== undefined) { event.preventDefault(); select(target, true); }
    });
  });
  select(0);
})();
