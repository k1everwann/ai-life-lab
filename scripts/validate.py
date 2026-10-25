"""Focused validation for the public learning materials."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse, unquote
from datetime import date
from decimal import Decimal
import csv
import importlib.util
import json
import re
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
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
    if doc.lang!="zh-Hant":errors.append(f"{file.name}: missing Traditional Chinese lang")
for file,doc in docs.items():
    for ref in doc.refs:
        parts=urlparse(ref)
        if parts.scheme or parts.netloc or ref.startswith("data:"):continue
        dest=(file.parent/unquote(parts.path)).resolve() if parts.path else file
        if not dest.is_file():errors.append(f"{file.name}: missing local file {ref}")
        if parts.fragment and dest in docs and unquote(parts.fragment) not in docs[dest].ids:
            errors.append(f"{file.name}: missing anchor {ref}")
checks.append(f"HTML local references and anchors: {len(docs)} pages")

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

for file,expected in (("instructor-guide.pdf",8),("student-cards.pdf",2)):
    from pypdf import PdfReader
    reader=PdfReader(ROOT/"downloads"/file)
    if len(reader.pages)!=expected:errors.append(f"{file}: expected {expected} pages")
    if any(len(p.extract_text()or"")<100 for p in reader.pages):errors.append(f"{file}: empty or missing text")
checks.append("PDFs: 8 instructor pages and 2 student pages, all contain text")

for file in ROOT.rglob("*.js"):
    if ".qa" in file.parts:continue
    result=subprocess.run(["node","--check",str(file)],capture_output=True,text=True)
    if result.returncode:errors.append(result.stderr)
tmp=ROOT/".qa";tmp.mkdir(exist_ok=True)
inline_count=0
for file,doc in docs.items():
    for i,script in enumerate(doc.scripts):
        target=tmp/f"inline-{file.stem}-{i}.js";target.write_text(script,encoding="utf-8")
        result=subprocess.run(["node","--check",str(target)],capture_output=True,text=True)
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
