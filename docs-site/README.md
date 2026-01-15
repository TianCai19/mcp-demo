# MCP Demo 文档站点

这是 MCP Demo 项目的文档站点，使用 [Astro](https://astro.build) + [Starlight](https://starlight.astro.build) 构建。

## 本地开发

```bash
# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

访问 http://localhost:4321

## 构建

```bash
npm run build
```

## 部署到 Vercel

### 方法 1：通过 Vercel CLI

```bash
# 安装 Vercel CLI
npm i -g vercel

# 部署
vercel
```

### 方法 2：通过 GitHub 集成

1. 将代码推送到 GitHub
2. 在 [Vercel](https://vercel.com) 导入项目
3. 选择 `docs-site` 目录作为根目录
4. 自动部署

### 方法 3：手动配置

在 Vercel 项目设置中：

- **Root Directory**: `docs-site`
- **Build Command**: `npm run build`
- **Output Directory**: `dist`

## 项目结构

```
docs-site/
├── src/
│   └── content/
│       └── docs/           # Markdown 文档
│           ├── index.md
│           ├── code-explained.md
│           ├── transport-explained.md
│           ├── config-explained.md
│           └── clients-setup.md
├── public/                  # 静态资源
├── astro.config.mjs        # Astro 配置
├── vercel.json             # Vercel 配置
└── package.json
```

## 文档来源

文档直接从主项目复制而来，保持内容一致性：

- `index.md` ← `../README.md`
- `code-explained.md` ← `../weather/CODE_EXPLAINED.md`
- `transport-explained.md` ← `../weather/TRANSPORT_EXPLAINED.md`
- `config-explained.md` ← `../MCP_CONFIG_EXPLAINED.md`
- `clients-setup.md` ← `../MCP_CLIENTS_SETUP.md`

## 更新文档

当主项目文档更新时，运行：

```bash
# 从主项目复制最新的文档
cp ../README.md src/content/docs/index.md
cp ../weather/CODE_EXPLAINED.md src/content/docs/code-explained.md
cp ../weather/TRANSPORT_EXPLAINED.md src/content/docs/transport-explained.md
cp ../MCP_CONFIG_EXPLAINED.md src/content/docs/config-explained.md
cp ../MCP_CLIENTS_SETUP.md src/content/docs/clients-setup.md
```

或者使用同步脚本：

```bash
./sync-docs.sh
```

## 技术栈

- [Astro](https://astro.build) - 现代化的静态站点生成器
- [Starlight](https://starlight.astro.build) - Astro 的文档主题
- [Vercel](https://vercel.com) - 部署平台
