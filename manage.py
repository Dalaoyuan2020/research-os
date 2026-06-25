#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Research OS 管理端口 (manage.py)

给 OpenClaw / Harness 这类自动化操作员日常维护用。只做固定的规范操作,
增量更新数据库 data/repos.json,然后由 build 重建 index.html ——
绝不手改 index.html、绝不推倒重建(避免补丁加补丁)。

操作:
  python manage.py list
  python manage.py add-repo <owner/name> --stage 想法|实验|写作|综合 [--type 类型] [--desc "一句话"]
  python manage.py refresh                       # 刷新所有 stars + push 时间
  python manage.py build                          # 由数据库重建 index.html
  python manage.py publish "提交说明"             # git add + commit + push(更新线上)

安全:修改类操作(add-repo / refresh / publish)需设置非空环境变量 ROS_TOKEN 作为操作确认门;
真正的写权限由 GitHub 账号(gh auth)控制。
"""
import sys, os, json, subprocess, argparse
HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(HERE, "data", "repos.json")
STAGES = {"想法", "实验", "写作", "综合"}

def load(): return json.load(open(DB, encoding="utf-8"))
def save(d): json.dump(d, open(DB, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
def gate():
    if not os.environ.get("ROS_TOKEN"):
        sys.exit("✋ 修改类操作需设置 ROS_TOKEN(操作确认门):export ROS_TOKEN=... 后重试")
def gh(args): return subprocess.run(["gh"] + args, capture_output=True, text=True)
def build(): subprocess.run([sys.executable, os.path.join(HERE, "build", "build.py")], check=True)

def cmd_list(_):
    for i, r in enumerate(sorted(load(), key=lambda x: -x["stars"]), 1):
        print("%2d. %-42s ★%-7d %s  %s" % (i, r["name"], r["stars"], "/".join(r["stages"]), r.get("typ", "")))
    print("共 %d 个" % len(load()))

def cmd_add(a):
    gate()
    name = a.repo.strip()
    if "/" not in name: sys.exit("仓库名应为 owner/name")
    if a.stage not in STAGES: sys.exit("--stage 必须是 想法/实验/写作/综合 之一")
    d = load()
    if any(r["name"].lower() == name.lower() for r in d): sys.exit("已存在,跳过:" + name)
    g = gh(["repo", "view", name, "--json", "nameWithOwner,stargazerCount,description,pushedAt"])
    if g.returncode != 0: sys.exit("gh 取不到该仓库:" + name + "\n" + g.stderr)
    j = json.loads(g.stdout)
    rec = {"name": j["nameWithOwner"], "label": j["nameWithOwner"].split("/")[-1],
           "stars": j["stargazerCount"], "typ": a.type or "", "stages": [a.stage],
           "one": (a.desc or j.get("description") or "")[:90], "push": (j.get("pushedAt") or "")[:10], "seed": False}
    d.append(rec); save(d); build()
    print("✅ 已加入并重建:%s ★%d [%s]" % (rec["name"], rec["stars"], a.stage))

def cmd_refresh(_):
    gate(); d = load(); n = 0
    for r in d:
        g = gh(["repo", "view", r["name"], "--json", "stargazerCount,pushedAt"])
        if g.returncode == 0:
            j = json.loads(g.stdout); r["stars"] = j["stargazerCount"]; r["push"] = (j.get("pushedAt") or "")[:10]; n += 1
    save(d); build(); print("✅ 刷新 %d/%d 个并重建" % (n, len(d)))

def cmd_build(_): build(); print("✅ 已重建 index.html")

def cmd_publish(a):
    gate()
    subprocess.run(["git", "-C", HERE, "add", "-A"], check=True)
    subprocess.run(["git", "-C", HERE, "commit", "-m", a.msg], check=True)
    subprocess.run(["git", "-C", HERE, "push"], check=True)
    print("✅ 已发布,GitHub Pages 几分钟后更新")

def main():
    p = argparse.ArgumentParser(description="Research OS 管理端口")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("list").set_defaults(fn=cmd_list)
    pa = sub.add_parser("add-repo"); pa.add_argument("repo"); pa.add_argument("--stage", required=True)
    pa.add_argument("--type", default=""); pa.add_argument("--desc", default=""); pa.set_defaults(fn=cmd_add)
    sub.add_parser("refresh").set_defaults(fn=cmd_refresh)
    sub.add_parser("build").set_defaults(fn=cmd_build)
    pp = sub.add_parser("publish"); pp.add_argument("msg"); pp.set_defaults(fn=cmd_publish)
    a = p.parse_args(); a.fn(a)

if __name__ == "__main__":
    main()
