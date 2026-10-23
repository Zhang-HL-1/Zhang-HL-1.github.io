# 小鳥遊的博客

[打开博客 →](https://zhang-hl-1.github.io/)

独立设计的静态博客：HTML、CSS、JavaScript + 一个小型 Python Markdown 生成器。无 Gmeek 依赖，不再通过 Issues 生成文章。

## 发布文章

在 `content/posts/` 新建英文小写文件名，例如 `my-first-note.md`：

```markdown
---
title: 我的第一篇笔记
date: 2026-10-23
category: 技术笔记
description: 这篇文章的一句话介绍。
draft: false
---

## 从这里开始

正文使用 Markdown，支持代码块、图片、表格和目录 `[TOC]`。
```

提交到 `main` 后 GitHub Actions 自动构建并发布。分类从文章中读取；草稿设置 `draft: true`，不会发布。日期使用 `YYYY-MM-DD`。图片放在 `site/images/`，文章中使用 `/images/文件名`。

## 本地运行

```sh
python3 -m pip install -r requirements.txt
python3 scripts/build.py
python3 -m http.server 8000 --directory docs
```

打开 `http://localhost:8000`。页面源文件在 `site/`，生成结果在 `docs/`。请修改源文件后重新构建。

## 功能

- 响应式布局、深浅色切换和主题记忆
- 文章全文搜索、分类筛选、按年归档
- 独立文章地址、Markdown 排版
- RSS、站点地图、404 页面
- 日本修考笔记与 TOEFL Study 入口

## 旧版备份

旧 Gmeek 版本保存在 `backup/gmeek-2026-10-23` 分支，起点为 `d2f328a54584ba67ee147b79c3507aa00ae7721b`。如需回滚，可从该分支恢复文件后提交到 main。旧 Issues 保留为历史资料，但不再用于发布。
