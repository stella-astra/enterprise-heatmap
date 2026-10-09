# 发到GitHub

推荐仓库名：enterprise-heatmap-skill

仓库简介：基于个人Techin MCP的企业分布热力图Skill，生成交互地图与16:9汇报图片；支持标准Agent Skills。

建议标签：agent-skills、mcp、techin、heatmap、industry-research、maplibre、python。

1. 解压“GitHub发布包”，进入enterprise-heatmap文件夹。
2. 在GitHub新建仓库，上传这个文件夹里面的内容：README.md、LICENSE、docs、tools、enterprise-heatmap、.github等。
3. 不要上传原始开发工作区或“测试结果包”；其中有查询数据与限制使用的候选边界。
4. 首次版本建议v0.1.1，发行说明直接使用RELEASE_NOTES.md。
5. 安装用户只复制内层enterprise-heatmap技能文件夹。

在终端使用Git时，先进入解压后的干净发布目录，再初始化仓库。发布前运行 `python3 tools/check_release.py`，确认通过。不要在原开发工作区直接git add .。

本次只准备材料，没有替你创建仓库或推送。GitHub Actions会再次验证公开包结构与常见凭证模式；它不能扫描用户机器外的连接或撤销已泄露Key。
