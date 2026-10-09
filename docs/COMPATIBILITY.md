# 兼容性核对（2026-10-09）

“模型”是思考能力，“Agent客户端”负责读技能、调用MCP与执行脚本。兼容性主要取决于客户端能力，不取决于是否使用GPT。

| 客户端 | 安装方式 | 核对程度 |
|---|---|---|
| CodeBuddy Code | `.codebuddy/skills/enterprise-heatmap` | 官方文档确认SKILL.md；未实机跑本技能 |
| WorkBuddy | 当前版本技能导入入口 | 官方文档有技能功能；导入ZIP和Techin连接待使用者实机确认 |
| OpenCode | `.opencode/skills/enterprise-heatmap` | 官方确认Skills和远程MCP；未实机跑本技能 |
| Claude Code | `.claude/skills/enterprise-heatmap` | 官方确认技能目录；未实机跑本技能 |
| 当前开发Agent | 本地脚本＋Techin MCP＋浏览器 | 已完成真实深圳街道／区级取数、交互与图片测试 |
| 其他支持Agent Skills的客户端 | 其官方技能目录 | 标准格式兼容，MCP／本地执行权限需确认 |
| 普通模型聊天网页 | 无执行环境 | 不能直接运行本技能 |

OpenCode的模型服务文档提供DeepSeek、Moonshot AI、MiniMax、Z.AI等选项，所以有不用GPT的可行路径；这不等于已经测试所有国产模型。所选模型须能稳定使用工具、完整翻页和执行文件任务。MCP数据权限、模型账号和费用各自独立。

核对依据（官方）：

- [Agent Skills规范](https://agentskills.io/specification)
- [CodeBuddy Skills](https://www.codebuddy.ai/docs/cli/skills)
- [WorkBuddy技能](https://www.codebuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Skills-Market)
- [OpenCode Skills](https://opencode.ai/docs/skills/)
- [OpenCode MCP](https://opencode.ai/docs/mcp-servers/)
- [OpenCode模型服务](https://opencode.ai/docs/providers/)
- [Claude Code Skills](https://code.claude.com/docs/en/skills)

首次在新客户端验收：识别技能→读取Techin字段→产业匹配→完整取数→出HTML→导出PNG。任何步骤失败，都不能把“文档支持”改称“已经验证能用”。
