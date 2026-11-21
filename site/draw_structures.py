"""Draw the user-facing signal-flow diagrams for chapter 6."""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

ASSETS = Path(__file__).resolve().parents[1] / "handout" / "assets"
INK = "#173b53"
FORWARD = "#24688d"
FEEDBACK = "#aa481c"
plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "DejaVu Sans"]


def panel(ax, title, x_max=10, y_max=3.2):
    ax.set(xlim=(-0.3, x_max + 0.25), ylim=(-0.3, y_max))
    ax.set_title(title, loc="left", fontsize=13, pad=10, color=INK)
    ax.axis("off")


def arrow(ax, start, end, label="", offset=(0, 0.16), color=FORWARD):
    ax.annotate("", end, start, arrowprops={
        "arrowstyle": "-|>", "color": color, "lw": 1.45, "shrinkA": 1, "shrinkB": 1
    })
    if label:
        center = [(start[i] + end[i]) / 2 + offset[i] for i in (0, 1)]
        ax.text(*center, label, ha="center", va="bottom", fontsize=11, color=color)


def node(ax, point, label="", *, add=False):
    if add:
        ax.text(*point, "+", ha="center", va="center", fontsize=13, color=INK,
                bbox={"boxstyle": "circle,pad=.15", "fc": "white", "ec": INK}, zorder=5)
    else:
        ax.plot(*point, "o", color=INK, markersize=3.4, zorder=5)
    if label:
        ax.text(point[0], point[1] - 0.28, label, ha="center", va="top", color=INK, fontsize=11)


def route(ax, points, label="", label_offset=(0, -.3), color=FEEDBACK):
    for start, end in zip(points[:-2], points[1:-1]):
        ax.plot([start[0], end[0]], [start[1], end[1]], color=color, lw=1.45)
    arrow(ax, points[-2], points[-1], label, label_offset, color)


def save(fig, name):
    ASSETS.mkdir(parents=True, exist_ok=True)
    fig.savefig(ASSETS / name, dpi=185, facecolor="white")
    plt.close(fig)


def four_forms():
    fig, axes = plt.subplots(2, 2, figsize=(13, 5.7), layout="constrained")
    ax = axes[0, 0]
    panel(ax, "直接 I 型 · 输入链与输出链独立")
    x, x1, s, y, y1, y2 = (0.5, 2.55), (2.5, 2.55), (4.55, 1.75), (6, 1.75), (7.55, 1.75), (9.45, 1.75)
    arrow(ax, x, x1, "$q$")
    arrow(ax, x1, s, "$1$")
    arrow(ax, x, s, "$1$", offset=(0, -.35))
    arrow(ax, s, y)
    arrow(ax, y, y1, "$q$")
    arrow(ax, y1, y2, "$q$")
    route(ax, [y1, (7.55, .65), (4.55, .65), s], "$2/3$", (-.55, -.37))
    route(ax, [y2, (9.45, .15), (3.75, .15), s], "$-1/4$", (-.58, -.48))
    for point, label in [(x,"$x$"),(x1,"$x_1$"),(y,"$y$"),(y1,"$y_1$"),(y2,"$y_2$")]:
        node(ax, point, label)
    node(ax, s, add=True)

    ax = axes[0, 1]
    panel(ax, "直接 II 型 · 两个延时由前馈和反馈共用")
    s, w, w1, w2, out = (1.8, 1.95), (3.15, 1.95), (5.15, 1.95), (7.2, 1.95), (8.6, 2.55)
    arrow(ax,(.45,1.95),s); arrow(ax,s,w); arrow(ax,w,w1,"$q$"); arrow(ax,w1,w2,"$q$")
    route(ax,[w,(3.15,2.55),out],"$1$",(0,.13),FORWARD)
    arrow(ax,w1,out,"$1$",(0,-.33))
    route(ax,[w1,(5.15,.75),(1.8,.75),s],"$2/3$",(-.42,-.3))
    route(ax,[w2,(7.2,.2),(.95,.2),s],"$-1/4$",(-.5,-.45))
    arrow(ax,out,(9.7,2.55))
    for point, label in [((.45,1.95),"$x$"),(w,"$w$"),(w1,"$w_1$"),(w2,"$w_2$"),((9.7,2.55),"$y$")]:
        node(ax,point,label)
    node(ax,s,add=True); node(ax,out,add=True)

    ax = axes[1, 0]
    panel(ax, "一阶节级联 · 前一节输出作为后一节输入")
    for x0, label in [(2.7,r"$\frac{1+q}{1-pq}$"),(7.2,r"$\frac{1}{1-p^*q}$")]:
        ax.text(x0,1.7,label,ha="center",va="center",fontsize=17,
                bbox={"boxstyle":"round,pad=.45","fc":"#e9f4f7","ec":FORWARD},zorder=5)
    arrow(ax,(.5,1.7),(2.7,1.7)); arrow(ax,(2.7,1.7),(7.2,1.7)); arrow(ax,(7.2,1.7),(9.5,1.7))
    for point,label in [((.5,1.7),"$x$"),((4.95,1.7),"$v$"),((9.5,1.7),"$y$")]:
        node(ax,point,label)

    ax = axes[1, 1]
    panel(ax,"一阶节并联 · 两条输出相加")
    for ypos,label in [(2.5,r"$\frac{A}{1-pq}$"),(.8,r"$\frac{A^*}{1-p^*q}$")]:
        route(ax,[(1.25,1.65),(2.2,ypos),(4.75,ypos)],color=FORWARD)
        route(ax,[(4.75,ypos),(7.1,ypos),(8.4,1.65)],color=FORWARD)
        ax.text(4.75,ypos,label,ha="center",va="center",fontsize=16,
                bbox={"boxstyle":"round,pad=.4","fc":"#e9f4f7","ec":FORWARD},zorder=5)
    arrow(ax,(.45,1.65),(1.25,1.65)); arrow(ax,(8.4,1.65),(9.75,1.65))
    node(ax,(8.4,1.65),add=True); node(ax,(1.25,1.65),"$x$"); node(ax,(9.75,1.65),"$y$")
    save(fig,"6-5_四种实现.png")


def fir_forms():
    fig, axes = plt.subplots(3, 1, figsize=(11.6, 7.2), layout="constrained")
    taps = list(range(1, 14, 2))
    ax = axes[0]
    panel(ax, "横截型 · 先延时，再乘系数并相加", 15)
    ax.text(.05, 2.5, "$x[n]$", ha="left", color=INK)
    arrow(ax,(.1,2.2),(1,2.2))
    for k,x in enumerate(taps):
        if k: arrow(ax,(taps[k-1],2.2),(x,2.2),"$q$")
        arrow(ax,(x,2.2),(x,.62),f"$a^{k}$" if k else "$1$",(.24,-.17))
        node(ax,(x,2.2))
        if k: arrow(ax,(taps[k-1],.62),(x,.62))
        node(ax,(x,.62),add=k>0)
    arrow(ax,(13,.62),(14.7,.62)); node(ax,(14.7,.62),"$y[n]$")

    ax = axes[1]
    panel(ax, "转置型 · 先乘系数，再沿部分和的延时链相加", 15)
    arrow(ax,(.1,2.2),(1,2.2)); ax.text(.05,2.5,"$x[n]$",color=INK)
    for k,x in enumerate(taps):
        if k: arrow(ax,(taps[k-1],2.2),(x,2.2))
        power=6-k
        arrow(ax,(x,2.2),(x,.62),f"$a^{power}$" if power else "$1$",(.24,-.17))
        node(ax,(x,2.2))
        if k: arrow(ax,(taps[k-1],.62),(x,.62),"$q$")
        node(ax,(x,.62),add=k>0)
    arrow(ax,(13,.62),(14.7,.62)); node(ax,(14.7,.62),"$y[n]$")

    ax = axes[2]
    panel(ax, "两次乘法 · 七拍前馈抵消指数尾巴", 15)
    inp, sum_node, out = (1,1.7),(9,1.7),(13.8,1.7)
    arrow(ax,inp,sum_node,"$1$"); arrow(ax,sum_node,out)
    route(ax,[inp,(1,2.55),(9,2.55),sum_node],color=FORWARD)
    route(ax,[out,(13.8,.55),(9,.55),sum_node])
    ax.text(5,2.64,"$-a^7q^7$",ha="center",color=FORWARD,fontsize=13)
    ax.text(11.45,.28,"$aq$",ha="center",color=FEEDBACK,fontsize=13)
    node(ax,inp,"$x[n]$"); node(ax,sum_node,add=True); node(ax,out,"$y[n]$")
    save(fig,"6-6_三种实现.png")


if __name__ == "__main__":
    four_forms()
    fir_forms()
