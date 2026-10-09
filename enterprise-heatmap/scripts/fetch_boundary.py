#!/usr/bin/env python3
"""按公开接口获取个人学习研究边界；不含凭证，不绕过访问限制。"""
import argparse
import hashlib
import json
import math
import re
import shutil
import ssl
import struct
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import urlopen
from urllib.error import URLError

BASE = 'https://map.ruiduobao.com'
MAX_BYTES = 20 * 1024 * 1024

def request(path, params=None):
    url = BASE + path + ('?' + urlencode(params) if params else '')
    try:
        with urlopen(url, timeout=40) as response:
            raw = response.read(MAX_BYTES + 1)
    except URLError as exc:
        # 部分桌面Python缺系统证书；curl仍验证TLS，绝不使用-k。
        if not isinstance(exc.reason, ssl.SSLCertVerificationError) or not shutil.which('curl'):
            raise RuntimeError('边界服务访问失败，请检查网络或网站访问限制。') from exc
        result = subprocess.run(['curl', '--fail', '--silent', '--show-error',
                                 '--max-time', '40', url], capture_output=True)
        if result.returncode:
            raise RuntimeError('边界服务访问失败；停止，不绕过密码、验证码或限流。')
        raw = result.stdout
    if len(raw) > MAX_BYTES:
        raise ValueError('边界响应过大，停止获取。')
    try:
        data = json.loads(raw.decode('utf-8'))
    except (UnicodeError, ValueError):
        raise ValueError('网站未返回JSON；请检查网站限制，不绕过验证。')
    if isinstance(data, dict) and 'status' in data and data['status'] != 'success':
        raise ValueError('网站拒绝请求；请按网站要求处理，不自动重试或绕过限制。')
    return data

def select(level, params, name):
    rows = request('/api/tree/' + level, params).get('data', [])
    matches = [r for r in rows if r.get('name') == name]
    if len(matches) != 1:
        raise ValueError('行政名称未唯一匹配：' + name + '。请核对完整名称和行政层级。')
    return str(matches[0]['code'])

def validate(data, code):
    if data.get('type') != 'FeatureCollection' or not data.get('features'):
        raise ValueError('边界不是有效FeatureCollection。')
    for feature in data['features']:
        props = feature.get('properties') or {}
        if str(props.get('code')) != code:
            raise ValueError('边界行政编码与请求不一致。')
        # 检查原始EWKB声明，而不是凭经纬度范围猜坐标系。
        try:
            ewkb = bytes.fromhex(props['geom'])
            endian = '<' if ewkb[0] == 1 else '>' if ewkb[0] == 0 else None
            if endian is None or not struct.unpack(endian + 'I', ewkb[1:5])[0] & 0x20000000:
                raise ValueError()
            if struct.unpack(endian + 'I', ewkb[5:9])[0] != 4326:
                raise ValueError()
        except (KeyError, ValueError, TypeError, struct.error, IndexError):
            raise ValueError('边界缺少可读取的SRID4326声明；不能猜坐标系。')
        geo = feature.get('geometry') or {}
        kind = geo.get('type')
        polys = [geo.get('coordinates')] if kind == 'Polygon' else geo.get('coordinates') if kind == 'MultiPolygon' else None
        if not polys:
            raise ValueError('边界必须为Polygon或MultiPolygon。')
        for polygon in polys:
            if not polygon:
                raise ValueError('空多边形。')
            for ring in polygon:
                if len(ring) < 4 or ring[0] != ring[-1]:
                    raise ValueError('边界环未闭合。')
                for point in ring:
                    if len(point) < 2 or any(isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v) for v in point[:2]) or not (-180 <= point[0] <= 180 and -90 <= point[1] <= 90):
                        raise ValueError('边界经纬度无效。')

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--province', required=True)
    parser.add_argument('--city', required=True)
    parser.add_argument('--district')
    parser.add_argument('--town')
    parser.add_argument('--year', choices=['2023'], default='2023')
    parser.add_argument('--noncommercial', action='store_true', help='使用者已明确仅作非商业学习研究')
    parser.add_argument('--out', required=True)
    args = parser.parse_args()
    if not args.noncommercial:
        raise ValueError('此来源仅用于非商业学习研究；请先确认用途或提供其他获授权边界。')
    if args.town and not args.district:
        raise ValueError('街道必须同时指定所属区。')
    out = Path(args.out).resolve()
    # 防止将第三方边界存入发布仓库或技能安装目录。
    if Path(__file__).resolve().parents[1] in out.parents or any((p / '.git').exists() for p in out.parents):
        raise ValueError('请将边界保存到个人输出目录，不要保存进技能或Git仓库。')
    sidecar = out.with_suffix('.metadata.json')
    region = {k: getattr(args, k) for k in ('province', 'city', 'district', 'town', 'year')}
    if out.exists() and sidecar.exists():
        metadata = json.loads(sidecar.read_text(encoding='utf-8'))
        raw = out.read_bytes()
        if metadata.get('region') == region and metadata.get('sha256') == hashlib.sha256(raw).hexdigest() and metadata.get('source') == BASE and metadata.get('usage') == 'noncommercial-learning-research':
            validate(json.loads(raw.decode('utf-8')), metadata['code'])
            print('已复用本地边界，无需再次下载。')
            return
    params = {'year': args.year, 'province': args.province}
    code = select('cities', params, args.city)
    params['city'] = args.city
    if args.district:
        code = select('counties', params, args.district)
        params['county'] = args.district
    if args.town:
        code = select('towns', params, args.town)
    export = request('/getGsonDB', {'code': code})
    path = export.get('filepath', '')
    if not re.fullmatch(r'/vectordata/' + re.escape(code) + r'\.gson', path):
        raise ValueError('下载路径不符合公开接口约定，停止。')
    data = request(path)
    validate(data, code)
    raw = json.dumps(data, ensure_ascii=False).encode('utf-8')
    metadata = {'source': BASE, 'source_documentation': 'https://github.com/ruiduobao/china-divisions-map',
                'region': region, 'code': code, 'usage': 'noncommercial-learning-research',
                'downloaded_at': datetime.now(timezone.utc).isoformat(), 'coord_system': 'WGS84',
                'crs_evidence': 'source EWKB declares SRID 4326', 'verified': False,
                'note': '已检查编码、坐标声明与结构；尚未独立核验最新行政边界精度。目录年份不是边界测绘年份。',
                'sha256': hashlib.sha256(raw).hexdigest()}
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(raw)
    sidecar.write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding='utf-8')
    print('已获取边界及来源记录；用于学习研究出图，不标为精度已核验。')

if __name__ == '__main__':
    try:
        main()
    except (ValueError, RuntimeError, OSError, TypeError, KeyError) as exc:
        print('未完成：' + str(exc), file=sys.stderr)
        sys.exit(1)
