#!/usr/bin/env python3
"""生成16:9图片导出页；数据和标签必须由Techin真实查询提供。"""
import argparse,json
from pathlib import Path
from render import prepare

def main():
 p=argparse.ArgumentParser()
 for k in ('data','boundary','summary','out'):p.add_argument('--'+k,required=True)
 p.add_argument('--preview',action='store_true');p.add_argument('--boundary-verified',action='store_true');p.add_argument('--boundary-crs',required=True,choices=['WGS84']);p.add_argument('--force',action='store_true');a=p.parse_args()
 out=Path(a.out)
 if out.exists() and not a.force:raise ValueError('输出已存在，覆盖需--force')
 doc=json.loads(Path(a.data).read_text(encoding='utf-8'));boundary=json.loads(Path(a.boundary).read_text(encoding='utf-8'));summary=json.loads(Path(a.summary).read_text(encoding='utf-8'))
 points,audit=prepare(doc,boundary,a.boundary_verified,a.preview)
 if summary['total']!=doc['meta']['expected_total']:raise ValueError('标签统计与完整企业数据总数不一致')
 if summary['region']!=doc['meta']['region'] or summary['industry']!=doc['meta']['industry'] or summary['status']!=doc['meta']['status']:raise ValueError('统计查询范围不一致')
 for k in ('hightech','specialized','little_giant','listed_total'):
  if not isinstance(summary[k],int) or not 0<=summary[k]<=summary['total']:raise ValueError('缺少有效标签统计')
 ids={r['credit_code']:r['name'] for r in doc['enterprises']}
 for r in summary['representatives']:
  if ids.get(r['credit_code'])!=r['name'] or not r['tags']:raise ValueError('展示企业不属于完整结果或缺少标签证据')
 payload=dict(points=points,boundary=boundary,meta=doc['meta'],summary=summary)
 template=(Path(__file__).parent.parent/'assets/report.html').read_text(encoding='utf-8')
 out.parent.mkdir(parents=True,exist_ok=True);out.write_text(template.replace('__PAYLOAD__',json.dumps(payload,ensure_ascii=False).replace('</','<\\/')), encoding='utf-8')
 audit['summary']=summary;out.with_suffix('.audit.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2), encoding='utf-8')
 print('已生成1920×1080图片导出页；打开后点击导出PNG')
if __name__=='__main__':main()
