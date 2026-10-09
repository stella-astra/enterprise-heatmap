# 外部依赖与数据

- MapLibre GL JS：浏览器从unpkg加载5.6.1版本；BSD-3-Clause，见 https://github.com/maplibre/maplibre-gl-js/blob/main/LICENSE.txt 。本仓库只含调用模板，不把第三方库源码一起分发。
- OpenFreeMap：联网底图服务，见 https://openfreemap.org/ 。无需地图Key，可用性取决于网络与服务；不提供离线地图。浏览器请求会连接此服务与unpkg，不上传本地企业列表或Techin凭证。
- OpenMapTiles、OpenStreetMap：保留各自地图署名；OSM数据ODbL及署名说明见 https://www.openstreetmap.org/copyright 。代码MIT许可不覆盖地图数据。
- Techin：企业数据由使用者自己的授权连接获取，查询权限和再分发要求遵循Techin条款。本仓库不附企业数据。
- 行政边界：默认非商业学习研究按需获取map.ruiduobao.com公开接口，来源声明见https://github.com/ruiduobao/china-divisions-map 。不得商用，不绕过下载限制，不随包分发。其他用途使用者须另行取得授权。边界本身的版权与更新日期独立于代码版本。

坐标迭代转换的数值收敛只表示计算一致，不表示定位精度，不能代替原始地址及边界核对。
