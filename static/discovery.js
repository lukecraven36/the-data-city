(() => {
  'use strict';
  const app = document.querySelector('#discovery-app');
  if (!app) return;
  const data = JSON.parse(document.querySelector('#discovery-payload').content.textContent);
  const $ = (s) => app.querySelector(s);
  const $$ = (s) => [...app.querySelectorAll(s)];
  const esc = (v) => String(v ?? '').replace(/[&<>"']/g, (c) => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const money = (v) => new Intl.NumberFormat('en-GB', {style:'currency', currency:'GBP', maximumFractionDigits:0}).format(v);
  const compact = (v) => v >= 1e6 ? '£' + (v / 1e6).toFixed(2) + 'm' : v >= 1000 ? '£' + new Intl.NumberFormat('en-GB', {maximumFractionDigits:0}).format(v / 1000) + 'k' : money(v);
  const date = (v) => new Date(v + 'T12:00:00').toLocaleDateString('en-GB', {day:'numeric', month:'short', year:'numeric'});
  const shortName = (n) => n.replace(/ LIMITED$| LTD$/,'').toLowerCase().replace(/\b[a-z]/g, (c) => c.toUpperCase());
  const safeURL = (v) => { try { const u = new URL(v.startsWith('http') ? v : 'https://' + v); return ['https:', 'http:'].includes(u.protocol) ? u.href : '#'; } catch { return '#'; } };
  const state = {contact:{}, answers:{}, compared:new Set(), timers:[], activeTab:'overview', lastProfileTrigger:null};
  const defaultAnswers = Object.fromEntries(new FormData($('#discovery-form')));
  const screens = ['contact-screen','discovery-screen','processing-screen','report-screen'];
  const announce = (text) => { $('#journey-announcement').textContent = text; };
  function show(screen, step, focus = true) {
    screens.forEach((id) => { $('#' + id).hidden = id !== screen; });
    $$('.journey-steps li').forEach((li, i) => {
      li.classList.toggle('is-current', i === step);
      li.classList.toggle('is-complete', i < step);
      li.querySelector('.step-index').textContent = i < step ? '✓' : '0' + (i + 1);
      if (i === step) li.setAttribute('aria-current', 'step'); else li.removeAttribute('aria-current');
    });
    if (focus) {
      const heading = $('#' + screen).querySelector('h1');
      heading.tabIndex = -1; heading.focus({preventScroll:true});
      window.scrollTo({top:0, behavior:'instant'});
    }
  }
  function valid(form, target) {
    const invalid = [...form.elements].find((el) => el.willValidate && (!el.checkValidity() || (el.required && !el.value.trim())));
    $(target).hidden = !invalid;
    if (invalid) {
      $(target).textContent = 'Please check the highlighted field before continuing.';
      invalid.setAttribute('aria-invalid','true'); invalid.focus(); invalid.reportValidity(); return false;
    }
    return true;
  }
  $$('input,textarea,select').forEach((el) => el.addEventListener('input', () => el.removeAttribute('aria-invalid')));
  $('#contact-form').addEventListener('submit', (event) => {
    event.preventDefault();
    if (!valid(event.currentTarget, '#contact-error')) return;
    state.contact = Object.fromEntries([...new FormData(event.currentTarget)].map(([k,v]) => [k,v.trim()]));
    $('#persona-name').textContent = state.contact.firstName + ' ' + state.contact.surname;
    $('#persona-org').textContent = state.contact.organisation + ' · ' + state.contact.industry;
    show('discovery-screen', 1); announce('Step two. Tell us about your challenge.');
  });
  function cancelTimers() { state.timers.forEach(clearTimeout); state.timers = []; }
  function startPreview() {
    show('processing-screen', 2);
    const stages = $$('#research-stages li');
    stages.forEach((s) => { s.className = ''; s.removeAttribute('aria-current'); });
    [0, 550, 1100, 1650].forEach((delay, i) => {
      state.timers.push(setTimeout(() => {
        stages.forEach((s,j) => { s.classList.toggle('stage-complete', j < i); s.classList.toggle('stage-current', j === i); });
        announce(stages[i].textContent);
      }, delay));
    });
    state.timers.push(setTimeout(() => {
      renderReport(); show('report-screen', 2); selectTab('overview'); announce('Your prepared insights preview is ready. Ten companies.');
      cancelTimers();
    }, 2300));
  }
  $('#discovery-form').addEventListener('submit', (event) => {
    event.preventDefault();
    if (!valid(event.currentTarget, '#discovery-error')) return;
    state.answers = Object.fromEntries([...new FormData(event.currentTarget)].map(([k,v]) => [k,v.trim()]));
    startPreview();
  });
  $('#cancel-preview').addEventListener('click', () => { cancelTimers(); show('discovery-screen',1); announce('Preview stopped. Your answers are preserved.'); });
  ['#edit-contact','#back-to-details'].forEach((id) => $(id).addEventListener('click', () => show('contact-screen',0)));
  $('#edit-brief').addEventListener('click', () => show('discovery-screen',1));
  $('#restore-example').addEventListener('click', () => {
    Object.entries(defaultAnswers).forEach(([k,v]) => { $('#discovery-form').elements[k].value=v; });
    announce('Local government example restored.');
  });
  $('#print-report').addEventListener('click', () => window.print());
  $('#restart-demo').addEventListener('click', () => {
    cancelTimers(); $('#contact-form').reset(); $('#discovery-form').reset();
    state.contact = {}; state.answers = {}; state.compared.clear(); $('#company-search').value = '';
    $$('.form-error').forEach((e) => {e.hidden=true;});
    show('contact-screen',0); announce('Experience restarted.');
  });
  function selectTab(tab, focus = false) {
    state.activeTab = tab;
    $$('[data-tab]').forEach((button) => {
      const active = button.dataset.tab === tab;
      button.setAttribute('aria-selected',String(active)); button.tabIndex = active ? 0 : -1;
      $('#panel-' + button.dataset.tab).hidden = !active;
      if (active && focus) button.focus();
    });
  }
  $$('[data-tab]').forEach((button, i, tabs) => {
    button.addEventListener('click', () => selectTab(button.dataset.tab));
    button.addEventListener('keydown', (e) => {
      let next = null;
      if (e.key === 'ArrowRight') next = (i+1)%tabs.length;
      if (e.key === 'ArrowLeft') next = (i+tabs.length-1)%tabs.length;
      if (e.key === 'Home') next = 0;
      if (e.key === 'End') next = tabs.length-1;
      if (next !== null) {e.preventDefault(); selectTab(tabs[next].dataset.tab,true);}
    });
  });
  function bars(companies, key, variant) {
    const max = Math.max(...companies.map((c) => c[key]),1);
    return companies.map((c,i) => `<button type="button" class="bar-row ${variant}" data-company="${esc(c.id)}" aria-label="Open ${esc(shortName(c.name))}, ${esc(key)}, ${esc(money(c[key]))}"><span>${esc(shortName(c.name))}</span><strong>${esc(compact(c[key]))}</strong><svg viewBox="0 0 500 10" preserveAspectRatio="none" aria-hidden="true"><rect class="bar-background" x="0" y="0" width="500" height="10" rx="5"/><rect class="bar-fill tone-${i%3}" x="0" y="0" width="${Math.max(3,c[key]/max*500).toFixed(2)}" height="10" rx="5"/></svg></button>`).join('');
  }
  function renderReport() {
    $('#understood-question').textContent = state.answers.goal;
    const total = (key) => data.companies.reduce((a,c) => a+c[key],0);
    const regions = new Set(data.companies.map((c) => c.region));
    $('#headline-kpis').innerHTML = [
      ['◈','Companies discovered','10','The complete returned sample','lime'],
      ['↗','Combined turnover',compact(total('turnover')),'Across the company preview','white'],
      ['✦','Funding landscape',compact(total('funding')),'Capital across the preview','white'],
      ['◎','Regions & nations',String(regions.size),'A UK-wide starting point','peach']
    ].map(([icon,label,value,note,tone])=>`<article class="kpi-card kpi-${tone}"><div><span>${esc(label)}</span><span class="kpi-icon" aria-hidden="true">${icon}</span></div><strong>${esc(value)}</strong><small>${esc(note)}</small></article>`).join('');
    $('#turnover-chart').innerHTML = bars([...data.companies].sort((a,b)=>b.turnover-a.turnover),'turnover','turnover-bars');
    $('#funding-chart').innerHTML = bars(data.companies.filter((c)=>c.funding>0).sort((a,b)=>b.funding-a.funding),'funding','funding-bars');
    const memberships = new Map();
    data.companies.forEach((c)=>c.sic.forEach((s)=>memberships.set(s.code,{name:s.description,count:(memberships.get(s.code)?.count||0)+1})));
    const top = [...memberships].sort((a,b)=>b[1].count-a[1].count).slice(0,4);
    $('#activity-chart').innerHTML = top.map(([code,v],i)=>`<div class="activity-row"><div><strong>${v.count}</strong><span>${esc(v.name)}<small>SIC ${esc(code)}</small></span></div><svg viewBox="0 0 500 9" preserveAspectRatio="none" aria-hidden="true"><rect class="bar-background" width="500" height="9" rx="4"/><rect class="bar-fill tone-${i%3}" width="${v.count/10*500}" height="9" rx="4"/></svg></div>`).join('');
    renderMap(); renderCompanies(); renderComparison(); renderHandoff();
    $('#classification-evidence').innerHTML = Object.entries(data.classifications).map(([type,items])=>`<h3>${esc(type)}</h3><ul>${items.map((item)=>`<li>${esc(item.Description)} <span class="code">${esc(item.Code)}</span></li>`).join('')}</ul>`).join('')+'<p class="chart-caption">Classifications belong to the submitted description. They have not been assigned to each returned company.</p>';
  }
  function renderMap() {
    const project = (lon,lat) => [(lon+11)*32,(60.5-lat)*49];
    const paths = data.map.features.map((f) => {
      const polygons = f.geometry.type==='MultiPolygon' ? f.geometry.coordinates : [f.geometry.coordinates];
      return polygons.map((polygon)=>`<path class="map-land ${f.name==='Ireland'?'map-neighbour':''}" d="${polygon.map((ring)=>ring.map(([lon,lat],i)=>{const [x,y]=project(lon,lat);return `${i?'L':'M'}${x.toFixed(2)},${y.toFixed(2)}`;}).join(' ')+'Z').join(' ')}"/>`).join('');
    }).join('');
    const points = data.companies.map((c)=>{const [x,y]=project(c.lon,c.lat);return `<g class="map-point" data-company="${esc(c.id)}" role="button" tabindex="0" aria-label="${esc(shortName(c.name))}, registered office ${esc(c.locality)}"><title>${esc(shortName(c.name))} · ${esc(c.locality)}</title><circle class="map-halo" cx="${x}" cy="${y}" r="10"/><circle cx="${x}" cy="${y}" r="4"/></g>`;}).join('');
    const counts = new Map(); data.companies.forEach(c=>counts.set(c.region,(counts.get(c.region)||0)+1));
    $('#company-map').innerHTML = `<div class="map-layout"><svg class="uk-map" viewBox="0 0 450 530" aria-label="UK registered-office locations" role="img">${paths}${points}</svg><div class="map-regions">${[...counts].sort((a,b)=>b[1]-a[1]).map(([name,count])=>`<div><span>${esc(name)}</span><strong>${count}</strong></div>`).join('')}<p>All ten businesses.<br>No geography filter.</p></div></div>`;
  }
  function renderCompanies() {
    const query=$('#company-search').value.trim().toLowerCase();
    const companies=data.companies.filter(c=>[c.name,c.locality,...c.capabilities].join(' ').toLowerCase().includes(query));
    $('#company-table').innerHTML=companies.length ? companies.map((c)=>`<tr><td><div class="table-company"><label class="compare-check"><span class="sr-only">Compare ${esc(shortName(c.name))}</span><input type="checkbox" data-compare="${esc(c.id)}" ${state.compared.has(c.id)?'checked':''} ${state.compared.size>=3&&!state.compared.has(c.id)?'disabled':''}></label><div><button type="button" data-company="${esc(c.id)}">${esc(shortName(c.name))}</button><small>${esc(c.id)} · ${esc(c.capabilities[0])}</small></div></div></td><td>${esc(c.locality)}</td><td class="numeric">${esc(compact(c.turnover))}</td><td class="numeric">${esc(compact(c.funding))}</td><td class="numeric">${c.employees===null?'—':c.employees}</td><td><button class="open-profile" type="button" data-company="${esc(c.id)}" aria-label="View ${esc(shortName(c.name))}">↗</button></td></tr>`).join('') : '<tr><td colspan="6" class="empty-results">No companies match that search. Clear it to see all ten.</td></tr>';
    $('#company-count').textContent=`Showing ${companies.length} of ${data.companies.length} companies · employee counts are reported period averages.`;
  }
  $('#company-search').addEventListener('input',renderCompanies);
  app.addEventListener('change',(event)=>{
    const id=event.target.dataset.compare; if(!id)return;
    if(event.target.checked&&state.compared.size<3)state.compared.add(id);else state.compared.delete(id);
    renderCompanies();renderComparison();announce(`${state.compared.size} companies selected for comparison.`);
  });
  $('#clear-comparison').addEventListener('click',()=>{state.compared.clear();renderCompanies();renderComparison();});
  function renderComparison() {
    const companies=data.companies.filter(c=>state.compared.has(c.id));
    const panel=$('#company-comparison');panel.hidden=companies.length<2;
    if(panel.hidden)return;
    const rows=[['Registered location',c=>c.locality],['Turnover',c=>compact(c.turnover)],['Funding',c=>compact(c.funding)],['Average employees',c=>c.employees===null?'Not disclosed':String(c.employees)],['Net assets',c=>money(c.netAssets)],['Accounts end',c=>date(c.accountsEnd)],['Capabilities',c=>c.capabilities.join(', ')]];
    panel.innerHTML=`<h3>Your company comparison</h3><div class="table-wrap"><table><thead><tr><th>Measure</th>${companies.map(c=>`<th>${esc(shortName(c.name))}</th>`).join('')}</tr></thead><tbody>${rows.map(([label,fn])=>`<tr><th>${esc(label)}</th>${companies.map(c=>`<td>${esc(fn(c))}</td>`).join('')}</tr>`).join('')}</tbody></table></div>`;
  }
  function openProfile(id,trigger) {
    const c=data.companies.find(c=>c.id===id); if(!c)return;
    state.lastProfileTrigger=trigger;
    $('#company-profile').innerHTML=`<h2 id="company-dialog-title">${esc(shortName(c.name))}</h2><div class="profile-meta">${esc(c.id)} <span>·</span> ${esc(c.status)} <span>·</span> ${esc(c.locality)}</div><p class="profile-summary">${esc(c.summary)}</p><div class="capability-tags">${c.capabilities.map(s=>`<span>${esc(s)}</span>`).join('')}</div><div class="profile-metrics"><div><span>Turnover</span><strong>${esc(compact(c.turnover))}</strong></div><div><span>Funding</span><strong>${esc(compact(c.funding))}</strong></div><div><span>Avg. employees</span><strong>${c.employees===null?'—':c.employees}</strong></div></div><dl class="profile-facts"><div><dt>Incorporated</dt><dd>${esc(date(c.incorporated))}</dd></div><div><dt>Latest filed accounts</dt><dd>${esc(date(c.accountsEnd))}</dd></div><div><dt>Net assets, as filed</dt><dd>${esc(money(c.netAssets))}</dd></div></dl><h3>Reported business activities</h3><ul class="profile-sic">${c.sic.map(s=>`<li><span>${esc(s.code)}</span>${esc(s.description)}</li>`).join('')}</ul>${c.products.length?`<h3>Products &amp; projects</h3><p>${esc(c.products.join(' · '))}</p>`:''}<h3>Explore the sources</h3><div class="profile-sources">${c.sources.map(s=>`<a href="${esc(safeURL(s.url))}" target="_blank" rel="noopener noreferrer">${esc(s.kind==='statutory_register'?'Companies House':s.kind==='filed_accounts'?'Filed accounts':c.website)} ↗</a>`).join('')}</div><p class="profile-note">Employee figures relate to the filed accounting period. Registered-office locations may differ from operating locations.</p>`;
    $('#company-dialog').showModal();
  }
  app.addEventListener('click',(event)=>{const trigger=event.target.closest('[data-company]');if(trigger)openProfile(trigger.dataset.company,trigger);});
  app.addEventListener('keydown',(event)=>{const trigger=event.target.closest('.map-point');if(trigger&&['Enter',' '].includes(event.key)){event.preventDefault();openProfile(trigger.dataset.company,trigger);}});
  $('#close-company').addEventListener('click',()=>$('#company-dialog').close());
  $('#company-dialog').addEventListener('close',()=>{if(state.lastProfileTrigger?.isConnected)state.lastProfileTrigger.focus({preventScroll:true});});
  $('#company-dialog').addEventListener('click',(event)=>{if(event.target===$('#company-dialog')){const r=event.target.getBoundingClientRect();if(event.clientX<r.left||event.clientX>r.right||event.clientY<r.top||event.clientY>r.bottom)event.target.close();}});
  function briefEntries() {
    return [['Prepared for',`${state.contact.firstName} ${state.contact.surname} · ${state.contact.organisation}`],['Industry',state.contact.industry],['The decision',state.answers.goal],['Existing information',state.answers.existing],['Desired output',state.answers.output],['Suggested next conversation','Explore relevant sectors, operating geographies, growth definitions and the evidence needed for a tailored product demonstration.']];
  }
  function renderHandoff() {$('#handoff-brief').innerHTML=briefEntries().map(([label,value])=>`<div><dt>${esc(label)}</dt><dd>${esc(value)}</dd></div>`).join('');}
  $('#download-brief').addEventListener('click',()=>{
    const text='DISCOVER YOUR MARKET — PREPARED DISCOVERY BRIEF\n\n'+briefEntries().map(([k,v])=>k+'\n'+v).join('\n\n')+'\n\nPrepared concept demonstration. Company turnover and funding visuals include illustrative values. No enquiry has been submitted.\n';
    const url=URL.createObjectURL(new Blob([text],{type:'text/plain;charset=utf-8'}));
    const a=document.createElement('a');a.href=url;a.download='your-discovery-brief.txt';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);
  });
  show('contact-screen',0,false);
})();
