/* Progressive enhancement: the journey remains readable without JavaScript. */
(() => {
  const flow = document.querySelector('.journey-flow');
  if (!flow) return;
  const buttons = [...flow.querySelectorAll('.journey-stage')];
  const panels = buttons.map(button => document.getElementById(button.getAttribute('aria-controls')));
  function select(index, focus = false) {
    buttons.forEach((button, i) => {
      button.setAttribute('aria-selected', String(i === index));
      button.tabIndex = i === index ? 0 : -1;
      panels[i].hidden = i !== index;
    });
    if (focus) buttons[index].focus();
  }
  flow.setAttribute('role', 'tablist');
  flow.querySelectorAll('li').forEach(item => item.setAttribute('role', 'presentation'));
  buttons.forEach((button, index) => {
    button.setAttribute('role', 'tab');
    panels[index].setAttribute('role', 'tabpanel');
    panels[index].tabIndex = 0;
    button.addEventListener('click', () => select(index));
    button.addEventListener('keydown', event => {
      let next;
      if (['ArrowRight', 'ArrowDown'].includes(event.key)) next = (index + 1) % buttons.length;
      if (['ArrowLeft', 'ArrowUp'].includes(event.key)) next = (index + buttons.length - 1) % buttons.length;
      if (event.key === 'Home') next = 0;
      if (event.key === 'End') next = buttons.length - 1;
      if (next !== undefined) { event.preventDefault(); select(next, true); }
    });
  });
  select(1);
})();
