"""An independent, offline interview presentation; no provider or personal data."""
from html import escape

STAGES = [
    ('attract', 'Attract', 'A relevant sector or problem-led entry.', 'Source · interest · audience', 'Entry context', 'A sector-led page brings a relevant question into focus.', 'Potential handoff', 'Source, interest theme and intended audience.'),
    ('explore', 'Explore', 'Three questions. A useful prepared preview.', 'Challenge · use case · outcome', 'Customer signal', 'The customer describes a challenge and the outcome they want.', 'Potential handoff', 'A discovery brief; contact details only when deliberately supplied, with clear consent.'),
    ('qualify', 'Qualify', 'Understand need, urgency and fit.', 'Context · owner · routing', 'Shared understanding', 'Check what matters, when it matters and whether there is a fit.', 'To agree with the team', 'Qualified context, an owner and routing rules to validate.'),
    ('demonstrate', 'Demonstrate', 'A tailored session, informed by discovery.', 'Brief · stakeholders · next action', 'Demonstration brief', 'Carry the original questions into a relevant conversation.', 'Potential handoff', 'Stakeholders, an agreed success criterion and a clear next action.'),
    ('learn', 'Learn & grow', 'Feedback, adoption questions and repeated needs.', 'Follow-up · adoption · product', 'Learning signal', 'Capture the outcome and questions that recur across conversations.', 'Potential handoff', 'Product insight and, where applicable, onboarding or expansion learning.'),
]


def render():
    steps = ''.join(f'''<li><button type="button" id="stage-{key}" aria-controls="handoff-{key}" class="journey-stage"><span class="stage-number">0{i}</span><strong>{name}</strong><span>{experience}</span><small>{signal}</small><span class="stage-hint" aria-hidden="true">View handoff ↗</span></button></li>''' for i, (key, name, experience, signal, *_) in enumerate(STAGES, 1))
    panels = ''.join(f'''<div class="handoff-panel" id="handoff-{key}" aria-labelledby="stage-{key}"><div><small>{label}</small><p>{escape(example)}</p></div><div><small>{handoff}</small><p>{escape(detail)}</p></div></div>''' for key, name, experience, signal, label, example, handoff, detail in STAGES)
    return f'''<article class="interview-story">
    <header class="interview-hero"><div class="eyebrow">INTERVIEW / A PROPOSED CONTRIBUTION</div><p class="proposal-label">Independent proposal for discussion</p>
    <h1>From first interest to<br><em>lasting customer value.</em></h1>
    <p class="interview-intro">A connected approach to customer discovery, practical AI and Revenue Operations — making the experience more relevant for customers and more useful for the business.</p>
    <ul class="theme-tags" aria-label="Focal themes"><li>Customer journey</li><li>Commercial delivery</li><li>AI &amp; product insight</li></ul>
    <div class="interview-actions"><a class="interview-primary" href="/">Explore the live demonstration <span aria-hidden="true">↗</span></a><a href="/role-at-data-city">See the role in more detail <span aria-hidden="true">↗</span></a></div>
    </header>
    <nav class="interview-index" aria-label="Interview sections"><a href="#built">01 / The demo</a><a href="#contribution">02 / Contribution</a><a href="#journey">03 / The journey</a><a href="#start">04 / First 90 days</a></nav>

    <section id="built" class="interview-section"><div class="section-kicker">01 / ALREADY BUILT</div><h2>Show something useful before<br>asking for another meeting.</h2>
    <ol class="demo-storyboard"><li><small>01 / Understand</small><p>A customer challenge. <br>Three contextual questions.</p></li><li><small>02 / Show</small><p>A prepared insight preview. <br>Illustrative visualisations.</p></li><li><small>03 / Progress</small><p>A tailored demonstration. <br>A meaningful next action.</p></li></ol>
    <a class="demo-miniature" href="/" aria-label="Open the existing Discover Your Market demonstration"><span class="mini-brief"><span class="mini-label">Discovery brief</span><span class="mini-line"></span><span class="mini-line short"></span><span class="mini-line"></span></span><span class="mini-insight"><span class="mini-label">Prepared market insight</span><span class="mini-sectors"><span>Companies</span><span>Sectors</span><span>Locations</span></span></span><span class="mini-next"><span class="mini-label">Next conversation</span><strong>A more relevant demo ↗</strong></span></a>
    <p class="interview-caption">Existing offline demo · prepared sample, illustrative financials · no live AI or CRM submission.</p></section>

    <section id="contribution" class="interview-section"><div class="section-kicker">02 / WHERE I COULD CONTRIBUTE</div><h2>Customer need first. AI as an enabler.</h2>
    <div class="contribution-grid"><div><span class="contribution-icon" aria-hidden="true">↗</span><h3>Commercial &amp; pre-sales</h3><p>Qualify the need, build relevant demos, clarify the next step.</p></div><div><span class="contribution-icon" aria-hidden="true">✦</span><h3>AI application</h3><p>Accelerate discovery and explanation, with human review and clear evidence boundaries.</p></div><div><span class="contribution-icon" aria-hidden="true">◎</span><h3>Product &amp; customer insight</h3><p>Turn recurring questions and objections into product direction.</p></div></div>
    <div class="shared-motion"><span aria-hidden="true">↳</span> One customer-centred motion <span aria-hidden="true">↲</span><a href="/role-at-data-city">Explore the proposed role ↗</a></div></section>

    <section id="journey" class="interview-section journey-section"><div class="section-kicker">03 / A PROPOSED REVOPS MODEL</div><h2>One connected journey. <br><em>Fewer blind handovers.</em></h2>
    <p class="journey-context">Connect interest, insight, conversations and product learning — subject to validating the current process with the team.</p>
    <p class="interview-caption journey-instruction">Select a stage to explore an illustrative handoff.</p>
    <ol class="journey-flow" aria-label="Proposed customer journey">{steps}</ol>
    <div class="feedback-loop"><span class="loop-return" aria-hidden="true">↶</span><strong>Learn &amp; grow</strong><span>feeds back into</span><span class="loop-destination">Attract + Explore</span><span class="loop-destination product-destination">Product</span></div>
    <div class="handoff-examples"><p class="handoff-label">ILLUSTRATIVE / TO VALIDATE</p>{panels}</div>
    <div class="value-levers"><p><strong>Better context</strong>Relevant first conversations.</p><p><strong>Cleaner handovers</strong>Right information, right person.</p><p><strong>Stronger learning</strong>Needs inform positioning, demos and product.</p></div>
    <p class="revops-definition"><strong>RevOps, in plain English:</strong> joined-up process, data, handovers, responsibilities and measures across marketing, sales, customer success and feedback to product.</p></section>

    <section id="start" class="interview-section"><div class="section-kicker">04 / WHERE I'D START</div><h2>Listen. Test. Make it repeatable.</h2><p class="interview-caption">A suggested 30 / 60 / 90-day hypothesis, shaped with the team.</p>
    <ol class="start-rail"><li><span class="day-number">30<small>FIRST DAYS</small></span><h3>Listen &amp; map</h3><p>Map actual stages, systems, friction and baseline with the team.</p><small class="output-label">OUTPUT</small><strong>Shared journey map. <br>Prioritised questions.</strong></li><li><span class="day-number">60<small>DAYS 31–60</small></span><h3>Prototype &amp; test</h3><p>Pilot one segment’s discovery-to-demo handoff.</p><small class="output-label">OUTPUT</small><strong>Measurable pilot. <br>Reusable demo brief.</strong></li><li><span class="day-number">90<small>DAYS 61–90</small></span><h3>Refine &amp; operationalise</h3><p>Review evidence, agree responsibilities, routing and feedback; decide whether to scale.</p><small class="output-label">OUTPUT</small><strong>Agreed playbook. <br>Metrics and product insight.</strong></li></ol></section>

    <section class="interview-measures" aria-labelledby="measure-title"><h2 id="measure-title">What would we measure?</h2><p>Baseline first. Agree measures with the team.</p><ul><li>Website enquiry → meaningful engagement</li><li>Qualified enquiry → demo</li><li>Demo → agreed next step</li><li>Time to first useful insight</li><li>Trial/onboarding progression <small>(if applicable)</small></li></ul></section>
    <section class="interview-close"><div class="section-kicker">LET'S DISCUSS</div><ol><li>Where does customer interest lose momentum, if anywhere?</li><li>What context reaches the person running the demo, and what gets lost?</li><li>Which RevOps outcome matters most: conversion, speed, handover quality, adoption — or something else?</li></ol><p>I'd start by understanding what already works, then help make the next part more connected and repeatable.</p><a class="interview-primary" href="/">Explore the full demonstration <span aria-hidden="true">↗</span></a></section>
    </article>'''
