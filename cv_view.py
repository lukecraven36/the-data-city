"""Accessible timeline from Luke's supplied CV and confirmed correspondence."""
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def esc(value):
    return html.escape(str(value), quote=True)

def bullets(items, css):
    return '<ul class="' + css + '">' + ''.join('<li>' + esc(item) + '</li>' for item in items) + '</ul>'

def full_detail(detail, label='Full detail', note=''):
    body = bullets(detail, 'cv-full-list') if isinstance(detail, list) else '<p>' + esc(detail) + '</p>'
    return '<details class="cv-detail"><summary>' + esc(label) + '<span class="cv-detail-icon" aria-hidden="true"></span></summary><div class="cv-detail-body">' + body + ('<p class="cv-source">' + esc(note) + '</p>' if note else '') + '</div></details>'

def section_card(title, section, identifier):
    return f'<section class="cv-support" id="{identifier}"><h2>{esc(title)}</h2>{bullets(section["summary"], "cv-highlights")}{full_detail(section["detail"])}</section>'

def render():
    cv = json.loads((ROOT / 'data/cv.json').read_text(encoding='utf-8'))
    roles = ''
    for role in cv['roles']:
        tag = '<span class="cv-current">Current role</span>' if role.get('current') else ''
        location = '<span> · ' + esc(role['location']) + '</span>' if role.get('location') else ''
        verification = '<p class="cv-verification">' + esc(role['verification']) + '</p>' if role.get('verification') else ''
        roles += f'''<li class="cv-entry" id="{esc(role['id'])}"><div class="cv-year" aria-hidden="true">{esc(role['year'])}</div><article class="cv-card"><div class="cv-role-meta"><span>{esc(role['dates'])}{location}</span>{tag}</div><h3>{esc(role['title'])}</h3><p class="cv-employer">{esc(role['company'])}</p>{bullets(role['summary'], 'cv-highlights')}{verification}{full_detail(role['detail'], 'Full role detail', role['source'])}</article></li>'''
    return f'''<div class="eyebrow">04 / About Me · Luke Craven</div><h1>My experience.<br><em>In context.</em></h1><p class="intro">From supply-chain analytics to customer discovery and AI presales. Three highlights from each chapter; open any section for the full detail.</p>
    <div class="cv-jumps" aria-label="CV sections"><a href="#career">Career timeline ↓</a><a href="#skills">Skills ↓</a><a href="#interests">Beyond work ↓</a></div>
    <div class="cv-controls" hidden><span>Explore at your own pace</span><div><button type="button" id="cv-expand">Expand all</button><button type="button" id="cv-collapse">Collapse all</button></div></div>
    {section_card('What I bring', cv['profile'], 'profile')}
    <section id="career" aria-labelledby="career-title"><div class="section-heading"><div><span class="eyebrow">The career timeline</span><h2 id="career-title">Experience, chapter by chapter</h2></div></div><p class="small">Most recent first. Career dates, titles and achievements come from my supplied CV, supplemented by confirmed Simpson Associates correspondence and my account of the current role.</p><ol class="cv-timeline">{roles}</ol></section>
    <div class="cv-support-grid">{section_card('Skills & strengths',cv['skills'],'skills')}{section_card('Beyond work',cv['interests'],'interests')}</div>
    {section_card('Additional background · Pathed Consulting',cv['pathed'],'pathed')}
    <section class="cv-support cv-reconnect"><span class="eyebrow">Looking ahead</span><h2>Why I would like to reconnect</h2>{bullets(['I previously chose an AI-focused opportunity with Simpson Associates.', 'Customer conversations have given me a clearer view of where I can contribute.', 'I would like to discuss customer discovery, useful products and practical AI value at The Data City.'], 'cv-highlights')}{full_detail(['When Natalia and I spoke previously, I chose an AI-focused opportunity with Simpson Associates involving Microsoft. At the time, I did not fully appreciate how central AI already was to The Data City’s business, or where you were taking it.', 'Since then, I have spent more time with customers understanding their AI needs and the problems they want to solve. That experience has made me reflect on where I work best and what I want to contribute. Looking back, I wonder whether I got the decision wrong.', 'I would like to reopen the conversation with a clearer view of how I could help: understanding customers and the market, shaping useful products and turning AI ambition into practical customer value.'], 'Read my reflection', 'Personal draft · review before sharing.')}</section>
    <aside class="note"><strong>Still to confirm:</strong> the full Simpson Associates role description; Pathed Consulting’s formal role and dates; and Natalia’s spelling before correspondence. Achievements are presented as supplied in my CV.</aside><p class="cv-action-status sr-only" role="status" aria-live="polite"></p>'''
