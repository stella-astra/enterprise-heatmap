#!/usr/bin/env python3
"""检查发布范围与常见凭证；只输出文件名和规则名，不输出匹配内容。"""
import re,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
ALLOWED={'README.md','LICENSE','THIRD_PARTY.md','RELEASE_NOTES.md','.gitignore',
 'docs/INSTALL.md','docs/TECHIN.md','docs/COMPATIBILITY.md','docs/GITHUB.md','docs/PRIVACY.md','docs/VALIDATION.md',
 'tools/check_release.py','.github/workflows/check.yml',
 'enterprise-heatmap/SKILL.md','enterprise-heatmap/references/data-format.md',
 'enterprise-heatmap/scripts/fetch_boundary.py','enterprise-heatmap/references/boundaries.md',
 'enterprise-heatmap/scripts/coordinates.py','enterprise-heatmap/scripts/render.py','enterprise-heatmap/scripts/render_report.py',
 'enterprise-heatmap/assets/map.html','enterprise-heatmap/assets/report.html'}
RULES={
 'personal_absolute_path':r'/(?:Users|home)/[A-Za-z0-9_.-]+/',
 'windows_personal_path':r'[A-Za-z]:\\Users\\[^\\\s]+\\',
 'email':r'[A-Za-z0-9_.+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}',
 'key_pattern':r'\b(?:sk|ghp|github_pat)[_-][A-Za-z0-9_-]{16,}',
 'bearer_value':r'(?i)Bearer\s+[A-Za-z0-9._-]{16,}',
 'credential_assignment':r'(?i)(?:api[_-]?key|password|secret|token)\s*[:=]\s*[\"\x27][A-Za-z0-9_-]{16,}',
 'credit_code':r'\b91[0-9A-Z]{16}\b'}
def main():
 errors=[];count=0
 for p in ROOT.rglob('*'):
  rel=p.relative_to(ROOT).as_posix()
  if '.git' in p.parts or '__pycache__' in p.parts or p.name == '.DS_Store':continue
  if p.is_symlink():errors.append((rel,'symlink'));continue
  if not p.is_file():continue
  count+=1
  if rel not in ALLOWED:errors.append((rel,'not_allowlisted'));continue
  text=p.read_text(encoding='utf-8')
  for name,pattern in RULES.items():
   if re.search(pattern,text):errors.append((rel,name))
  if p.suffix=='.py':compile(text,str(p),'exec')
  if p.suffix=='.html' and '__PAYLOAD__' not in text:errors.append((rel,'non_template_html'))
 skill=(ROOT/'enterprise-heatmap/SKILL.md').read_text(encoding='utf-8')
 head=skill.split('---',2)[1];name=re.search(r'^name: (.+)$',head,re.M);desc=re.search(r'^description: (.+)$',head,re.M)
 if not name or not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',name.group(1)) or name.group(1)!='enterprise-heatmap':errors.append(('SKILL.md','name'))
 if not desc or not 1<=len(desc.group(1))<=1024:errors.append(('SKILL.md','description'))
 for f in ALLOWED:
  if not (ROOT/f).is_file():errors.append((f,'missing'))
 if errors:
  for f,rule in errors:print('FAIL',f,rule)
  return 1
 print('PASS:',count,'files; syntax, skill metadata, file allowlist and privacy patterns')
 return 0
if __name__=='__main__':sys.exit(main())
