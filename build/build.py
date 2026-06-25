# -*- coding: utf-8 -*-
# Research OS 构建器:读 data/repos.json(单一数据库)→ 套 template.html → 出 index.html
# 操作员(OpenClaw)只改 data/repos.json,跑本脚本重建,绝不手改 index.html。
import json, math, os
HERE = os.path.dirname(os.path.abspath(__file__))
DB   = os.path.normpath(os.path.join(HERE, "..", "data", "repos.json"))
OUT  = os.path.normpath(os.path.join(HERE, "..", "index.html"))
TPL  = os.path.join(HERE, "template.html")

items = json.load(open(DB, encoding="utf-8"))
items.sort(key=lambda x: -x["stars"])

SC = {"想法": "#6c9bff", "实验": "#ecc079", "写作": "#34d3c0", "综合": "#a78bfa"}
STAGES = [("all", "全部"), ("想法", "想法"), ("实验", "实验"), ("写作", "写作"), ("综合", "综合")]
maxs = max((i["stars"] for i in items), default=1) or 1
tot  = sum(i["stars"] for i in items)
def barw(s): return round(100 * math.log10(s + 1) / math.log10(maxs + 1), 1)
def tagspan(s): return '<span class="sg" style="color:%s;border-color:%s55;background:%s1a">%s</span>' % (SC[s], SC[s], SC[s], s)

def rowhtml(it, i):
    stags = "".join(tagspan(s) for s in it["stages"])
    seed = '<span class="seed">种子</span>' if it.get("seed") else ''
    return ('<a class="row" href="https://github.com/%s" target="_blank" data-stars="%d" data-push="%s" data-stages="%s">'
            '<div class="rk">%d</div>'
            '<div class="ni"><div class="nm">%s%s</div><div class="meta"><span class="tp">%s</span>%s</div></div>'
            '<div class="sw"><div class="st" data-star="%d"><span class="sstar">★</span> <span class="snum">0</span></div><div class="hb"><span style="width:%s%%"></span></div></div>'
            '<div class="one">%s</div><div class="go">↗</div></a>') % (
            it["name"], it["stars"], it["push"], " ".join(it["stages"]), i,
            it["label"], seed, it["typ"], stags, it["stars"], barw(it["stars"]), it["one"])
ROWS = "".join(rowhtml(it, k + 1) for k, it in enumerate(items))

def pill(k, lab):
    dot = '' if k == 'all' else '<i style="background:%s"></i>' % SC[k]
    return '<button class="pill%s" data-stage="%s">%s%s</button>' % (' on' if k == 'all' else '', k, dot, lab)
PILLS = "".join(pill(k, l) for k, l in STAGES)

# 球体节点:按阶段聚类(同色成块)+ 真实 stars + 链接
SORD = {"想法": 0, "实验": 1, "写作": 2, "综合": 3}
nitems = sorted(items, key=lambda x: (SORD.get(x["stages"][0], 9), -x["stars"]))
NODES = [{"t": it["label"], "s": it["stars"], "c": SC[it["stages"][0]], "seed": it.get("seed", False),
          "u": "https://github.com/" + it["name"]} for it in nitems]
NODES_JSON = json.dumps(NODES, ensure_ascii=False)

LAYERS = [("L1", "文件阅读层", "#3b82f6", ["文献检索", "文献分析", "文档结构解析", "本地文献库", "速读卡"]),
          ("L2", "知识库层", "#a855f7", ["文献情报闭环", "知识图谱", "洞察向上传播"]),
          ("L3", "文献写作层", "#22c55e", ["改稿版本管理", "交互批审", "模拟期刊评审", "引用规范化", "去AI味", "科研配图"]),
          ("L4", "自动科研层", "#f59e0b", ["实验驾驭 Harness", "自迭代循环", "学术仓库自循环"]),
          ("L5", "项目管理层", "#ef4444", ["多项目看板", "进度总控", "任务编排"])]
LAYHTML = "".join('<div class="lay reveal" style="--lc:%s"><div class="lh"><span class="ln">%s</span><span class="lnm">%s</span></div><div class="lb">%s</div></div>'
                  % (c, ln, nm, "".join('<span class="pl">%s</span>' % s for s in sk)) for ln, nm, c, sk in LAYERS)

I_IDEA = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M9 18h6M10 21h4"/><path d="M12 3a6 6 0 0 1 3.8 10.6c-.5.4-.8 1-.8 1.7H9c0-.7-.3-1.3-.8-1.7A6 6 0 0 1 12 3z"/></svg>'
I_FIND = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><circle cx="11" cy="11" r="7"/><path d="M21 21l-4.3-4.3"/></svg>'
I_ORCH = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="5" cy="6" r="2.1"/><circle cx="19" cy="6" r="2.1"/><circle cx="12" cy="18" r="2.1"/><path d="M6.6 7.6l4 8.8M17.4 7.6l-4 8.8"/></svg>'
I_GOAL = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="12" cy="12" r="8.2"/><circle cx="12" cy="12" r="3.6"/><circle cx="12" cy="12" r=".4" fill="currentColor" stroke="none"/></svg>'
CASE = ('<div class="case reveal">'
        '<div class="cstep"><div class="cic" style="--cc:#6c9bff">%s</div><div class="ct">一个想法</div><div class="cd">"墒情预测能不能更准、更说服人?"</div></div>'
        '<div class="carrow">&rarr;</div>'
        '<div class="cstep"><div class="cic" style="--cc:#6c9bff">%s</div><div class="ct">收集</div><div class="cd">文献检索 + 文献分析,对标目标期刊真实惯例</div></div>'
        '<div class="carrow">&rarr;</div>'
        '<div class="cstep"><div class="cic" style="--cc:#a78bfa">%s</div><div class="ct">编排</div><div class="cd">改稿版本管理 + 模拟期刊评审 + 去AI味,串成改稿闭环</div></div>'
        '<div class="carrow">&rarr;</div>'
        '<div class="cstep"><div class="cic" style="--cc:#34d3c0">%s</div><div class="ct">效果</div><div class="cd">选出最稳的方法,改成一篇能投出去的论文</div></div>'
        '</div>') % (I_IDEA, I_FIND, I_ORCH, I_GOAL)

t = open(TPL, encoding="utf-8").read()
out = (t.replace("__ROWS__", ROWS).replace("__PILLS__", PILLS).replace("__LAYERS__", LAYHTML)
        .replace("__NODES__", NODES_JSON).replace("__CASE__", CASE)
        .replace("__NREPO__", str(len(items))).replace("__TOTK__", str(tot // 1000)))
open(OUT, "w", encoding="utf-8").write(out)
print("built %d repos -> index.html" % len(items))
