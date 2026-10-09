# 每位用户配置自己的Techin

本Skill的渲染脚本不读取Key、不发Techin请求。Agent通过当前用户配置的MCP连接查询数据，再将数据交给脚本。这意味着复制Skill不会复制开发者的查询身份。

## 首次配置

1. 登录你自己的Techin账号，按官方流程取得个人API Key和MCP服务地址。
2. 打开所用Agent的MCP／连接设置，新建Techin连接。服务地址和传输类型以Techin官方说明为准；本仓库不猜测或内置开发者私有地址。
3. 请求头名填写 `X-Techin-Api-Key`，值只在平台本地连接设置中填写你自己的Key。支持密钥管理或环境变量引用的平台优先使用该功能；不支持的情况下使用个人配置目录，不要放到共享项目配置里。
4. 让Agent调用 `list_datasets` 和 `get_dataset_fields` 验证权限。无权限／认证失败只提示配置问题，不打印完整请求头或配置文件。

这里的Techin Key与模型Key不同：前者访问企业数据，后者访问DeepSeek/GLM等模型服务。

## 能力检查

至少要能使用list_datasets、get_dataset_fields、match_industry、query_stat、query_detail；查标签还需要get_field_enums。各宿主的工具前缀可能不同，Agent通过MCP工具列表发现，不写死Codex前缀。企业数据权限必须属于当前用户。

## 不要这样做

不要把Key发给AI聊天、写在HTML或JSON、提交到GitHub、复用其他人的连接。不要上传个人 `.mcp.json`、宿主config/auth文件或 `.env`。连接配置只在自己的机器配置一次，不需要每次生成地图重新输入。

更换用户时由新用户配置自己的连接，不能因为复制旧工作区就默认复用原用户身份。已泄露的Key应在Techin后台撤销并重建；不要只删除截图或聊天消息。
