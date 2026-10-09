# 安装与使用

## 选择一个Agent

- CodeBuddy Code：把 `enterprise-heatmap` 放到项目的 `.codebuddy/skills/` 或个人的 `~/.codebuddy/skills/`。用 `/skills` 查看加载结果。
- OpenCode：放到项目的 `.opencode/skills/` 或个人的 `~/.config/opencode/skills/`。
- Claude Code：放到项目的 `.claude/skills/` 或个人的 `~/.claude/skills/`。
- WorkBuddy：先在“技能”界面查看当前版本支持的导入方式，导入文件夹／ZIP；此客户端未实机验收，不使用未经官方证实的专属路径。
- 其他宿主：使用其官方SKILL.md导入入口；没有Skills功能但能读文件的Agent，可明确要求阅读SKILL.md执行，这属于手动流程，不保证自动触发。

安装后检查目录：`技能目录/enterprise-heatmap/SKILL.md`。保留scripts、assets、references；不要只复制SKILL.md。

## 配置自己的Techin

按TECHIN.md在宿主连接设置填写自己的Key与官方服务地址。先让Agent检查 `list_datasets` 是否可用，确认能读取“企业全景画像”。连接失败就停止，不应使用安装包中的演示数据代替真实查询。

## 执行

1. 对Agent说区域、产业、需要网页和图片。
2. Agent核对产业分类；非商业学习研究会自动获取行政边界。首次用途未知时先确认用途；网站限制时按网站正常流程取得文件。无需地图Key，详见Skill内references/boundaries.md。
3. Agent完整查询企业、统计资质、核对异常，再在你指定的输出目录生成HTML及数据审计文件。
4. 双击HTML打开浏览器。PNG导出页等待地图加载完成后点击导出。如果宿主浏览器不支持下载，可右键保存生成后的完整图片。

Python脚本仅需标准库。Windows可用 `py -3`，macOS/Linux可用 `python3`，版本须≥3.9。读取UTF-8中文文件，不依赖开发者目录或操作系统用户名。命令中的脚本路径要从安装的Skill根目录定位，数据路径使用你自己的位置。

离线机器不能加载在线底图。网络失败时换可访问网络后重试，不把空白地图当成功结果。无需注册高德地图Key。
