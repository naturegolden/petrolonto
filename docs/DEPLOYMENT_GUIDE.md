# petrolonto 文档站点 GitHub Pages 部署完整指南

## 一、部署架构概览

```
push to main branch
        ↓
GitHub Actions 触发 deploy-docs.yml
        ↓
┌─────────────────────────────────┐
│  Build Job (ubuntu-latest)      │
│  1. Checkout code               │
│  2. Setup Python 3.11           │
│  3. Install Rye                 │
│  4. Sync dependencies           │
│  5. mkdocs build --strict       │
│  6. Upload pages artifact       │
└─────────────────────────────────┘
        ↓
┌─────────────────────────────────┐
│  Deploy Job (if main + push)    │
│  1. Deploy to GitHub Pages      │
│  2. Set environment URL         │
└─────────────────────────────────┘
        ↓
https://naturegolden.github.io/petrolonto/
```

## 二、已完成的配置

### 2.1 工作流文件
- 文件路径：`.github/workflows/deploy-docs.yml`
- 触发条件：
  - `main` 分支 push（仅当 `docs/` 或 `core/` 有变更）
  - Pull Request 到 `main`（仅构建验证，不部署）
  - 手动触发（`workflow_dispatch`）

### 2.2 MkDocs 配置更新
- `site_name`: PetrolOnto - Petroleum Ontology Knowledge Platform
- `site_url`: https://naturegolden.github.io/petrolonto/
- `repo_url`: https://github.com/naturegolden/petrolonto
- `edit_uri`: edit/main/docs/docs/

## 三、GitHub 仓库端配置（必须手动操作）

### 3.1 启用 GitHub Pages

1. 打开 GitHub 仓库页面：https://github.com/naturegolden/petrolonto
2. 点击 **Settings** 标签
3. 左侧菜单点击 **Pages**
4. 在 **Source** 下拉框选择 **GitHub Actions**（不是 "Deploy from a branch"）
5. 保存设置

### 3.2 配置 Environment 权限（如需要）

1. 在 **Settings → Pages** 页面，确认显示 "GitHub Actions" 作为部署源
2. 如果第一次部署失败，检查 **Settings → Environments → github-pages**
3. 确保没有设置 "Required reviewers"（或添加自己为 reviewer）

## 四、部署操作

### 4.1 推送代码触发首次部署

```bash
cd d:\gitcodepm\ontobuild\petrolonto

# 查看变更
git status

# 添加变更文件
git add .github/workflows/deploy-docs.yml
git add docs/mkdocs.yml

# 提交
git commit -m "ci: add GitHub Pages documentation deployment workflow"

# 推送到远程
git push origin main
```

### 4.2 监控部署状态

1. 打开 GitHub 仓库 → **Actions** 标签
2. 点击正在运行的 `Deploy Documentation to GitHub Pages` 工作流
3. 查看 `build` job 的日志，确认：
   - Rye 安装成功
   - 依赖同步完成
   - MkDocs 构建成功
4. 查看 `deploy` job 的日志，确认：
   - Pages artifact 上传成功
   - 部署到 GitHub Pages 成功
   - 输出部署 URL

### 4.3 验证部署

部署成功后，访问：
```
https://naturegolden.github.io/petrolonto/
```

## 五、本地预览（开发阶段）

在推送前，可以在本地预览文档站点：

### 5.1 使用 Rye 本地运行

```bash
cd d:\gitcodepm\ontobuild\petrolonto\docs

# 同步依赖（首次需要）
rye sync

# 启动本地开发服务器
rye run mkdocs serve
```

浏览器访问：http://127.0.0.1:8000

### 5.2 本地构建验证

```bash
cd d:\gitcodepm\ontobuild\petrolonto\docs

# 严格模式构建（与 CI 一致）
rye run mkdocs build --strict

# 查看输出
ls site/
```

## 六、触发机制说明

### 6.1 自动触发

| 事件 | 条件 | 行为 |
|------|------|------|
| Push to main | `docs/**` 或 `core/**` 有变更 | 构建 + 部署 |
| Pull Request | `docs/**` 或 `core/**` 有变更 | 仅构建验证 |
| Release | 发布新版本 | 构建 + 部署 |

### 6.2 手动触发

1. 打开 GitHub 仓库 → **Actions** 标签
2. 点击 `Deploy Documentation to GitHub Pages` 工作流
3. 点击 **Run workflow** 按钮
4. 选择分支（通常选 `main`）
5. 点击 **Run workflow**

### 6.3 强制重新部署（不修改代码）

```bash
# 创建一个空提交触发部署
git commit --allow-empty -m "ci: trigger docs redeploy"
git push origin main
```

## 七、文档内容更新流程

### 7.1 添加新页面

1. 在 `docs/docs/` 目录下创建新的 `.md` 文件
2. 在 `docs/mkdocs.yml` 的 `nav` 部分添加导航条目
3. 提交并推送

```bash
# 示例：添加新的石油行业本体建模页面
echo "# 石油行业本体建模\n\n这里是内容..." > docs/docs/petroleum-ontology.md

# 编辑 mkdocs.yml，在 nav 中添加：
#       - Petroleum Ontology: petroleum-ontology.md
```

### 7.2 修改现有页面

直接编辑 `docs/docs/` 下的 `.md` 文件，提交推送即可自动部署。

### 7.3 添加图片资源

将图片放在 `docs/docs/` 目录下（或子目录），在 Markdown 中使用相对路径引用：

```markdown
![架构图](./assets/architecture.png)
```

## 八、常见问题排查

### 8.1 构建失败：依赖问题

**症状**：`rye sync` 或 `mkdocs build` 失败

**排查**：
```bash
# 本地复现
cd docs
rye sync --no-lock
rye run mkdocs build --strict
```

**解决**：检查 `docs/pyproject.toml` 中的依赖是否正确。

### 8.2 构建失败：mkdocstrings 导入错误

**症状**：`mkdocstrings` 无法导入 `quivr_core` 模块

**原因**：`docs/pyproject.toml` 中引用了 `core/` 目录的本地路径

**解决**：确保 `core/` 目录的 `pyproject.toml` 格式正确，或者在 CI 中先安装 core：

```yaml
# 在 build job 中添加步骤
- name: Install quivr-core
  run: |
    cd ../core
    pip install -e .
```

### 8.3 部署成功但页面 404

**原因**：GitHub Pages 还未生效（通常需要 1-3 分钟）

**解决**：等待几分钟后刷新页面，或检查 `https://github.com/naturegolden/petrolonto/deployments`

### 8.4 页面样式丢失

**原因**：`site_url` 配置不正确

**解决**：确认 `mkdocs.yml` 中 `site_url` 设置为：
```yaml
site_url: https://naturegolden.github.io/petrolonto/
```

### 8.5 自定义域名配置

如果想使用自定义域名（如 `docs.petrolonto.com`）：

1. 在 `docs/` 目录下创建 `CNAME` 文件：
```
docs.petrolonto.com
```

2. 在 DNS 提供商 处添加 CNAME 记录指向 `naturegolden.github.io`

3. 在 GitHub 仓库 **Settings → Pages → Custom domain** 中输入域名

## 九、后续优化建议

### 9.1 添加版本控制

使用 `mike` 工具实现多版本文档：

```yaml
# 在 docs/pyproject.toml 中添加
dependencies = [
    "mike>=2.0.0",
]
```

```yaml
# 在工作流中添加
- name: Deploy with mike
  run: |
    git config user.name "github-actions"
    git config user.email "actions@github.com"
    mike deploy --push --update-aliases latest
```

### 9.2 添加搜索功能

MkDocs Material 已内置搜索，无需额外配置。如需增强搜索，可集成 Algolia DocSearch。

### 9.3 添加分析

在 `mkdocs.yml` 中添加 Google Analytics：

```yaml
extra:
  analytics:
    provider: google
    property: G-XXXXXXXXXX
```

### 9.4 添加社交卡片

```yaml
extra:
  social:
    - icon: fontawesome/brands/github
      link: https://github.com/naturegolden/petrolonto
```

## 十、完整文件清单

| 文件 | 状态 | 说明 |
|------|------|------|
| `.github/workflows/deploy-docs.yml` | ✅ 已创建 | GitHub Actions 部署工作流 |
| `docs/mkdocs.yml` | ✅ 已修改 | 更新站点配置（site_url、repo_url 等） |
| `docs/docs/**/*.md` | 现有 | 文档内容 |
| `docs/pyproject.toml` | 现有 | 文档依赖配置 |
| `docs/overrides/empty` | 现有 | 主题覆盖目录 |
| `docs/docs/css/style.css` | 现有 | 自定义样式 |

## 十一、快速操作清单

- [ ] 1. 在 GitHub 仓库 Settings → Pages 中选择 "GitHub Actions" 作为部署源
- [ ] 2. 推送 `.github/workflows/deploy-docs.yml` 和更新的 `docs/mkdocs.yml`
- [ ] 3. 在 GitHub Actions 标签页监控构建和部署状态
- [ ] 4. 部署成功后访问 `https://naturegolden.github.io/petrolonto/` 验证
- [ ] 5. （可选）配置自定义域名
