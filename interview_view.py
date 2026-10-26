"""Dated public research and proposed contribution for Luke's interview briefing."""
from html import escape

SOURCES = {
    'about': ('https://thedatacity.com/about-us/', 'Company overview'),
    'history': ('https://thedatacity.com/blog/the-data-city-in-2025-scaling-new-heights/', 'Origins and 2025 milestones'),
    'team': ('https://thedatacity.com/about-us/meet-the-team/', 'Official leadership list'),
    'mitali': ('https://thedatacity.com/about-us/meet-the-team/mitali-mookerjee/', 'Mitali’s profile'),
    'data': ('https://thedatacity.com/data/', 'Data sources and coverage'),
    'method': ('https://thedatacity.com/blog/behind-the-scenes-of-rtic-creation/', 'How RTICs are built'),
    'updates': ('https://thedatacity.com/blog/real-time-all-the-time-the-process-behind-rtic-updates/', 'How RTICs are maintained'),
    'rsic': ('https://thedatacity.com/product-service/real-time-sic-codes-rsics/', 'RSIC and RTIC explained'),
    'global': ('https://thedatacity.com/blog/the-future-of-business-intelligence/', '14 September 2026 business update'),
    'release': ('https://thedatacity.com/blog/industry-engine-release-notes/', 'September 2026 release notes'),
    'regional': ('https://thedatacity.com/blog/finding-your-areas-industrial-strategy-strengths-a-northern-ireland-case-study/', '29 September 2026 regional insight'),
    'refresh': ('https://thedatacity.com/blog/real-time-sic-codes-have-had-a-refresh/', '11 August 2026 RSIC update'),
}
LEADERS = [
    ('AC', 'Alex Craven', 'Chief Executive Officer'),
    ('PC', 'Paul Connell', 'Executive Chair'),
    ('TF', 'Tom Forth', 'Chief Technology Officer'),
    ('KW', 'Kelly Weston', 'Chief Operating Officer'),
    ('ED', 'Emma Dickinson', 'Chief Financial Officer'),
    ('MM', 'Mitali Mookerjee', 'Managing Director (UK)'),
]


def source(*keys):
    links = ' · '.join(f'<a href="{escape(SOURCES[k][0], quote=True)}" target="_blank" rel="noopener noreferrer">{escape(SOURCES[k][1])} ↗</a>' for k in keys)
    return f'<p class="brief-sources">{links}</p>'


def render():
    leaders = ''.join(f'<li class="leader-card{" leader-focus" if initials == "MM" else ""}"><span class="leader-initials" aria-hidden="true">{initials}</span><div><h3>{name}</h3><p>{title}</p></div></li>' for initials, name, title in LEADERS)
    return f'''<article class="interview-story interview-briefing">
    <section id="company" class="brief-section company-section" aria-labelledby="company-title">
      <div class="brief-heading"><p class="brief-eyebrow">LUKE’S INTERVIEW NOTES <span>CHECKED 26 OCTOBER 2026</span></p><h1 id="company-title">The Data City <em>at a glance.</em></h1><p class="brief-summary">A Leeds-born data and software business helping people understand <strong>what companies actually do</strong> — and how industries are changing.</p></div>
      <nav class="brief-index" aria-label="Interview sections"><a href="#company">01 / The business</a><a href="#developments">02 / News &amp; growth</a><a href="#my-role">03 / My contribution</a></nav>
      <div class="business-grid"><div class="business-main"><span class="brief-label">WHAT THEY SELL</span><h2>Company activity →<br>economic intelligence.</h2><p>Industry Engine lets customers find companies, build sector lists, analyse growth and map clusters. Data also reaches customers through APIs, licensing and bespoke data services.</p></div><div class="business-audience"><span class="brief-label">WHO USES IT / WHY</span><ul><li><strong>Government &amp; councils</strong>Understand sectors, places and investment priorities.</li><li><strong>Investors &amp; businesses</strong>Find opportunities, research companies and markets.</li><li><strong>Researchers &amp; consultants</strong>Measure economic activity and emerging industries.</li></ul></div></div>
      {source('about', 'data')}
      <div class="brief-subhead"><h2>The company’s journey</h2><span>From a UK classification problem to global infrastructure</span></div>
      <ol class="company-timeline"><li><strong>2017</strong><h3>The starting point</h3><p>Founded as a spin-out from Open Innovations, combining open data, the web and machine learning.</p></li><li><strong>2025</strong><h3>A platform for scale</h3><p>Industry Engine V5 and an Oxford Economics investment partnership support international expansion.</p></li><li><strong>2026</strong><h3>Going global</h3><p>A US joint venture and multi-country data products extend the UK foundation.</p></li></ol>
      {source('history', 'global')}
      <div class="brief-subhead"><h2>Who’s leading the business?</h2><span>Senior leadership, including Mitali · not a reporting-line chart</span></div>
      <ul class="leadership-grid">{leaders}</ul>
      <p class="brief-callout"><strong>Remember Mitali’s current title:</strong> Managing Director (UK). Her official profile emphasises business-information experience, commercial growth and international partnerships.</p>
      {source('team', 'mitali')}
      <div class="brief-subhead"><h2>How the data becomes useful</h2><span>The UK workflow, simplified</span></div>
      <ol class="data-pipeline"><li><span>01</span><h3>Company records</h3><p>Companies House anchors identities, filings and registered SIC codes.</p></li><li><span>02</span><h3>Web evidence</h3><p>Match companies to websites; analyse how they describe their activities.</p></li><li><span>03</span><h3>Classification</h3><p>Machine learning and sector experts identify relevant activities and industry verticals.</p></li><li><span>04</span><h3>Enrichment &amp; insight</h3><p>Add financial, location, jobs and growth information; explore sectors and places.</p></li></ol>
      <div class="code-comparison"><div><span class="code-tag">SIC</span><h3>The registered category</h3><p><strong>Standard Industrial Classification.</strong> Company-selected categories can be broad, inaccurate or slow to reflect new activities.</p></div><div><span class="code-tag">RSIC</span><h3>A better SIC assignment</h3><p><strong>Real-Time SIC.</strong> AI assigns more relevant codes within the existing SIC framework, filling gaps or correcting weak matches.</p></div><div><span class="code-tag">RTIC</span><h3>A new sector lens</h3><p><strong>Real-Time Industrial Classification.</strong> Expert-defined sectors and verticals use website evidence to find activities such as AI, quantum and CleanTech beyond SIC boundaries.</p></div></div>
      <div class="method-notes"><p><strong>Human expertise stays in the loop.</strong> Define a taxonomy → train on relevant and irrelevant examples → review results → publish. Monthly maintenance, annual reviews and fixes keep classifications evolving; “real-time” does not mean every field refreshes instantly.</p><p><strong>More than Companies House.</strong> Published sources include Creditsafe for company/financial data, Lightcast for jobs and skills, and Innovate UK / 360Giving for funding. Coverage varies; some turnover, employee and growth measures are estimates.</p></div>
      {source('data', 'method', 'updates', 'rsic')}
      <div class="brief-takeaway"><small>THE POINT TO REMEMBER</small><p>The value is the combination: <strong>company identity + evidence of activity + context</strong> — making emerging sectors visible and decisions better informed.</p></div>
    </section>
    <section id="developments" class="brief-section" aria-labelledby="developments-title"><div class="section-number">02 / NEWS &amp; GROWTH</div><h2 id="developments-title">What’s moving now?</h2><p class="section-intro">Selected public updates available on 26 October 2026. Reported performance and plans are dated, not live figures.</p>
      <div class="growth-direction"><div><span class="brief-label">EXPANSION DIRECTION</span><h3>UK foundation → US priority → wider markets</h3><p>The September update describes a US joint venture using Oxford Economics’ infrastructure and customer network. European customers are supported from Leeds and London.</p><ul class="country-tags" aria-label="Countries named in the September product announcement"><li>UK</li><li>Ireland</li><li>France</li><li>Germany</li><li>USA</li></ul><p class="brief-note">These are announced product markets; availability and commercial rollout differ. Confirm the current position in the interview.</p></div><div class="growth-signal"><span class="brief-label">COMPANY-REPORTED / 14 SEP 2026</span><strong>&gt;$2m <small>ARR</small></strong><strong>+25% <small>UK public-sector growth</small></strong><p>ARR is annual recurring revenue.</p></div></div>
      <div class="news-grid"><div class="news-card"><time datetime="2026-09-29">29 SEP 2026 / CUSTOMER USE CASE</time><h3>Industrial Strategy in practice</h3><p>Northern Ireland analysis connects IS-8 sector strengths, clusters and skills. A useful example for a local-government conversation.</p>{source('regional')}</div><div class="news-card"><time datetime="2026-09">SEP 2026 / PRODUCT</time><h3>Industry Engine v6.5</h3><p>A redesigned Explore experience, customisable lists, clearer filters and AI-powered help put usability and discovery in focus.</p>{source('release')}</div><div class="news-card"><time datetime="2026-09-14">14 SEP 2026 / COMMERCIAL</time><h3>More markets, more use cases</h3><p>The company reports new markets in defence, real estate, higher education and financial services; investment partners are being sought for 2027/28 expansion.</p>{source('global')}</div><div class="news-card"><time datetime="2026-08-11">11 AUG 2026 / CLASSIFICATION</time><h3>RSICs refreshed</h3><p>Richer website evidence improves SIC comparisons across Industry Engine, the API and Instant Classification.</p>{source('refresh')}</div></div>
      <div class="brief-takeaway"><small>MY INTERPRETATION / TO EXPLORE</small><p>As markets broaden, the opportunity is to make a sophisticated product <strong>easy to understand, relevant to each buyer and straightforward to adopt.</strong></p></div>
    </section>
    <section id="my-role" class="brief-section" aria-labelledby="role-brief-title"><div class="section-number">03 / MY POTENTIAL CONTRIBUTION</div><h2 id="role-brief-title">Connect customer need<br>to commercial value.</h2><p class="section-intro">A proposed <strong>Commercial AI Product / Pre-sales</strong> contribution — responsibilities and priorities to agree with the team.</p>
      <div class="role-brief-grid"><div><span class="role-symbol" aria-hidden="true">◎</span><h3>Discover the real need</h3><p>Understand processes, pains, implications and desired outcomes before choosing a solution.</p><strong>I bring</strong><p>Consultative pre-sales and the ability to surface challenges customers have not yet articulated.</p></div><div><span class="role-symbol" aria-hidden="true">↗</span><h3>Show, then progress</h3><p>Turn discovery into recognisable demonstrations, clear success criteria and an agreed next action.</p><strong>I bring</strong><p>Commercial storytelling, practical prototypes and tailored demos that help buyers see the value.</p></div><div><span class="role-symbol" aria-hidden="true">✦</span><h3>Apply AI deliberately</h3><p>Test where AI can improve discovery, explanation or workflows, with evidence boundaries and human review.</p><strong>I bring</strong><p>AI use-case prioritisation, solution shaping and go-to-market thinking.</p></div><div><span class="role-symbol" aria-hidden="true">↻</span><h3>Close the learning loop</h3><p>Connect website enquiries, sales handovers and customer feedback to product and positioning decisions.</p><strong>I bring</strong><p>A bridge between customer conversations, commercial teams and product development.</p></div></div>
      <div class="role-motion" aria-label="Proposed customer journey"><span>Understand</span><b aria-hidden="true">→</b><span>Demonstrate</span><b aria-hidden="true">→</b><span>Agree next step</span><b aria-hidden="true">→</b><span>Learn &amp; improve</span></div>
      <p class="brief-callout"><strong>RevOps angle:</strong> agree the context, owner and next action at each handover, then measure enquiry → demo → meaningful next step. Understand the existing process and baseline first.</p>
      <details class="interview-prompts"><summary>Three questions to take into the conversation</summary><ol><li>Which customer segments and markets matter most in the next phase?</li><li>What context would make each demonstration more relevant?</li><li>Where could I add the most value first: discovery, conversion, adoption or product learning?</li></ol></details>
      <div class="brief-actions"><a class="brief-primary" href="/">Open my demonstration ↗</a><a href="/role-at-data-city">Explore the proposed role ↗</a></div>
    </section></article>'''
