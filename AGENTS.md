# AGENTS.md · 运维操作手册(内部)

> 这份文件写给**维护者本人**和**维护者的运维 Agent**。它不是面向公众的功能介绍 —— 普通访客不需要读它,共创者请看 [CONTRIBUTING.md](./CONTRIBUTING.md)。
>
> 这里说明:本仓库**只通过一个固定端口增量维护,绝不手改网页**。运维 Agent(OpenClaw / Harness 这类自动化操作员)读这份文件,就知道怎么安全地更新 Research OS。

---

## 心法:单一真源 + 固定端口 + 不推倒重建

- **单一真源** = `data/repos.json`。热榜的全部内容都来自它。
- **锁定模板** = `build/template.html`。视觉与交互在这里,**运维不碰它**。
- **构建** = `build/build.py` 读 `data/repos.json` 套模板,生成 `index.html`。
- 因此:改内容 = 改数据库 → 重建 → 发布。**永远是补丁加补丁,不是重写。**

## 端口:`manage.py`

```bash
python manage.py add-repo owner/name --stage 实验   # 发现新工具,一行加进来(自动取 stars/描述)
python manage.py refresh                            # 刷新所有 stars
python manage.py build                              # 由 data/repos.json 重建 index.html
python manage.py publish "add: xxx"                 # 提交并上线
```

- 写操作(add-repo / refresh / publish)需要设置环境变量 **`ROS_TOKEN`** 才放行。
- `add-repo` 会自动抓 stars 和描述,写回 `data/repos.json`,**不要手动编辑 JSON**。
- 加完务必跑一次 `build`,确认 `index.html` 正常,再 `publish`。

## 部署铁律(踩过的坑)

GitHub Pages 是**单线部署**:每来一个新触发,会取消上一个正在跑的部署。

- **一次干净提交 → 停手 → 耐心等它跑完**(几分钟)。
- **不要**反复 push、不要来回切 `build_type`、不要连点 rebuild —— 会互相取消,全部失败。
- 要排查先拿真实日志(`gh run view <id> --log`),别凭笼统报错瞎试。

## 入站:共创者的 Issue 怎么进库

公众通过 [Issue](https://github.com/Dalaoyuan2020/research-os/issues) 推荐工具(见 CONTRIBUTING)。运维 Agent 的职责:

1. 读「推荐工具」类 Issue,核实(真实可用、学术相关、非营销)。
2. 合适 → `python manage.py add-repo <owner/name> --stage <阶段>`。
3. `build` → 自检 → `publish`。
4. 回 Issue 致谢并说明已收录(署名来源)。

## 发现引擎

`peers/discover.sh`:按关键词扫 GitHub,新工具落 `peers/seen.txt` 去重,候选交人工/Agent 复核后再入库。这是热榜"自循环"的来源。

---

*这份文件本身也遵循单一真源原则:运维流程有变,改这里,别散落到各处。*
