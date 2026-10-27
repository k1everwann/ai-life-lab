"""Focused validation for the public learning materials."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse, unquote
from datetime import date
from decimal import Decimal
import csv
import importlib.util
import json
import os
import re
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
NODE=os.environ.get("AI_LAB_NODE","node")
errors=[]
checks=[]
class Doc(HTMLParser):
    def __init__(self):
        super().__init__();self.ids=set();self.refs=[];self.duplicates=[];self.scripts=[];self.current_script=None;self.lang=None
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=="html":self.lang=a.get("lang")
        if a.get("id"):
            if a["id"] in self.ids:self.duplicates.append(a["id"])
            self.ids.add(a["id"])
        for key in ("href","src"):
            if key in a:self.refs.append(a[key])
        if tag=="script" and "src" not in a:self.current_script=[]
    def handle_data(self,data):
        if self.current_script is not None:self.current_script.append(data)
    def handle_endtag(self,tag):
        if tag=="script" and self.current_script is not None:
            self.scripts.append("".join(self.current_script));self.current_script=None

docs={}
for file in ROOT.rglob("*.html"):
    if ".qa" in file.parts:continue
    doc=Doc();doc.feed(file.read_text(encoding="utf-8"));docs[file.resolve()]=doc
    if doc.duplicates:errors.append(f"{file.name}: duplicate IDs {doc.duplicates}")
    expected_lang="en" if "en" in file.relative_to(ROOT).parts else "zh-Hant"
    if doc.lang!=expected_lang:errors.append(f"{file.relative_to(ROOT)}: expected {expected_lang} lang")
for file,doc in docs.items():
    for ref in doc.refs:
        parts=urlparse(ref)
        if parts.scheme or parts.netloc or ref.startswith("data:"):continue
        dest=(file.parent/unquote(parts.path)).resolve() if parts.path else file
        if not dest.is_file():errors.append(f"{file.name}: missing local file {ref}")
        if parts.fragment and dest in docs and unquote(parts.fragment) not in docs[dest].ids:
            errors.append(f"{file.name}: missing anchor {ref}")
checks.append(f"HTML local references and anchors: {len(docs)} pages")

# Both languages must offer the complete activity, not just translated headings.
for relative in ("index.html", "instructor.html", "next-steps.html", "examples/starter.html", "examples/my-checklist.html"):
    zh=ROOT/relative; en=ROOT/"en"/relative
    if not zh.is_file() or not en.is_file():
        errors.append(f"Bilingual counterpart missing: {relative}");continue
    for page in (zh,en):
        content=page.read_text(encoding="utf-8")
        if 'data-language-switch="zh-Hant"' not in content or 'data-language-switch="en"' not in content:
            errors.append(f"{page.relative_to(ROOT)}: missing top language switch")
for relative in ("index.html", "en/index.html"):
    doc=docs.get((ROOT/relative).resolve())
    required={"phone-panel","computer-panel","beginner-start","build-prompt","html-code","code-preview","takeaway"}
    if not doc or not required.issubset(doc.ids):errors.append(f"{relative}: incomplete learner route")
for relative in ("script.js", "en/script.js"):
    code=(ROOT/relative).read_text(encoding="utf-8") if (ROOT/relative).is_file() else ""
    if 'sandbox' not in (ROOT/relative.replace('script.js','index.html')).read_text(encoding="utf-8"):
        errors.append(f"{relative}: preview sandbox missing")
    if 'default-src' not in code or 'form-action' not in code:errors.append(f"{relative}: preview CSP missing")
checks.append("Bilingual routes, top switches, beginner guidance, and preview boundaries")

spec=importlib.util.spec_from_file_location("materials",ROOT/"scripts"/"build_materials.py")
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
for name,rows in (("phone",m.PHONE),("computer",m.COMPUTER)):
    end=0
    for span,duration,*_ in rows:
        start,new_end=map(int,span.split("-"))
        if start!=end or new_end-start!=int(duration):errors.append(f"{name}: invalid schedule {span}")
        end=new_end
    if end!=60 or sum(int(r[1])for r in rows)!=60:errors.append(f"{name}: not 60 minutes")
checks.append("Both schedules: continuous, 60 minutes each")
connector_rows=[r for r in m.PHONE if "Gmail" in r[2] and "Drive" in r[2]]
if len(connector_rows)!=1 or connector_rows[0][0]!="38-48" or connector_rows[0][1]!="10":
    errors.append("phone: preserve Gmail and Drive demonstrations, five minutes each at 38-48")
checks.append("Connector teaching: Gmail and Drive keep their combined 10-minute slot")

assert date(2026,11,8).weekday()==6
assert date(2026,11,5).weekday()==3
assert date(2026,11,7).weekday()==5
assert date(2026,11,4).weekday()==2
assert date(2026,11,6).weekday()==4
checks.append("Scenario date and weekday consistency")

rows=list(csv.DictReader((ROOT/"downloads"/"travel-budget.csv").open(encoding="utf-8",newline="")))
a,b=rows
total=Decimal(a["amount"])*Decimal(a["people"])+Decimal(a["transport_group_total"])
if total!=4400 or Decimal(b["amount"])!=4000 or a["lunch_status"]!="unknown" or b["lunch_status"]!="included":errors.append("budget: incorrect amount or missing-cost handling")
checks.append("Budget: A known cost 4400 TWD, B 4000 TWD, lunch uncertainty preserved")
english_budget=ROOT/"en"/"downloads"/"travel-budget.csv"
if english_budget.is_file():
    english_rows=list(csv.DictReader(english_budget.open(encoding="utf-8",newline="")))
    for original,translated in zip(rows,english_rows):
        for key in ("amount","people","transport_group_total","lunch_status"):
            if original.get(key)!=translated.get(key):errors.append(f"English budget changed {key}")
    if len(english_rows)!=len(rows):errors.append("English budget row count differs")
else:errors.append("English budget download missing")

if (ROOT/"instructor.html").read_text(encoding="utf-8")!=m.render_html(m.PAGES):
    errors.append("Instructor HTML differs from its generator")
checks.append("Instructor web output matches generator; bilingual budget values agree")

for file,expected in (("instructor-guide.pdf",8),("student-cards.pdf",2)):
    from pypdf import PdfReader
    reader=PdfReader(ROOT/"downloads"/file)
    if len(reader.pages)!=expected:errors.append(f"{file}: expected {expected} pages")
    if any(len(p.extract_text()or"")<100 for p in reader.pages):errors.append(f"{file}: empty or missing text")
checks.append("PDFs: 8 instructor pages and 2 student pages, all contain text")

for file in ROOT.rglob("*.js"):
    if ".qa" in file.parts:continue
    result=subprocess.run([NODE,"--check",str(file)],capture_output=True,text=True)
    if result.returncode:errors.append(result.stderr)
tmp=ROOT/".qa";tmp.mkdir(exist_ok=True)
inline_count=0
for file,doc in docs.items():
    for i,script in enumerate(doc.scripts):
        target=tmp/f"inline-{file.stem}-{i}.js";target.write_text(script,encoding="utf-8")
        result=subprocess.run([NODE,"--check",str(target)],capture_output=True,text=True)
        if result.returncode:errors.append(result.stderr)
        inline_count+=1
checks.append(f"JavaScript syntax including {inline_count} inline script")

# This repo must stay public-safe: only derived summaries and fictional material.
patterns=[
    (r"192\.168\.\d+\.\d+","private LAN address"),
    (r"100\.(?:6[4-9]|[7-9]\d|1[01]\d|12[0-7])\.\d+\.\d+","private overlay address"),
    (r"[a-z0-9.-]+\.ts\.net","private overlay hostname"),
    (r"/home/[a-z_][a-z0-9_-]*/","private home path"),
    (r"app\.notion\.com/p/","private Notion source URL"),
    (r"sk-[A-Za-z0-9_-]{20,}","possible API key"),
    (r"gh[pousr]_[A-Za-z0-9]{20,}","possible GitHub token"),
    (r"-----BEGIN [A-Z ]*PRIVATE KEY-----","private key"),
]
for file in ROOT.rglob("*"):
    if not file.is_file() or any(x in file.parts for x in (".git",".qa","__pycache__")) or file.name=="validate.py" or file.suffix.lower() in (".pdf",".png",".jpg"):continue
    content=file.read_text(encoding="utf-8",errors="replace")
    for pattern,label in patterns:
        if re.search(pattern,content):errors.append(f"{file.relative_to(ROOT)}: {label}")
checks.append("Focused public-content scan: no private topology, Notion URLs, or high-signal secrets")
for msg in checks:print("PASS "+msg)
if errors:
    for msg in errors:print("FAIL "+msg)
    sys.exit(1)
print("PASS all focused checks")
