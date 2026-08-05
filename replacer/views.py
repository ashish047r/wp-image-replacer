import re
from django.shortcuts import render
from django.http import HttpResponse
from bs4 import BeautifulSoup, Tag

WP_BASE = "https://augmintech.com/wp-content/uploads"

AUGMINTECH_CSS = """
:root{
  --brand:#0F4C81;--brand-lite:#e8f2fc;--brand-border:#c8d8ec;
  --green:#18d104;--green-lite:#f0fdf0;--green-border:#9fd9c5;
  --coral:#c0471f;--coral-lite:#fdf0eb;--coral-border:#f5c4b3;
  --warn:#e67e22;--warn-lite:#fef9ef;--warn-border:#f5cc80;
  --teal:#0a6b8a;--teal-lite:#e8f8fc;--teal-border:#b3e0ec;
  --ink:#1a1a1a;--ink-mid:#555;--muted:#888;
  --surface:#f4f6f9;--white:#fff;--border:#e5e5e5;
  --radius:8px;
  --mono:'Courier New',monospace;--display:system-ui,sans-serif;
}
.aug-wrap *{box-sizing:border-box;margin:0;padding:0;}
.aug-wrap{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Oxygen-Sans,Ubuntu,Cantarell,"Helvetica Neue",sans-serif;font-size:16px;line-height:1.65em;color:#333;max-width:1200px;margin:0 auto;padding:20px 20px 60px;}
.aug-grid{display:block;max-width:820px;}
.aug-hr{border:none;border-top:1px solid #ddd;margin:20px 0 28px;}
.aug-h2{font-size:30px;font-weight:700;color:#1a1a1a;margin:36px 0 16px;line-height:1.25em;}
.aug-h2.underline{text-decoration:underline;text-underline-offset:4px;}
.aug-h2.green{color:#18d104;text-align:center;}
.aug-h3{font-size:20px;font-weight:700;color:#1a1a1a;margin:28px 0 12px;}
.aug-h4{font-size:16px;font-weight:700;color:#1a1a1a;margin:18px 0 8px;}
.aug-p{margin-bottom:16px;color:#333;font-size:16px;}
.aug-ul,.aug-ol{padding-left:28px;margin-bottom:18px;}
.aug-ul li,.aug-ol li{margin-bottom:8px;font-size:16px;color:#333;}
.aug-toc{background:#1a1a1a;border:2px solid #18d104;border-radius:6px;margin:28px 0 36px;overflow:hidden;}
.aug-toc-head{display:flex;align-items:center;justify-content:space-between;padding:14px 20px;cursor:pointer;background:#1a1a1a;border-bottom:1px solid #333;}
.aug-toc-head span{font-size:17px;font-weight:700;color:#fff;}
.aug-toc-toggle{color:#18d104;font-size:18px;user-select:none;}
.aug-toc-body{padding:16px 20px 20px;}
.aug-toc-body ol{padding-left:22px;margin:0;}
.aug-toc-body ol li{margin-bottom:8px;}
.aug-toc-body ol li a{color:#fff;text-decoration:none;font-size:15px;}
.aug-toc-body ol li a:hover{color:#18d104;}
.aug-toc-body ol ol{margin-top:8px;padding-left:20px;}
.aug-toc-body ol ol li a{color:#aaa;font-size:14px;}
.aug-table-wrap{overflow-x:auto;margin:16px 0 24px;}
.aug-table{width:100%;border-collapse:collapse;font-size:15px;}
.aug-table thead{background:#1a1a1a;color:#fff;}
.aug-table thead th{padding:11px 14px;text-align:left;font-weight:600;}
.aug-table tbody tr:nth-child(even){background:#f9f9f9;}
.aug-table td{padding:10px 14px;border:1px solid #e5e5e5;color:#333;vertical-align:top;}
.aug-table td:first-child{font-weight:600;}
.aug-formula{background:#18d104;color:#fff;border-radius:8px;padding:24px 20px;font-family:'Courier New',monospace;font-weight:700;text-align:center;margin:14px 0 22px;}
.aug-formula small{display:block;font-size:12px;letter-spacing:.18em;text-transform:uppercase;color:rgba(255,255,255,0.75);margin-bottom:14px;font-family:sans-serif;font-weight:600;}
.aug-formula .aug-fl{display:block;font-size:20px;margin:6px 0;}
.aug-formula .aug-fn{display:block;font-size:13px;font-weight:400;margin-top:12px;opacity:.9;font-family:sans-serif;line-height:1.7em;}
.aug-formula .aug-frac{display:inline-flex;flex-direction:column;align-items:center;vertical-align:middle;margin:0 4px;}
.aug-formula .aug-num{border-bottom:2px solid #fff;padding-bottom:3px;font-size:20px;}
.aug-formula .aug-den{padding-top:3px;font-size:20px;}
.aug-standards{background:#18d104;color:#fff;border-radius:14px;padding:32px 36px;margin:16px 0 24px;}
.aug-standards h4{font-size:11px;font-weight:800;letter-spacing:.22em;text-transform:uppercase;margin-bottom:22px;color:#fff;}
.aug-standards ul{padding-left:0;margin:0;list-style:none;}
.aug-standards ul li{margin-bottom:18px;font-size:16px;color:#fff;padding-left:26px;position:relative;line-height:1.5em;}
.aug-standards ul li:last-child{margin-bottom:0;}
.aug-standards ul li::before{content:'•';position:absolute;left:0;color:#fff;font-size:20px;line-height:1.3;}
.aug-standards ul li strong{font-weight:800;}
.aug-insight{border-left:4px solid #18d104;background:#f0fdf0;border-radius:0 8px 8px 0;padding:16px 20px;margin:16px 0 24px;}
.aug-insight p{margin:0;font-size:15px;color:#1a4d2e;line-height:1.7em;}
.aug-warn{border-left:4px solid #e67e22;background:#fef9ef;border-radius:0 8px 8px 0;padding:16px 20px;margin:16px 0 24px;}
.aug-warn p{margin:0;font-size:15px;color:#7a4200;line-height:1.7em;}
.aug-img-wrap{margin:24px 0 28px;text-align:center;}
.aug-img-wrap img{max-width:100%;height:auto;border-radius:6px;display:block;margin:0 auto;}
.aug-img-caption{font-size:13px;color:#888;margin-top:8px;font-style:italic;}
.aug-cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:14px;margin:16px 0 24px;}
.aug-card{background:#f9f9f9;border:1px solid #e5e5e5;border-radius:6px;padding:18px;}
.aug-card-icon{font-size:22px;margin-bottom:8px;display:block;}
.aug-card h4{font-size:13px;font-weight:700;text-transform:uppercase;color:#1a1a1a;margin-bottom:6px;letter-spacing:.04em;}
.aug-card p{font-size:13.5px;color:#555;margin:0;}
.aug-flow{background:#f9f9f9;border:1px solid #e5e5e5;border-radius:8px;padding:20px;margin:16px 0 24px;}
.aug-flow-title{font-size:13px;font-weight:600;color:#888;margin-bottom:16px;text-transform:uppercase;letter-spacing:.08em;}
.aug-flow-steps{display:grid;grid-template-columns:repeat(auto-fit,minmax(120px,1fr));gap:8px;}
.aug-flow-step{background:#fff;border:1px solid #e5e5e5;border-radius:6px;padding:12px;text-align:center;}
.aug-flow-num{font-size:11px;color:#18d104;font-weight:700;margin-bottom:6px;}
.aug-flow-name{font-size:12px;font-weight:600;color:#1a1a1a;line-height:1.4em;}
.aug-stat-row{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:12px;margin:20px 0 28px;}
.aug-stat-card{background:#f9f9f9;border:1px solid #e5e5e5;border-radius:8px;padding:16px;text-align:center;}
.aug-stat-num{font-size:28px;font-weight:700;color:#18d104;line-height:1;margin-bottom:6px;}
.aug-stat-label{font-size:12px;color:#666;line-height:1.5em;}
.aug-compare{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin:16px 0 24px;}
.aug-compare-col{border:1px solid #e5e5e5;border-radius:8px;padding:16px;}
.aug-compare-col.good{border-color:#18d104;background:#f0fdf0;}
.aug-compare-col .aug-compare-title{font-size:13px;font-weight:700;margin-bottom:10px;}
.aug-compare-col.good .aug-compare-title{color:#0a6e4f;}
.aug-compare-col.bad .aug-compare-title{color:#c0392b;}
.aug-compare-list{list-style:none;padding:0;margin:0;font-size:13px;color:#555;line-height:1.9em;}
.aug-career{display:flex;flex-direction:column;gap:8px;margin:16px 0 24px;}
.aug-cp-card{background:#f9f9f9;border:1px solid #e5e5e5;border-radius:8px;padding:14px 18px;border-left:4px solid #18d104;}
.aug-cp-title{font-size:15px;font-weight:700;color:#1a1a1a;margin-bottom:4px;}
.aug-cp-salary{font-size:13px;color:#18d104;font-weight:700;}
.aug-cp-skills{font-size:12px;color:#888;margin-top:4px;}
.aug-tag-row{display:flex;flex-wrap:wrap;gap:8px;margin:12px 0 20px;}
.aug-tag{display:inline-block;background:#f9f9f9;border:1px solid #e5e5e5;border-radius:20px;font-size:12px;padding:4px 12px;color:#555;}
.aug-cta-banner{background:#1a1a1a;border-radius:10px;padding:22px 26px;margin:24px 0;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:14px;}
.aug-cta-banner-text h3{font-size:17px;font-weight:700;color:#fff;margin-bottom:4px;}
.aug-cta-banner-text p{font-size:14px;color:rgba(255,255,255,0.7);margin:0;}
.aug-cta-btn{background:#18d104;color:#000;font-size:13px;font-weight:700;padding:10px 20px;border-radius:6px;text-decoration:none;white-space:nowrap;}
.aug-cta-btn:hover{background:#12b803;color:#000;text-decoration:none;}
.aug-faq-item{border-bottom:1px solid #e5e5e5;padding:16px 0;}
.aug-faq-q{font-size:16px;font-weight:700;color:#1a1a1a;margin-bottom:8px;}
.aug-faq-a{font-size:15px;color:#555;line-height:1.65em;}
.aug-wa-link{color:#18d104;font-weight:700;text-decoration:none;}
.aug-wa-link:hover{text-decoration:underline;}
.aug-teal{border-left:4px solid #00747d;background:#e0f5f7;border-radius:0 8px 8px 0;padding:16px 20px;margin:16px 0 24px;}
.aug-teal p{margin:0;font-size:15px;color:#003d42;line-height:1.7em;}
.steps{list-style:none;counter-reset:stp;padding:0;margin:16px 0 24px;}
.steps > li{counter-increment:stp;position:relative;padding:0 0 20px 40px;border-left:2px solid #e5e5e5;margin-left:15px;}
.steps > li:last-child{border-left-color:transparent;padding-bottom:0;}
.steps > li::before{content:counter(stp);position:absolute;left:-16px;top:-2px;width:30px;height:30px;border-radius:50%;background:#18d104;color:#000;font-weight:800;font-size:13.5px;display:flex;align-items:center;justify-content:center;}
.step-h{font-size:16.5px;font-weight:700;margin-bottom:8px;padding-top:4px;color:#1a1a1a;}
.eq{background:#f9f9f9;border:1px solid #e5e5e5;border-radius:8px;padding:18px 22px;margin:24px 0;}
.eq-title{font-size:11px;font-weight:600;letter-spacing:1.6px;text-transform:uppercase;color:#18d104;margin-bottom:12px;}
.eq-res{font-family:Georgia,'Times New Roman',serif;font-size:19px;font-weight:700;color:#0a6e4f;background:#f0fdf0;border:1px solid #9fd9c5;border-radius:6px;padding:6px 14px;display:inline-block;margin-top:8px;}
.eq-res.alt{color:#7a4200;background:#fef9ef;border-color:#f5cc80;}
.eq-note{font-size:14px;color:#666;line-height:1.7em;margin:12px 0 0;}
.eq-note strong{color:#1a1a1a;}
.eq-where{list-style:none;padding:0;margin:14px 0 0;border-top:1px solid #e5e5e5;padding-top:11px;}
.eq-where li{font-size:14px;color:#555;padding:3px 0;line-height:1.6;}
.eq-where .sym{font-family:Georgia,serif;font-style:italic;font-size:16px;color:#18d104;font-weight:700;display:inline-block;min-width:34px;}
.eq-sep{border-top:1px dashed #e5e5e5;margin:14px 0 12px;}
.math{font-family:'Cambria Math','Latin Modern Math',Georgia,'Times New Roman',serif;font-size:21px;line-height:1.35;color:#333;display:flex;align-items:center;flex-wrap:wrap;margin:12px 0;}
.math.ctr{justify-content:center;}
.math .var{font-style:italic;}
.math sub{font-size:.64em;vertical-align:-.3em;font-style:normal;}
.math sup{font-size:.64em;vertical-align:.55em;font-style:normal;}
.math .eqs{padding:0 .5em;}
.math .opr{padding:0 .32em;}
.math .unit{font-family:-apple-system,BlinkMacSystemFont,sans-serif;font-size:.6em;color:#888;font-style:normal;padding-left:.6em;letter-spacing:.2px;}
.math .res{color:#18d104;font-weight:700;}
.math .paren{font-size:1.25em;font-weight:300;padding:0 .05em;}
.frac{display:inline-flex;flex-direction:column;align-items:center;text-align:center;margin:0 .32em;vertical-align:middle;}
.frac > .num{padding:0 .55em .16em;border-bottom:1.6px solid currentColor;white-space:nowrap;}
.frac > .den{padding:.16em .55em 0;white-space:nowrap;}
.mathblock{background:#fff;border:1px solid #e5e5e5;border-radius:6px;padding:14px 18px;margin:14px 0;overflow-x:auto;}
.mathblock .math{margin:6px 0;}
.math-lbl{font-size:10px;letter-spacing:1.2px;text-transform:uppercase;color:#888;margin-bottom:6px;}
.mi{font-family:Georgia,'Times New Roman',serif;font-style:italic;font-size:1.04em;}
.mi sub{font-style:normal;font-size:.68em;}
.panel{background:linear-gradient(180deg,#f2fdf0 0%,#ffffff 60%);border:1px solid #cdeecb;border-top:4px solid #18d104;border-radius:12px;padding:26px 28px;margin:28px 0;box-shadow:0 4px 18px rgba(24,209,4,.12);}
.calc-head{display:inline-block;font-size:11px;font-weight:800;letter-spacing:1.6px;text-transform:uppercase;color:#fff;background:#18d104;padding:5px 14px;border-radius:20px;margin-bottom:18px;}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:14px;}
.grid3{display:grid;grid-template-columns:1fr 1fr 1fr;gap:14px;}
.grid4{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;}
.calc-label{display:block;font-size:12px;font-weight:700;color:#444;margin-bottom:6px;letter-spacing:.2px;}
.calc-input{width:100%;padding:12px 14px;border:1px solid transparent;border-radius:8px;background:#eef1ee;font-size:14px;color:#1a1a1a;box-sizing:border-box;font-family:inherit;transition:border-color .15s,background .15s;}
.calc-input:focus{outline:none;border-color:#18d104;background:#fff;}
select.calc-input{cursor:pointer;}
.calc-btn{display:inline-block;background:#18d104;color:#fff;border:none;border-radius:8px;padding:13px 30px;font-size:14px;font-weight:700;cursor:pointer;margin-top:20px;letter-spacing:.3px;font-family:inherit;box-shadow:0 3px 10px rgba(24,209,4,.35);}
.calc-btn:hover{background:#12b803;}
.calc-result{background:#fff;border:1px solid #cdeecb;border-left:4px solid #18d104;border-radius:8px;padding:14px 18px;margin-top:18px;font-size:14px;color:#333;line-height:1.65em;}
.rescard{background:#fff;border:1px solid #e5e5e5;border-radius:8px;padding:14px 16px;}
.rescard .rl{display:block;font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:.6px;color:#888;margin-bottom:5px;}
.rescard .rv{display:block;font-size:21px;font-weight:800;color:#1a1a1a;line-height:1.2;}
.rescard .rs{display:block;font-size:11px;color:#888;margin-top:4px;}
@media(max-width:640px){
  .grid3,.grid4{grid-template-columns:1fr 1fr;}
}
"""

# Standard SVG presentation attributes whose names are camelCase per spec.
# BeautifulSoup's html.parser lowercases every attribute name (correct for
# plain HTML, which is case-insensitive) but that silently breaks SVG, whose
# attribute names ARE case-sensitive -- viewbox="..." and markerwidth="8"
# are simply ignored by browsers. Restore the original casing after parsing.
SVG_CAMELCASE_ATTRS = [
    'allowReorder', 'attributeName', 'attributeType', 'autoReverse',
    'baseFrequency', 'baseProfile', 'calcMode', 'clipPathUnits',
    'contentScriptType', 'contentStyleType', 'diffuseConstant', 'edgeMode',
    'externalResourcesRequired', 'filterRes', 'filterUnits', 'glyphRef',
    'gradientTransform', 'gradientUnits', 'kernelMatrix', 'kernelUnitLength',
    'keyPoints', 'keySplines', 'keyTimes', 'lengthAdjust',
    'limitingConeAngle', 'markerHeight', 'markerUnits', 'markerWidth',
    'maskContentUnits', 'maskUnits', 'numOctaves', 'pathLength',
    'patternContentUnits', 'patternTransform', 'patternUnits',
    'pointsAtX', 'pointsAtY', 'pointsAtZ', 'preserveAlpha',
    'preserveAspectRatio', 'primitiveUnits', 'refX', 'refY',
    'repeatCount', 'repeatDur', 'requiredExtensions', 'requiredFeatures',
    'specularConstant', 'specularExponent', 'spreadMethod', 'startOffset',
    'stdDeviation', 'stitchTiles', 'surfaceScale', 'systemLanguage',
    'tableValues', 'targetX', 'targetY', 'textLength', 'viewBox',
    'viewTarget', 'xChannelSelector', 'yChannelSelector', 'zoomAndPan',
]
_SVG_ATTR_FIX_MAP = {a.lower(): a for a in SVG_CAMELCASE_ATTRS}
_SVG_ATTR_FIX_RE = re.compile(
    r'\b(' + '|'.join(re.escape(a) for a in _SVG_ATTR_FIX_MAP) + r')=',
    re.IGNORECASE,
)


def _restore_svg_attribute_case(html):
    return _SVG_ATTR_FIX_RE.sub(lambda m: _SVG_ATTR_FIX_MAP[m.group(1).lower()] + '=', html)


def _classes(tag):
    return tag.get('class', [])


def _has(tag, *names):
    classes = _classes(tag)
    return any(n in classes for n in names)


def apply_augmintech_theme(html):
    soup = BeautifulSoup(html, 'html.parser')

    # ── 1. Remove all <style> and <link rel=stylesheet>; keep <script> for interactivity ──
    for tag in soup.find_all('style'):
        tag.decompose()
    for tag in soup.find_all('link', rel=lambda r: r and 'stylesheet' in r):
        tag.decompose()

    # ── 2. Remove decorative-only elements ──
    for tag in soup.find_all(class_=lambda c: c and any(
        x in c for x in ['eyebrow', 'pill', 'pill-green', 'meta', 'progress']
    )):
        tag.decompose()
    prog = soup.find(id='progress')
    if prog:
        prog.decompose()

    # ── 3. h1 hero title → h2 aug-h2 (no h1 in Augmintech blogs) ──
    for tag in soup.find_all(class_=lambda c: c and 'hero-title' in c):
        tag.name = 'h2'
        tag['class'] = ['aug-h2']
    for tag in soup.find_all('h1'):
        tag.name = 'h2'
        tag['class'] = ['aug-h2']

    # ── 4. hero-sub → aug-p ──
    for tag in soup.find_all(class_=lambda c: c and 'hero-sub' in c):
        tag.name = 'p'
        tag['class'] = ['aug-p']

    # ── 5. Headings ──
    for tag in soup.find_all('h2'):
        tag['class'] = ['aug-h2']
    for tag in soup.find_all('h3'):
        tag['class'] = ['aug-h3']
    for tag in soup.find_all('h4'):
        tag['class'] = ['aug-h4']

    # ── 6. Paragraphs ──
    for tag in soup.find_all('p'):
        tag['class'] = ['aug-p']

    # ── 7. Lists ──
    # 'steps' (numbered worked-solution lists) and 'eq-where' (equation
    # symbol legends) carry their own dedicated CSS above and must not be
    # collapsed into the generic bullet/number styles.
    PRESERVE_LIST_CLASSES = ('steps', 'eq-where')
    for tag in soup.find_all('ul'):
        if _has(tag, *PRESERVE_LIST_CLASSES):
            continue
        tag['class'] = ['aug-ul']
    for tag in soup.find_all('ol'):
        if _has(tag, *PRESERVE_LIST_CLASSES):
            continue
        tag['class'] = ['aug-ol']

    # ── 8. HR ──
    for tag in soup.find_all('hr'):
        tag['class'] = ['aug-hr']

    # ── 9. Tables → wrap in aug-table-wrap ──
    for table in soup.find_all('table'):
        table['class'] = ['aug-table']
        # unwrap any existing .tbl-wrap first
        parent = table.parent
        if parent and isinstance(parent, Tag) and _has(parent, 'tbl-wrap'):
            parent.unwrap()
        wrap = soup.new_tag('div', attrs={'class': 'aug-table-wrap'})
        table.insert_before(wrap)
        wrap.append(table.extract())

    # ── 10. figure + figcaption → aug-img-wrap ──
    for fig in soup.find_all('figure'):
        fig.name = 'div'
        fig['class'] = ['aug-img-wrap']
    for fig in soup.find_all('figcaption'):
        fig.name = 'p'
        fig['class'] = ['aug-img-caption']

    # ── 11. Stat strip ──
    for tag in soup.find_all(class_=lambda c: c and ('stats' in c or 'stat-row' in c)):
        tag['class'] = ['aug-stat-row']
    for tag in soup.find_all(class_=lambda c: c and c == ['stat']):
        tag['class'] = ['aug-stat-card']
    for tag in soup.find_all(class_=lambda c: c and 'stat-n' in c):
        tag['class'] = ['aug-stat-num']
    for tag in soup.find_all(class_=lambda c: c and 'stat-l' in c):
        tag['class'] = ['aug-stat-label']

    # ── 12. Cards ──
    for tag in soup.find_all(class_=lambda c: c and ('card-grid' in c or 'cards' in c)):
        tag['class'] = ['aug-cards']
    for tag in soup.find_all(class_=lambda c: c and c == ['card']):
        tag['class'] = ['aug-card']
    for tag in soup.find_all(class_=lambda c: c and 'card-title' in c):
        tag.name = 'h4'
        tag['class'] = []
    for tag in soup.find_all(class_=lambda c: c and 'card-desc' in c):
        tag.name = 'p'
        tag['class'] = []
    for tag in soup.find_all(class_=lambda c: c and 'card-icon' in c):
        tag['class'] = ['aug-card-icon']

    # ── 13a. TL;DR → aug-standards (green rounded box, per Augmintech spec) ──
    for tag in soup.find_all(lambda t: 'tldr' in (t.get('class') or [])):
        tag['class'] = ['aug-standards']
        # tldr-head label → h4
        for label in tag.find_all(lambda t: any(
            c in (t.get('class') or []) for c in ['tldr-head', 'tldr-title']
        )):
            label.name = 'h4'
            label['class'] = []
        # ul inside tldr keeps its list but strip class
        for ul in tag.find_all('ul'):
            ul['class'] = []
        for p in tag.find_all('p'):
            p['class'] = []

    # ── 13b. Inline callout boxes ──
    # box-green / box-blue → aug-insight (left green border)
    for tag in soup.find_all(lambda t: any(
        c in (t.get('class') or []) for c in ['box-green', 'box-blue', 'insight']
    )):
        tag['class'] = ['aug-insight']
        for p in tag.find_all('p'):
            p['class'] = []
        for label in tag.find_all(lambda t: any(
            c in (t.get('class') or []) for c in ['box-label', 'box-title']
        )):
            label.name = 'h4'
            label['class'] = []

    # box-warn / box-coral / box-purple → aug-warn (left orange border)
    for tag in soup.find_all(lambda t: any(
        c in (t.get('class') or []) for c in ['box-warn', 'box-coral', 'box-purple']
    )):
        tag['class'] = ['aug-warn']
        for p in tag.find_all('p'):
            p['class'] = []
        for label in tag.find_all(lambda t: any(
            c in (t.get('class') or []) for c in ['box-label', 'box-title']
        )):
            label.name = 'h4'
            label['class'] = []

    # box-teal → aug-teal (left teal border). Previously unhandled entirely,
    # so its class fell through to the OLD_PREFIXES cleanup below and got
    # deleted outright, leaving a bare unstyled <div>.
    for tag in soup.find_all(lambda t: 'box-teal' in (t.get('class') or [])):
        tag['class'] = ['aug-teal']
        for p in tag.find_all('p'):
            p['class'] = []
        for label in tag.find_all(lambda t: any(
            c in (t.get('class') or []) for c in ['box-label', 'box-title']
        )):
            label.name = 'h4'
            label['class'] = []

    # ── 14. TOC — rebuild full aug-toc structure ──
    # A source draft occasionally has a TOC block duplicated by accident during
    # editing. If we styled every match, each one would become its own aug-toc
    # box stacked in the output. Keep only the first; drop any extras entirely.
    toc_matches = soup.find_all(lambda t: 'toc' in (t.get('class') or []))
    for extra_toc in toc_matches[1:]:
        extra_toc.decompose()

    for toc in toc_matches[:1]:
        toc['class'] = ['aug-toc']

        # Find or create the head element
        head_el = toc.find(lambda t: any(
            c in (t.get('class') or []) for c in ['toc-title', 'toc-head', 'toc-label']
        ))

        if head_el:
            # Grab the text, rebuild head with span + toggle
            label_text = head_el.get_text(strip=True) or 'Table of Contents'
            head_el.clear()
            head_el['class'] = ['aug-toc-head']
            head_el['onclick'] = "var b=this.nextElementSibling;b.style.display=b.style.display==='none'?'block':'none';this.querySelector('.aug-toc-toggle').textContent=b.style.display==='none'?'∨':'∧'"
            span_title = soup.new_tag('span')
            span_title.string = label_text
            span_toggle = soup.new_tag('span', attrs={'class': 'aug-toc-toggle'})
            span_toggle.string = '∧'
            head_el.append(span_title)
            head_el.append(span_toggle)
        else:
            # No title element — inject one at the top
            head_el = soup.new_tag('div', attrs={'class': 'aug-toc-head'})
            head_el['onclick'] = "var b=this.nextElementSibling;b.style.display=b.style.display==='none'?'block':'none';this.querySelector('.aug-toc-toggle').textContent=b.style.display==='none'?'∨':'∧'"
            span_title = soup.new_tag('span')
            span_title.string = 'Table of Contents'
            span_toggle = soup.new_tag('span', attrs={'class': 'aug-toc-toggle'})
            span_toggle.string = '∧'
            head_el.append(span_title)
            head_el.append(span_toggle)
            toc.insert(0, head_el)

        # Wrap the <ol>/<ul> list in aug-toc-body
        toc_list = toc.find(['ol', 'ul'])
        if toc_list:
            # Check if already inside a toc-body div
            existing_body = toc.find(lambda t: 'toc-body' in (t.get('class') or []))
            if existing_body:
                existing_body['class'] = ['aug-toc-body']
            else:
                body_div = soup.new_tag('div', attrs={'class': 'aug-toc-body'})
                toc_list.insert_before(body_div)
                body_div.append(toc_list.extract())

        # Style links white — strip any class from inner ol/ul/li/a
        for inner in toc.find_all(['ol', 'ul', 'li', 'a']):
            if 'class' in inner.attrs:
                del inner.attrs['class']

    # ── 15. CTA banners ──
    # Step 1: mark buttons first (before container matching touches them)
    for btn in soup.find_all(lambda t: any(
        c in (t.get('class') or []) for c in ['cta-btn', 'cta-btn-blue', 'cta-btn-green']
    )):
        btn['class'] = ['aug-cta-btn']

    # Step 2: match CTA containers with EXACT class check (not substring)
    for tag in soup.find_all(lambda t: t.name in ['div', 'section', 'a'] and any(
        c in ['cta', 'cta-green', 'cta-blue'] for c in (t.get('class') or [])
    ) and not any(
        c in ['aug-cta-btn'] for c in (t.get('class') or [])
    )):
        tag['class'] = ['aug-cta-banner']
        # Wrap non-button children in aug-cta-banner-text div
        text_div = soup.new_tag('div', attrs={'class': 'aug-cta-banner-text'})
        for child in list(tag.children):
            if isinstance(child, Tag) and 'aug-cta-btn' not in (child.get('class') or []):
                text_div.append(child.extract())
        if text_div.contents:
            tag.insert(0, text_div)

    # ── 16. Tags strip ──
    for tag in soup.find_all(class_=lambda c: c and c == ['tags']):
        tag['class'] = ['aug-tag-row']
    for tag in soup.find_all(class_=lambda c: c and c == ['tag']):
        tag['class'] = ['aug-tag']

    # ── 17. FAQ ──
    for tag in soup.find_all(class_=lambda c: c and 'faq-item' in c):
        tag['class'] = ['aug-faq-item']
    for tag in soup.find_all(class_=lambda c: c and 'faq-q' in c):
        tag['class'] = ['aug-faq-q']
    for tag in soup.find_all(class_=lambda c: c and 'faq-a' in c):
        tag['class'] = ['aug-faq-a']

    # ── 18. Strip leftover class attrs that are old custom classes ──
    OLD_PREFIXES = ('blog', 'step-list', 'step-title', 'tip-list', 'tip-title',
                    'tbl-', 'box ', 'box-', 'pill', 'hero', 'eyebrow')
    for tag in soup.find_all(True):
        old = tag.get('class', [])
        if old and any(any(c.startswith(p) for p in OLD_PREFIXES) for c in old):
            del tag['class']

    # ── 19. Wrap body content in aug-wrap > aug-grid > aug-article ──
    body = soup.find('body')
    if body:
        inner_tags = list(body.children)
        article = soup.new_tag('div', attrs={'class': 'aug-article'})
        grid = soup.new_tag('div', attrs={'class': 'aug-grid'})
        wrap = soup.new_tag('div', attrs={'class': 'aug-wrap'})
        for child in inner_tags:
            article.append(child.extract())
        grid.append(article)
        wrap.append(grid)
        body.append(wrap)

    # ── 20. Inject Augmintech CSS into <head> ──
    head = soup.find('head')
    if not head:
        head = soup.new_tag('head')
        soup.insert(0, head)
    style_tag = soup.new_tag('style')
    style_tag.string = AUGMINTECH_CSS
    head.append(style_tag)

    # ── 21. Restore SVG attribute casing lowercased by html.parser ──
    return _restore_svg_attribute_case(str(soup))


def index(request):
    if request.method == 'GET':
        return render(request, 'index.html')

    html_file = request.FILES.get('html_file')
    images = request.FILES.getlist('images')
    year_month = request.POST.get('year_month', '').strip()
    apply_theme = request.POST.get('apply_theme') == 'on'

    errors = []
    if not html_file:
        errors.append('Please upload an HTML file.')
    if not year_month:
        errors.append('Please enter a year/month (e.g. 2026/05).')

    if errors:
        return render(request, 'index.html', {'errors': errors})

    html_content = html_file.read().decode('utf-8')

    # ── Replace base64 images with WordPress URLs ──
    pattern = re.compile(r'src="data:image/(?:png|jpeg|jpg|gif|webp);base64,[^"]+"')
    matches = list(pattern.finditer(html_content))

    if len(matches) == 0 and len(images) == 0:
        pass  # no base64 images in HTML and none uploaded — proceed (theme-only run)
    elif len(matches) != len(images):
        return render(request, 'index.html', {
            'errors': [
                f'HTML has {len(matches)} base64 image(s) but you uploaded {len(images)} image(s). '
                f'They must match exactly.'
            ]
        })

    for match, img_file in zip(matches, images):
        wp_url = f"{WP_BASE}/{year_month}/{img_file.name}"
        html_content = html_content.replace(match.group(0), f'src="{wp_url}"', 1)

    # ── Apply Augmintech theme if checked ──
    if apply_theme:
        html_content = apply_augmintech_theme(html_content)

    out_filename = html_file.name.replace('.html', '_updated.html')
    response = HttpResponse(html_content, content_type='text/html; charset=utf-8')
    response['Content-Disposition'] = f'attachment; filename="{out_filename}"'
    return response
