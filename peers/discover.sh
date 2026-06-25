#!/bin/zsh
# 学术仓库自循环 · 一轮发现引擎。用法: ./discover.sh  (需 gh 已登录)
DIR="${0:A:h}"; SEEN="$DIR/seen.txt"; touch "$SEEN"
TERMS=( "AI scientist" "autonomous research" "automated scientific discovery" "AI co-scientist"
        "automated paper writing" "AI survey generation" "scientific writing agent"
        "research agent" "agentic data science" "ML research agent" "self-driving lab"
        "agent harness" "autoresearch runtime" "self-improving agent" "vibe research"
        "scientific agent skills" "academic agent skills" )
TOPICS=( ai-scientist research-automation autonomous-agents )
echo "== 新发现(不在 seen.txt) =="
{ for t in "${TERMS[@]}"; do
    gh search repos "$t" --sort stars --limit 8 --json fullName,stargazersCount,description 2>/dev/null
  done
  for tp in "${TOPICS[@]}"; do
    gh search repos --topic "$tp" --sort stars --limit 8 --json fullName,stargazersCount,description 2>/dev/null
  done; } | python3 -c '
import json,sys,os
seen=set(l.strip().lower() for l in open(os.environ["SEEN"]))
out={}
for line in sys.stdin:
    line=line.strip()
    if not line.startswith("["): continue
    for r in json.loads(line):
        fn=r["fullName"]
        if fn.lower() in seen or fn in out: continue
        out[fn]=(r["stargazersCount"], (r["description"] or "")[:80])
for fn,(s,d) in sorted(out.items(), key=lambda x:-x[1][0]):
    print(f"⭐{s:>6}  {fn} — {d}")
print(f"\n[{len(out)} 个新候选。人工挑 Tier 后追加进 AUTO_DISCOVERY_LOOP.md 注册表 + seen.txt]")
'
