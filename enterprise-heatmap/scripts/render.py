"""完整性和位置检查后生成地图；只用Python标准库。"""
import argparse, json, math
from pathlib import Path
from coordinates import gcj02_to_wgs84

def rings(geom):
    if geom['type']=='Polygon': return [geom['coordinates']]
    if geom['type']=='MultiPolygon': return geom['coordinates']
    raise ValueError('边界必须为Polygon或MultiPolygon')

def inside_ring(p, ring):
    x,y=p; result=False
    for a,b in zip(ring,ring[1:]+ring[:1]):
        if (a[1]>y)!=(b[1]>y) and x<(b[0]-a[0])*(y-a[1])/(b[1]-a[1])+a[0]: result=not result
    return result

def inside(p, gj):
    return any(inside_ring(p,poly[0]) and not any(inside_ring(p,h) for h in poly[1:]) for f in gj['features'] for poly in rings(f['geometry']))

def boundary_distance(p,gj):
    # 到边界线段的局部平面距离，用于保留边界附近疑点。
    sx=111320*math.cos(math.radians(p[1])); sy=111320; best=float('inf')
    for f in gj['features']:
        for poly in rings(f['geometry']):
            for ring in poly:
                for a,b in zip(ring,ring[1:]+ring[:1]):
                    ax=(a[0]-p[0])*sx; ay=(a[1]-p[1])*sy
                    bx=(b[0]-p[0])*sx; by=(b[1]-p[1])*sy
                    dx=bx-ax;dy=by-ay; den=dx*dx+dy*dy
                    t=max(0,min(1,-(ax*dx+ay*dy)/den)) if den else 0
                    best=min(best,math.hypot(ax+t*dx,ay+t*dy))
    return best

def prepare(doc,gj,verified=False,preview=False,tolerance=100):
    rows=doc['enterprises']; expected=doc['meta']['expected_total']
    ids=[r.get('credit_code') for r in rows]
    if len(rows)!=expected or not all(ids) or len(set(ids))!=expected: raise ValueError('取数不完整或存在缺失/重复信用代码，停止出图')
    if doc['meta'].get('coord_system')!='GCJ-02': raise ValueError('当前只接受已标明GCJ-02的高德坐标')
    if not verified and not preview: raise ValueError('边界未核验，不能生成正式地图')
    features=[]; missing=[]; rejected=[]; suspected=[]
    for row in rows:
        r=dict(row);x=r.get('lng');y=r.get('lat')
        if not isinstance(x,(int,float)) or not isinstance(y,(int,float)) or not math.isfinite(x) or not math.isfinite(y) or not(-180<=x<=180 and -90<=y<=90):
            missing.append(dict(name=r['name'],reason='缺失或无效坐标'));continue
        p=gcj02_to_wgs84(x,y)
        if not inside(p,gj):
            d=boundary_distance(p,gj)
            issue=dict(name=r['name'],reason='边界外',distance_m=round(d),credit_code=r['credit_code'])
            if verified and d>tolerance: rejected.append(issue);continue
            suspected.append(issue)
        features.append({'type':'Feature','geometry':{'type':'Point','coordinates':p},'properties':{'name':r['name'],'address':r.get('address',''),'credit_code':r['credit_code']}})
    if len(rejected)>5 or len(rejected)>expected*.01: raise ValueError('明显位置错误超过5家或1%，停止出图，需核对数据/边界')
    audit=dict(total=expected,mapped=len(features),missing=missing,rejected=rejected,suspected=suspected,boundary_verified=verified,preview=preview,tolerance_m=tolerance,query=doc['meta'])
    return {'type':'FeatureCollection','features':features},audit

def main():
    p=argparse.ArgumentParser();p.add_argument('--data',required=True);p.add_argument('--boundary',required=True);p.add_argument('--boundary-crs',required=True,choices=['WGS84']);p.add_argument('--boundary-verified',action='store_true');p.add_argument('--preview',action='store_true');p.add_argument('--out',required=True);p.add_argument('--force',action='store_true');a=p.parse_args()
    out=Path(a.out);auditpath=out.with_suffix('.audit.json')
    if not a.force and (out.exists() or auditpath.exists()): raise ValueError('输出已存在；明确覆盖才使用--force')
    doc=json.loads(Path(a.data).read_text(encoding='utf-8'));boundary=json.loads(Path(a.boundary).read_text(encoding='utf-8'))
    points,audit=prepare(doc,boundary,a.boundary_verified,a.preview)
    data={'points':points,'boundary':boundary,'title':doc['meta']['title'],'preview':a.preview}
    template=(Path(__file__).parent.parent/'assets/map.html').read_text(encoding='utf-8')
    # 转义闭合script，企业名称和地址均通过textContent展示。
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(template.replace('__PAYLOAD__',json.dumps(data,ensure_ascii=False).replace('</','<\\/')), encoding='utf-8')
    auditpath.write_text(json.dumps(audit,ensure_ascii=False,indent=2), encoding='utf-8')
    print(json.dumps({'total':audit['total'],'mapped':audit['mapped'],'missing':len(audit['missing']),'rejected':len(audit['rejected']),'suspected':len(audit['suspected']),'preview':a.preview},ensure_ascii=False))

if __name__=='__main__': main()
