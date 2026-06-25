# Research OS · 学术 AI 工具 Hub

一个学术版的 GitHub —— 把每天最值得用的**学术 AI 工具与 Agent Skill** 挑出来、按研究阶段分好,帮你快速找到它们,学清楚细节、提取核心。

**🌐 在线访问:** https://dalaoyuan2020.github.io/research-os/

---

## 这个 Hub 是干什么的

GitHub 上每天都冒出新的学术 AI 工具(自动写论文、自动跑实验、科研 Agent、写作 Skill……),好东西散落各处,很难一眼找到。
Research OS 做一件事:**替你收口** —— 每天扫一遍 GitHub,把真正值得用的挑出来,按你的**研究阶段**(找想法 / 做实验 / 写论文 / 综合)分类,做成一个可读、可筛、可跳转的热榜,中转到各自的仓库。

你可以在这里:
- 按研究阶段快速找到对口的工具
- 看「热榜 / 新榜」追最火、最新的项目
- 拖动首页的 **Skill 星球**,点节点直达对应仓库
- 顺着我们的**五层科研系统**,看这些工具能怎么串成一条流水线

## 理念

我是**吕志远**,河海大学在校学生。
我的想法是:在 AI 时代,学一个 AI 工具,提升的不只是「会用这个工具」——更重要的是,它让我们**更高效地获取想法、与人交流、并不断把别人的好东西吸收进来、迭代进化**。
工具会过时,但「会快速读懂别人最好的工程、转化成自己的能力」这件事不会。这个 Hub,就是把这套吸收的过程公开出来,也想找一些同频的伙伴一起做。

## 结构(仓库 → 项目 → 网页)

```
research-os/
├── index.html          ← 网页(GitHub Pages 直接服务)
├── data/repos.json     ← 数据库:收录的工具(单一真源)
├── build/
│   ├── build.py        ← 构建器:读 data/repos.json → 生成 index.html
│   └── template.html   ← 页面模板(样式/交互,锁定)
├── manage.py           ← 管理端口:增量维护(给自动化操作员用)
├── peers/discover.sh   ← 发现引擎:关键词扫 GitHub,挖同类新仓库
└── README.md
```

## 怎么维护(管理端口,不推倒重建)

日常维护交给一个自动化操作员(OpenClaw / Harness 这类 Agent),它**只走固定的规范端口**增量更新,不手改网页、不推倒重建:

```bash
python manage.py list                                  # 看当前收录
python manage.py add-repo owner/name --stage 实验      # 增量加一个工具(自动取 stars/描述)
python manage.py refresh                               # 刷新所有 stars
python manage.py build                                 # 由数据库重建 index.html
python manage.py publish "add: xxx"                    # 提交并上线
```

- **数据库** = `data/repos.json`。加新工具 = 往里加一条记录,从不手改 `index.html`。
- 修改类操作需设置环境变量 `ROS_TOKEN`(操作确认门);真正的写权限由 GitHub 账号控制。
- `阶段` 取值:`想法` / `实验` / `写作` / `综合`。

## 本地预览 / 构建

```bash
python build/build.py      # 由 data/repos.json 重建 index.html
# 然后用任意静态服务器打开 index.html(页面用到 CDN 模块,直接双开也基本可用)
```

## 一起做

欢迎做学术的同学、研究者。发现了好用的工具/Skill,提个 Issue 或 PR 就行。

## License

[MIT](./LICENSE) · © 2026 吕志远 (Dalaoyuan2020)
