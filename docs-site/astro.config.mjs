// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

// https://astro.build/config
export default defineConfig({
	integrations: [
		starlight({
			title: 'MCP Demo - Weather Server & Client',
			description: 'Model Context Protocol 完整示例项目文档',
			// GitHub 链接
			social: [
				{
					icon: 'github',
					label: 'GitHub',
					href: 'https://github.com/TianCai19/mcp-demo',
				},
			],
			// 编辑链接
			editLink: {
				baseUrl: 'https://github.com/TianCai19/mcp-demo/edit/main/docs-site/src/content/docs/',
			},
			// 侧边栏导航配置
			sidebar: [
				{
					label: '项目文档',
					items: [
						{ label: '项目介绍', link: '/index' },
					],
				},
				{
					label: '代码学习',
					items: [
						{ label: '代码逐行解析', link: '/code-explained' },
						{ label: 'Transport 详解', link: '/transport-explained' },
					],
				},
				{
					label: '配置指南',
					items: [
						{ label: '配置格式详解', link: '/config-explained' },
						{ label: '各客户端配置', link: '/clients-setup' },
					],
				},
			],
			// 多语言配置
			locales: {
				root: {
					label: '简体中文',
					lang: 'zh-CN',
				},
			},
		}),
	],
	// 静态站点输出（适合 Vercel）
	output: 'static',
});
