"""Accessible timeline from Luke's supplied CV and confirmed correspondence."""
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def esc(value):
    return html.escape(str(value), quote=True)

def bullets(items, css):
    return '<ul class="' + css + '">' + ''.join('<li>' + esc(item) + '</li>' for item in items) + '</ul>'

def full_detail(detail, label='Full detail', prose=False):
    body = (''.join('<p>' + esc(item) + '</p>' for item in detail) if prose else bullets(detail, 'cv-full-list')) if isinstance(detail, list) else '<p>' + esc(detail) + '</p>'
    return '<details class="cv-detail"><summary>' + esc(label) + '<span class="cv-detail-icon" aria-hidden="true"></span></summary><div class="cv-detail-body">' + body + '</div></details>'

def section_card(title, section, identifier):
    profile = identifier == 'profile'
    label = '<span class="eyebrow">Discovery → opportunity → growth</span>' if profile else ''
    highlights = ('<ul class="cv-highlights">' + ''.join('<li><strong>' + esc(item.partition(':')[0]) + ':</strong>' + esc(item.partition(':')[2]) + '</li>' for item in section['summary']) + '</ul>') if profile else bullets(section['summary'], 'cv-highlights')
    return f'<section class="cv-support{" cv-profile" if profile else ""}" id="{identifier}">{label}<h2>{esc(title)}</h2>{highlights}{full_detail(section["detail"], "The experience behind these strengths" if profile else "Full detail", prose=profile)}</section>'

def render():
    cv = json.loads((ROOT / 'data/cv.json').read_text(encoding='utf-8'))
    roles = ''
    for role in cv['roles']:
        tag = '<span class="cv-current">Current role</span>' if role.get('current') else ''
        location = '<span> · ' + esc(role['location']) + '</span>' if role.get('location') else ''
        verification = '<p class="cv-verification">' + esc(role['verification']) + '</p>' if role.get('verification') else ''
        roles += f'''<li class="cv-entry" id="{esc(role['id'])}"><div class="cv-year" aria-hidden="true">{esc(role['year'])}</div><article class="cv-card"><div class="cv-role-meta"><span>{esc(role['dates'])}{location}</span>{tag}</div><h3>{esc(role['title'])}</h3><p class="cv-employer">{esc(role['company'])}</p>{bullets(role['summary'], 'cv-highlights')}{verification}{full_detail(role['detail'], 'Full role detail', prose=role.get('detail_prose', False))}</article></li>'''
    skill_tags = '<ul class="cv-skill-tags" aria-label="Skills at a glance">' + ''.join('<li><a href="#skills">' + esc(skill) + '</a></li>' for skill in cv['skills']['tags']) + '</ul>'
    return f'''<div class="eyebrow">03 / About Me · Luke Craven</div><h1>My experience.<br><em>In context.</em></h1><p class="intro cv-intro">Understanding the challenge. Finding the opportunity. Turning customer conversations into practical solutions and commercial growth.</p>
    {skill_tags}
    <div class="cv-jumps" aria-label="CV sections"><a href="#career">Career timeline ↓</a><a href="#skills">Skills ↓</a><a href="#interests">Beyond work ↓</a></div>
    <div class="cv-controls" hidden><span>Explore at your own pace</span><div><button type="button" id="cv-expand">Expand all</button><button type="button" id="cv-collapse">Collapse all</button></div></div>
    {section_card('What I bring', cv['profile'], 'profile')}
    <section id="career" aria-labelledby="career-title"><div class="section-heading"><div><span class="eyebrow">The career timeline</span><h2 id="career-title">Experience, chapter by chapter</h2></div></div><p class="small">Most recent first. Open each chapter to explore the full role.</p><ol class="cv-timeline">{roles}</ol></section>
    <div class="cv-support-grid">{section_card('Skills & strengths',cv['skills'],'skills')}{section_card('Beyond work',cv['interests'],'interests')}</div>
    {section_card('Additional background · Pathed Consulting',cv['pathed'],'pathed')}
    <section class="cv-support cv-reconnect"><span class="eyebrow">Looking ahead</span><h2>Why I would like to reconnect</h2>{bullets(['I previously chose an AI-focused opportunity with Simpson Associates.', 'Customer conversations have given me a clearer view of where I can contribute.', 'I would like to discuss customer discovery, useful products and practical AI value at The Data City.'], 'cv-highlights')}{full_detail(['When Mitali and I spoke previously, I chose an AI-focused opportunity with Simpson Associates involving Microsoft. At the time, I did not fully appreciate how central AI already was to The Data City’s business, or where you were taking it.', 'Since then, I have spent more time with customers understanding their AI needs and the problems they want to solve. That experience has made me reflect on where I work best and what I want to contribute. Looking back, I wonder whether I got the decision wrong.', 'I would like to reopen the conversation with a clearer view of how I could help: understanding customers and the market, shaping useful products and turning AI ambition into practical customer value.'], 'Read my reflection')}</section>
    <aside class="note"><strong>Still to confirm:</strong> Pathed Consulting’s formal role and dates.</aside><p class="cv-action-status sr-only" role="status" aria-live="polite"></p>'''
