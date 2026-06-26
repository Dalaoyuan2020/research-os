#!/usr/bin/env python3
# Research OS logo 终版 —— 无核风车(A) + 柔和增长 + 金种子; 副标题: 学术 Agentic 工具 Hub
INK="#1f2b47"; GOLD="#e0a94a"; PAPER="#ffffff"; PAGE="#9aa7bd"
T=1.40; LENS=[3.4,2.9,2.5,2.25]; GOLD_IDX=3  # 每本都是矩形(书形); 种子2.25/1.4=1.6≈黄金5:8; 前大后小
TILT=15                                       # 顺时针倾角, 给一点动感

SW=0.15   # 描边收细(原0.22), 不再显呆
def book(x,y,w,h,fill,vertical,stroke,page_color):
    rx=min(0.18,min(w,h)*0.26)
    s=[f'<rect x="{x:.3f}" y="{y:.3f}" width="{w:.3f}" height="{h:.3f}" rx="{rx:.3f}" fill="{fill}" stroke="{stroke}" stroke-width="{SW}" stroke-linejoin="round"/>']
    # 最简书符号 = 靠"外侧短边"的一条装订脊线 (notebook 图标式: 矩形+边线=书)
    pc = page_color if fill!=GOLD else "#9c7a2a"
    if vertical:        # 竖书: 脊线=横线, 靠离中心远的那个短端
        far_top = abs(y) > abs(y+h)
        sy = y + h*0.15 if far_top else y + h*0.85
        x1,x2 = x+w*0.20, x+w*0.80
        s.append(f'<line x1="{x1:.3f}" y1="{sy:.3f}" x2="{x2:.3f}" y2="{sy:.3f}" stroke="{pc}" stroke-width="{SW}" stroke-linecap="round"/>')
    else:               # 横书: 脊线=竖线, 靠离中心远的那个短端
        far_left = abs(x) > abs(x+w)
        sx = x + w*0.15 if far_left else x + w*0.85
        y1,y2 = y+h*0.20, y+h*0.80
        s.append(f'<line x1="{sx:.3f}" y1="{y1:.3f}" x2="{sx:.3f}" y2="{y2:.3f}" stroke="{pc}" stroke-width="{SW}" stroke-linecap="round"/>')
    return "\n".join(s)

def body(stroke,page_color,paper_fill):
    eu,el,ed,er=LENS; t=T
    arms=[(0,-eu,t,eu,True),(-el,-t,el,t,False),(-t,0,t,ed,True),(0,0,er,t,False)]
    bk=[book(arms[i][0],arms[i][1],arms[i][2],arms[i][3],
             GOLD if GOLD_IDX==i else paper_fill, arms[i][4], stroke, page_color) for i in range(4)]
    xs=[a[0] for a in arms]+[a[0]+a[2] for a in arms]
    ys=[a[1] for a in arms]+[a[1]+a[3] for a in arms]
    return "\n".join(bk),(min(xs)+max(xs))/2,(min(ys)+max(ys))/2

def place(scale,cx,cy,stroke=INK,page_color=PAGE,paper_fill=PAPER,angle=TILT):
    b,bcx,bcy=body(stroke,page_color,paper_fill)
    return (f'<g transform="rotate({angle} {cx:.2f} {cy:.2f}) '
            f'translate({cx-bcx*scale:.3f} {cy-bcy*scale:.3f}) scale({scale:.3f})">{b}</g>')

# 1) 纯图标
open("icon_v2.svg","w").write(
f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="1024" height="1024"><rect width="100" height="100" fill="{PAPER}"/>{place(9.6,50,50)}</svg>')

# 2) 横版锁定 —— 文字块视觉垂直居中对齐图标中线, 图标:字 ~1.6:1, 间距≈半字高
open("lockup_v2.svg","w").write(
f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 432 112" width="1728" height="448">
<rect width="432" height="112" fill="{PAPER}"/>
{place(9.6,56,55)}
<text x="94" y="58" font-family="'Helvetica Neue','Arial',sans-serif" font-size="34" font-weight="700" fill="{INK}" letter-spacing="-0.8">Research<tspan font-weight="400" fill="{GOLD}" letter-spacing="1"> OS</tspan></text>
<text x="96" y="78" font-family="'Helvetica Neue','Arial',sans-serif" font-size="12.5" letter-spacing="1"><tspan font-weight="700" fill="{GOLD}">Agentic</tspan><tspan font-weight="500" fill="#7c8aa3"> 学术工具站</tspan></text>
</svg>''')

# 3) 深色版图标 (网站/星球)
open("icon_v2_dark.svg","w").write(
f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="1024" height="1024"><rect width="100" height="100" fill="#0e1422"/>{place(9.6,50,50,stroke="#e9edf6",page_color="#5b6b86",paper_fill="#161e30")}</svg>')
print("ok")

# 4) 字号对比 —— 缩小不同字号给吕博选 (位置仍垂直居中)
FONT="'Helvetica Neue','Arial',sans-serif"
def lockup_svg(title_fs, sub_fs, cy=55, icon_scale=9.6):
    tcap=0.72*title_fs; gap=0.42*title_fs; bh=tcap+gap+sub_fs
    top=cy-bh/2; tb=top+tcap; sb=tb+gap+sub_fs
    return (f'{place(icon_scale,56,cy)}'
        f'<text x="94" y="{tb:.1f}" font-family="{FONT}" font-size="{title_fs}" font-weight="700" fill="{INK}" letter-spacing="-0.8">Research<tspan font-weight="400" fill="{GOLD}" letter-spacing="1"> OS</tspan></text>'
        f'<text x="96" y="{sb:.1f}" font-family="{FONT}" font-size="{sub_fs}" letter-spacing="1"><tspan font-weight="700" fill="{GOLD}">Agentic</tspan><tspan font-weight="500" fill="#7c8aa3"> 学术工具站</tspan></text>')

OPTS=[(31,11.5,"A  31/11.5"),(28,11,"B  28/11"),(25,10.5,"C  25/10.5")]
for fs,sfs,_ in OPTS:
    open(f"lockup_{int(fs)}.svg","w").write(
      f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 432 112" width="1728" height="448"><rect width="432" height="112" fill="{PAPER}"/>{lockup_svg(fs,sfs)}</svg>')
rows=[]
for i,(fs,sfs,name) in enumerate(OPTS):
    rows.append(lockup_svg(fs,sfs,cy=56+i*112))
    rows.append(f'<text x="425" y="{22+i*112}" font-family="Arial" font-size="11" fill="#b0b0b0" text-anchor="end">{name}</text>')
    if i<2: rows.append(f'<line x1="20" y1="{112+i*112}" x2="412" y2="{112+i*112}" stroke="#eee" stroke-width="1"/>')
open("sheet_sizes.svg","w").write(
  f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 432 336" width="1296" height="1008"><rect width="432" height="336" fill="{PAPER}"/>'+"\n".join(rows)+'</svg>')
print("sizes ok")
