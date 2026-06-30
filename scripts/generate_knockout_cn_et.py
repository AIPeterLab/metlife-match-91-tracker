from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"

R32 = {
    73: ("6月28日 3:00 PM ET", "南非", "加拿大"),
    74: ("6月29日 4:30 PM ET", "德国", "巴拉圭"),
    75: ("6月29日 9:00 PM ET", "荷兰", "摩洛哥"),
    76: ("6月29日 1:00 PM ET", "巴西", "日本"),
    77: ("6月30日 5:00 PM ET", "法国", "瑞典"),
    78: ("6月30日 1:00 PM ET", "科特迪瓦", "挪威"),
    79: ("6月30日 9:00 PM ET", "墨西哥", "厄瓜多尔"),
    80: ("7月1日 12:00 PM ET", "英格兰", "刚果（金）"),
    81: ("7月1日 8:00 PM ET", "美国", "波黑"),
    82: ("7月1日 4:00 PM ET", "比利时", "塞内加尔"),
    83: ("7月2日 7:00 PM ET", "葡萄牙", "克罗地亚"),
    84: ("7月2日 3:00 PM ET", "西班牙", "奥地利"),
    85: ("7月2日 11:00 PM ET", "瑞士", "阿尔及利亚"),
    86: ("7月3日 6:00 PM ET", "阿根廷", "佛得角"),
    87: ("7月3日 9:30 PM ET", "哥伦比亚", "加纳"),
    88: ("7月3日 2:00 PM ET", "澳大利亚", "埃及"),
}

NEXT = {
    89: ("7月4日 5:00 PM ET", "M74胜者", "M77胜者"),
    90: ("7月4日 1:00 PM ET", "M73胜者", "M75胜者"),
    91: ("7月5日 4:00 PM ET", "M76胜者", "M78胜者"),
    92: ("7月5日 8:00 PM ET", "M79胜者", "M80胜者"),
    93: ("7月6日 3:00 PM ET", "M83胜者", "M84胜者"),
    94: ("7月6日 8:00 PM ET", "M81胜者", "M82胜者"),
    95: ("7月7日 12:00 PM ET", "M86胜者", "M88胜者"),
    96: ("7月7日 4:00 PM ET", "M85胜者", "M87胜者"),
    97: ("7月9日 4:00 PM ET", "M89胜者", "M90胜者"),
    98: ("7月10日 3:00 PM ET", "M93胜者", "M94胜者"),
    99: ("7月11日 5:00 PM ET", "M91胜者", "M92胜者"),
    100: ("7月11日 9:00 PM ET", "M95胜者", "M96胜者"),
    101: ("7月14日 3:00 PM ET", "M97胜者", "M98胜者"),
    102: ("7月15日 3:00 PM ET", "M99胜者", "M100胜者"),
    103: ("7月18日 5:00 PM ET", "M101负者", "M102负者"),
    104: ("7月19日 3:00 PM ET", "M101胜者", "M102胜者"),
}

BLOCKS = [
    ("左上路径", "left", 40, 150, [(74, 77, 89), (73, 75, 90)], 97),
    ("右上路径", "right", 760, 150, [(76, 78, 91), (79, 80, 92)], 99),
    ("左下路径", "left", 40, 910, [(83, 84, 93), (81, 82, 94)], 98),
    ("右下路径", "right", 760, 910, [(86, 88, 95), (85, 87, 96)], 100),
]

BOX_H = 78
BOX_GAP = 102


def esc(value: str) -> str:
    return (
        value.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def text(x: int, y: int, value: str, cls: str, anchor: str | None = None) -> str:
    extra = f' text-anchor="{anchor}"' if anchor else ""
    return f'<text class="{cls}" x="{x}" y="{y}"{extra}>{esc(value)}</text>'


def connector(points: str, cls: str = "connector") -> str:
    return f'<path class="{cls}" d="{points}"/>'


def box(x: int, y: int, w: int, h: int, cls: str, match_no: int, label: str, team_a: str, team_b: str) -> list[str]:
    return [
        f'<g id="m{match_no}">',
        f'  <rect class="{cls}" x="{x}" y="{y}" width="{w}" height="{h}" rx="10"/>',
        text(x + 12, y + 22, f"M{match_no} · {label}", "time"),
        text(x + 12, y + 48, team_a, "team"),
        text(x + 12, y + 69, team_b, "team"),
        "</g>",
    ]


def draw_pair_left(x: int, y: int, first: int, second: int, target: int) -> list[str]:
    r32_x = x + 22
    r16_x = x + 252
    mid_x = x + 218
    target_y = y + 50
    lines: list[str] = []
    lines += box(r32_x, y, 172, BOX_H, "match", first, *R32[first])
    lines += box(r32_x, y + BOX_GAP, 172, BOX_H, "match", second, *R32[second])
    lines += box(r16_x, target_y, 168, BOX_H, "slot", target, *NEXT[target])
    lines.append(connector(f"M{r32_x+172} {y+39} H{mid_x} V{target_y+39} H{r16_x}"))
    lines.append(connector(f"M{r32_x+172} {y+BOX_GAP+39} H{mid_x} V{target_y+39} H{r16_x}"))
    return lines


def draw_pair_right(x: int, y: int, first: int, second: int, target: int) -> list[str]:
    r16_x = x + 180
    r32_x = x + 408
    mid_x = x + 384
    target_y = y + 50
    lines: list[str] = []
    lines += box(r32_x, y, 172, BOX_H, "match", first, *R32[first])
    lines += box(r32_x, y + BOX_GAP, 172, BOX_H, "match", second, *R32[second])
    lines += box(r16_x, target_y, 168, BOX_H, "slot", target, *NEXT[target])
    lines.append(connector(f"M{r32_x} {y+39} H{mid_x} V{target_y+39} H{r16_x+168}"))
    lines.append(connector(f"M{r32_x} {y+BOX_GAP+39} H{mid_x} V{target_y+39} H{r16_x+168}"))
    return lines


def draw_block(name: str, side: str, x: int, y: int, pairs: list[tuple[int, int, int]], qf: int) -> list[str]:
    lines: list[str] = [
        f'<rect class="panel" x="{x}" y="{y}" width="600" height="540" rx="14"/>',
        text(x + 24, y + 38, name, "section"),
    ]
    pair_y = [y + 70, y + 300]
    r16_centers = []
    for idx, (first, second, target) in enumerate(pairs):
        if side == "left":
            lines += draw_pair_left(x, pair_y[idx], first, second, target)
            r16_centers.append((x + 252 + 168, pair_y[idx] + 50 + 39))
        else:
            lines += draw_pair_right(x, pair_y[idx], first, second, target)
            r16_centers.append((x + 180, pair_y[idx] + 50 + 39))

    qf_y = y + 232
    if side == "left":
        qf_x = x + 446
        join_x = x + 432
        lines += box(qf_x, qf_y, 132, BOX_H, "quarter", qf, *NEXT[qf])
        lines.append(connector(f"M{r16_centers[0][0]} {r16_centers[0][1]} H{join_x} V{qf_y+39} H{qf_x}"))
        lines.append(connector(f"M{r16_centers[1][0]} {r16_centers[1][1]} H{join_x} V{qf_y+39} H{qf_x}"))
    else:
        qf_x = x + 22
        join_x = x + 166
        lines += box(qf_x, qf_y, 132, BOX_H, "quarter", qf, *NEXT[qf])
        lines.append(connector(f"M{r16_centers[0][0]} {r16_centers[0][1]} H{join_x} V{qf_y+39} H{qf_x+132}"))
        lines.append(connector(f"M{r16_centers[1][0]} {r16_centers[1][1]} H{join_x} V{qf_y+39} H{qf_x+132}"))
    return lines


def build_svg() -> str:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines: list[str] = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="1400" height="1700" viewBox="0 0 1400 1700">',
        "<defs>",
        "<style>",
        ".bg{fill:#160b04}.glow{fill:#6b3f10;opacity:.32}.title{font:900 32px 'Microsoft YaHei','Noto Sans CJK SC',Arial,sans-serif;fill:#fff7ed}.subtitle{font:400 10px 'Microsoft YaHei','Noto Sans CJK SC',Arial,sans-serif;fill:#fed7aa}.section{font:800 13px 'Microsoft YaHei','Noto Sans CJK SC',Arial,sans-serif;fill:#ffedd5}.time{font:800 8px 'Microsoft YaHei','Noto Sans CJK SC',Arial,sans-serif;fill:#991b1b}.team{font:800 10px 'Microsoft YaHei','Noto Sans CJK SC',Arial,sans-serif;fill:#111827}.panel{fill:#301707;stroke:#b45309;stroke-width:1.5}.match{fill:#fffaf0;stroke:#f59e0b;stroke-width:1.5}.slot{fill:#fff7ed;stroke:#fb923c;stroke-width:2}.quarter{fill:#ffedd5;stroke:#f97316;stroke-width:2.5}.semi{fill:#fef3c7;stroke:#facc15;stroke-width:2.5}.final{fill:#fff7cc;stroke:#fbbf24;stroke-width:3}.third{fill:#f1f5f9;stroke:#94a3b8;stroke-width:2.5}.connector{fill:none;stroke:#f8fafc;stroke-width:3.5;stroke-linecap:round;stroke-linejoin:round;opacity:.86}.connectorHot{fill:none;stroke:#fbbf24;stroke-width:4;stroke-linecap:round;stroke-linejoin:round}.note{font:400 9px 'Microsoft YaHei','Noto Sans CJK SC',Arial,sans-serif;fill:#fde68a}.pathLabel{font:800 10px 'Microsoft YaHei','Noto Sans CJK SC',Arial,sans-serif;fill:#ffffff}",
        "</style>",
        '<radialGradient id="gold" cx="50%" cy="14%" r="72%"><stop offset="0%" stop-color="#a16207"/><stop offset="45%" stop-color="#3b1d09"/><stop offset="100%" stop-color="#120805"/></radialGradient>',
        "</defs>",
        '<rect class="bg" x="0" y="0" width="1400" height="1700"/>',
        '<rect x="0" y="0" width="1400" height="1700" fill="url(#gold)" opacity=".68"/>',
        '<circle class="glow" cx="700" cy="790" r="280"/>',
        text(70, 70, "2026世界杯淘汰赛赛程", "title"),
        text(72, 102, "美国东部时间（ET）；右侧路径已改为左侧的镜像方向，四分之一决赛和半决赛按 match number 连接。", "subtitle"),
        text(72, 127, f"生成时间：{now}；赛程数据刷新至 2026-06-29。", "subtitle"),
    ]
    for block in BLOCKS:
        lines += draw_block(*block)

    lines += box(490, 724, 185, 88, "semi", 101, *NEXT[101])
    lines += box(725, 724, 185, 88, "semi", 102, *NEXT[102])
    lines += box(592, 575, 216, 92, "final", 104, *NEXT[104])
    lines += box(592, 860, 216, 88, "third", 103, *NEXT[103])

    lines.append(text(450, 704, "M101 = M97胜者 vs M98胜者", "pathLabel"))
    lines.append(text(722, 704, "M102 = M99胜者 vs M100胜者", "pathLabel"))
    lines.append(connector("M618 421 H470 V744 H490", "connectorHot"))
    lines.append(connector("M618 1181 H470 V792 H490", "connectorHot"))
    lines.append(connector("M782 421 H930 V744 H910", "connectorHot"))
    lines.append(connector("M782 1181 H930 V792 H910", "connectorHot"))
    lines.append(connector("M582 724 V690 H700 V667", "connectorHot"))
    lines.append(connector("M818 724 V690 H700 V667", "connectorHot"))
    lines.append(connector("M582 812 V835 H700 V860", "connector"))
    lines.append(connector("M818 812 V835 H700 V860", "connector"))

    lines.append(text(70, 1624, "关键路径：M97=M89/M90，M98=M93/M94，M99=M91/M92，M100=M95/M96；M101=M97/M98，M102=M99/M100。", "note"))
    lines.append(text(70, 1652, "来源：FIFA 公共赛事 API与世界杯 2026 淘汰赛官方赛程框架；第三名落位按 2026-06-29 刷新后的当前对阵。", "note"))
    lines.append("</svg>")
    return "\n".join(lines) + "\n"


def build_html() -> str:
    return """<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>2026 世界杯淘汰赛赛程（ET）</title>
  <style>
    body { margin: 0; background: #120805; color: #ffedd5; font-family: "Microsoft YaHei", "Noto Sans CJK SC", Arial, sans-serif; }
    main { padding: 14px; }
    h1 { margin: 0 0 8px; font-size: clamp(18px, 2.6vw, 26px); }
    p { margin: 0 0 12px; color: #fed7aa; font-size: .84rem; }
    .frame { border: 1px solid #92400e; border-radius: 8px; background: #160b04; }
    img { display: block; width: 1400px; max-width: none; height: auto; }
    a { color: #fde68a; }
    @media (min-width: 900px) {
      body { overflow: hidden; }
      main { height: calc(100vh - 28px); display: flex; flex-direction: column; }
      .frame { flex: 1; min-height: 0; overflow: hidden; display: flex; align-items: center; justify-content: center; }
      img { width: 100%; height: 100%; max-width: 1400px; object-fit: contain; }
    }
    @media (max-width: 899px) {
      .frame { overflow: auto; -webkit-overflow-scrolling: touch; }
    }
  </style>
</head>
<body>
  <main>
    <h1>2026 世界杯淘汰赛赛程（美国东部时间）</h1>
    <p>左右路径已镜面对称；桌面端自动缩放显示完整图片。SVG 原图：<a href="./knockout-cn-et.svg">打开</a></p>
    <div class="frame"><img src="./knockout-cn-et.svg" alt="2026 世界杯淘汰赛中文赛程，美国东部时间"></div>
  </main>
</body>
</html>
"""


def main() -> None:
    DOCS.mkdir(exist_ok=True)
    (DOCS / "knockout-cn-et.svg").write_text(build_svg(), encoding="utf-8")
    (DOCS / "knockout-cn-et.html").write_text(build_html(), encoding="utf-8")
    print("Wrote docs/knockout-cn-et.svg and docs/knockout-cn-et.html")


if __name__ == "__main__":
    main()
