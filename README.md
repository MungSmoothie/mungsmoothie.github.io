# Sen 的生活笔记

中文个人静态博客，首批收录饮食与健身两份笔记。页面使用本地插画，电脑和手机均可阅读。

## 页面

- `index.html`：博客首页。
- `workout-plan.html`：健身房训练、器械图解、体态活动与每周两次的腹部安排。
- `diet-plan.html`：食谱、备餐和饮食复盘。
- `assets/*.png`：文章所需的 38 张插画（24 个主训练条目均有配图）。

## GitHub Pages

站点已发布：[Sen 的生活笔记](https://mungsmoothie.github.io/)。源文件保存在 [MungSmoothie/mungsmoothie.github.io](https://github.com/MungSmoothie/mungsmoothie.github.io)。

仓库的 Settings → Pages 已设置为 **Deploy from a branch**，发布 `main` 分支的 **/(root)**。仓库根目录中的 `.nojekyll` 让 GitHub 直接发布这些 HTML 和配图。

发布时只提交网站文件与本说明。备份、预览截图、生成提示词、工具和未整理的旧页面均已在 `.gitignore` 中排除。

## 更新笔记

1. 修改已有 HTML，或创建一篇新的 HTML，配图放入 `assets/`。
2. 在 `index.html` 的 `posts` 容器中添加文章链接、标题、日期和摘要。复制已有文章条目即可。
3. 使用相对链接，例如 `assets/photo.png`，保留返回 `index.html` 的入口。
4. 提交并推送到 `main`，GitHub Pages 会发布更新。

本地可运行 `python3 -m http.server 8765 --bind 127.0.0.1`，打开 `http://127.0.0.1:8765/` 预览。`python3 check_site.py` 检查站点入口、链接、配图和发布文件。

GitHub Pages 发布的是公开网页，适合文章和图片；请在上传前确认内容适合公开。

参考：[GitHub Pages 快速入门](https://docs.github.com/en/pages/quickstart)、[配置发布来源](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)。
