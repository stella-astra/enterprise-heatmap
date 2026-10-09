# 数据与执行规范

数据由当前用户的Techin MCP完整查询取得；下面只描述结构，没有模拟企业或真实开发者数据。

企业JSON包含 `meta` 与 `enterprises`：

- meta：title（中文标题）、expected_total（服务统计整数）、coord_system固定GCJ-02、region（省/市/区[/街道]）、industry、status、fetched_at（YYYY-MM-DD）、filters、adjustments、pages（每页数量）。
- enterprises：数组，每项name、credit_code、address、lng、lat；坐标字段必须是数值或null，不能保留字符串数值。
- 代表企业可另保留raw_tags、listed、score。标签来自有效科技认定和是否上市公司字段。

summary.json包含total、hightech、specialized、little_giant、listed_total整数及region、industry、status、fetched_at。地区和产业必须与企业JSON完全一致；资质数需在0到总数间。representatives数组含name、credit_code、tags（短标签数组）、raw_tags，最多12项。筛选规则和评分保留在selection及代表企业字段中，禁止凭名称推断上市或独角兽。字段不可用时说明问题，不用0代替未知数量。

边界GeoJSON必须是FeatureCollection，geometry仅接受Polygon或MultiPolygon；坐标为经核对的WGS84，经纬顺序。每个环闭合，支持孔洞。获取边界要核对来源、日期、坐标系、使用许可，并将依据保存到使用者输出目录的边界元数据。标志--boundary-verified代表已有证据，不能靠文件扩展名或SRID声明直接勾选。

从Skill根目录运行（根据宿主使用python3或py -3）：

```
python3 scripts/render.py --data 数据.json --boundary 边界.geojson --boundary-crs WGS84 --boundary-verified --out 输出目录/地图.html
python3 scripts/render_report.py --data 数据.json --boundary 边界.geojson --boundary-crs WGS84 --boundary-verified --summary summary.json --out 输出目录/信息图.html
```

输出已存在时，只有明确需要覆盖才加--force。--preview用于本地诊断，审计中记录preview=true；它不会把未知边界变为可靠边界。异常太多则正式模式停止，不把预览结果当正式验收。

经确认的明显位置错误仅允许≤5家且≤完整总数1%；边界附近100米内保留核对，不能只因企业分散而删除。信息卡数量基于完整行政字段查询；地图仅展示边界内位置，审计保留差异。
