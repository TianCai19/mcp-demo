#!/bin/bash
# 从主项目同步文档到 docs-site

echo "开始同步文档..."

# 复制文档
cp ../README.md src/content/docs/index.md
cp ../weather/CODE_EXPLAINED.md src/content/docs/code-explained.md
cp ../weather/TRANSPORT_EXPLAINED.md src/content/docs/transport-explained.md
cp ../MCP_CONFIG_EXPLAINED.md src/content/docs/config-explained.md
cp ../MCP_CLIENTS_SETUP.md src/content/docs/clients-setup.md

echo "文档同步完成！"
echo "运行 'npm run dev' 查看效果"
