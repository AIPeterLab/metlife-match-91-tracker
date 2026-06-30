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
    ("左上路径", 70, 245, [(74, 77, 89), (73, 75, 90)], 97),
    ("右上路径", 970, 245, [(76, 78, 91), (79, 80, 92)], 99),
    ("左下路径", 70, 1265, [(83, 84, 93), (81, 82, 94)], 98),
    ("右下路径", 970, 1265, [(86, 88, 95), (85, 87, 96)], 100),
]


def esc(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def text(x: int, y: int, value: str, cls: str) -> str:
    return f'<text class="{cls}" x="{x}" y="{y}">{esc(value)}</text>'


def box(x: int, y: int, w: int, h: int, cls: str, match_no: int, label: str, team_a: str, team_b: str) -> list[str]:
    return [
        f'<g id="m{match_no}">',
        f'  <rect class="{cls}" x="{x}" y="{y}" width="{w}" height="{h}" rx="14"/>',
        text(x + 18, y + 30, f"M{match_no} · {label}", "time"),
        text(x + 18, y + 66, team_a, "team"),
        text(x + 18, y + 100, team_b, "team"),
        "</g>",
    ]


def connector(points: str, cls: str = "connector") -> str:
    return f'<path class="{cls}" d="{points}"/>'


def draw_pair(x: int, y: int, first: int, second: int, target: int) -> list[str]:
    lines: list[str] = []
    lines += box(x, y, 245, 120, "match", first, *R32[first])
    lines += box(x, y + 155, 245, 120, "match", second, *R32[second])
    lines += box(x + 315, y + 78, 240, 120, "slot", target, *NEXT[target])
    mid_x = x + 280
    tgt_x = x + 315
    lines.append(connector(f"M{x+245} {y+60} H{mid_x} V{y+138} H{tgt_x}"))
    lines.append(connector(f"M{x+245} {y+215} H{mid_x} V{y+138} H{tgt_x}"))
    return lines


def draw_block(name: str, x: int, y: int, pairs: list[tuple[int, int, int]], qf: int) -> list[str]:
    lines: list[str] = [
        f'<rect class="panel" x="{x}" y="{y}" width="760" height="755" rx="18"/>',
        text(x + 26, y + 48, name, "section"),
    ]
    pair_y = [y + 84, y + 420]
    r16_centers = []
    for idx, (first, second, target) in enumerate(pairs):
        lines += draw_pair(x + 28, pair_y[idx], first, second, target)
        r16_centers.append(pair_y[idx] + 138)

    qf_x = x + 610
    qf_y = y + 318
    lines += box(qf_x, qf_y, 225, 120, "quarter", qf, *NEXT[qf])
    join_x = x + 595
    lines.append(connector(f"M{x+28+555} {r16_centers[0]} H{join_x} V{qf_y+60} H{qf_x}"))
    lines.append(connector(f"M{x+28+555} {r16_centers[1]} H{join_x} V{qf_y+60} H{qf_x}"))
    return lines


def build_svg() -> str:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines: list[str] = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="1800" height="2380" viewBox="0 0 1800 2380">',
        "<defs>",
        "<style>",
        ".bg{fill:#160b04}.glow{fill:#6b3f10;opacity:.38}.title{font:900 62px 'Microsoft YaHei','Noto Sans CJK SC',Arial,sans-serif;fill:#fff7ed}.subtitle{font:400 24px 'Microsoft YaHei','Noto Sans CJK SC',Arial,sans-serif;fill:#fed7aa}.section{font:800 28px 'Microsoft YaHei','Noto Sans CJK SC',Arial,sans-serif;fill:#ffedd5}.time{font:800 20px 'Microsoft YaHei','Noto Sans CJK SC',Arial,sans-serif;fill:#991b1b}.team{font:800 28px 'Microsoft YaHei','Noto Sans CJK SC',Arial,sans-serif;fill:#111827}.panel{fill:#301707;stroke:#b45309;stroke-width:2}.match{fill:#fffaf0;stroke:#f59e0b;stroke-width:2}.slot{fill:#fff7ed;stroke:#fb923c;stroke-width:2.5}.quarter{fill:#ffedd5;stroke:#f97316;stroke-width:3}.semi{fill:#fef3c7;stroke:#facc15;stroke-width:3}.final{fill:#fff7cc;stroke:#fbbf24;stroke-width:4}.third{fill:#f1f5f9;stroke:#94a3b8;stroke-width:3}.connector{fill:none;stroke:#f8fafc;stroke-width:5;stroke-linecap:round;stroke-linejoin:round;opacity:.86}.connectorHot{fill:none;stroke:#fbbf24;stroke-width:7;stroke-linecap:round;stroke-linejoin:round}.note{font:400 22px 'Microsoft YaHei','Noto Sans CJK SC',Arial,sans-serif;fill:#fde68a}.pathLabel{font:800 24px 'Microsoft YaHei','Noto Sans CJK SC',Arial,sans-serif;fill:#ffffff}",
        "</style>",
        '<radialGradient id="gold" cx="50%" cy="15%" r="75%"><stop offset="0%" stop-color="#a16207"/><stop offset="45%" stop-color="#3b1d09"/><stop offset="100%" stop-color="#120805"/></radialGradient>',
        "</defs>",
        '<rect class="bg" x="0" y="0" width="1800" height="2380"/>',
        '<rect x="0" y="0" width="1800" height="2380" fill="url(#gold)" opacity=".68"/>',
        '<circle class="glow" cx="900" cy="1080" r="390"/>',
        text(90, 92, "2026世界杯淘汰赛赛程", "title"),
        text(92, 134, "比赛时间已统一换成美国东部时间（ET）。四分之一决赛与半决赛连线按官方 match number 路径重画。", "subtitle"),
        text(92, 170, f"生成时间：{now}；赛程数据刷新至 2026-06-29。", "subtitle"),
    ]

    for block in BLOCKS:
        lines += draw_block(*block)

    # Semifinals, third-place match, and final.
    lines += box(595, 1088, 285, 132, "semi", 101, *NEXT[101])
    lines += box(920, 1088, 285, 132, "semi", 102, *NEXT[102])
    lines += box(750, 870, 300, 138, "final", 104, *NEXT[104])
    lines += box(750, 1298, 300, 132, "third", 103, *NEXT[103])

    # Correct quarterfinal-to-semifinal connectors.
    lines.append(text(588, 1058, "半决赛：M97胜者 vs M98胜者", "pathLabel"))
    lines.append(text(914, 1058, "半决赛：M99胜者 vs M100胜者", "pathLabel"))
    lines.append(connector("M905 623 H930 V1108 H595", "connectorHot"))
    lines.append(connector("M905 1643 H930 V1188 H595", "connectorHot"))
    lines.append(connector("M1580 623 H1510 V1108 H1205", "connectorHot"))
    lines.append(connector("M1580 1643 H1510 V1188 H1205", "connectorHot"))

    # Semifinals to final and third-place match.
    lines.append(connector("M880 1154 H900 V1008", "connectorHot"))
    lines.append(connector("M920 1154 H900 V1008", "connectorHot"))
    lines.append(connector("M880 1154 H900 V1298", "connector"))
    lines.append(connector("M920 1154 H900 V1298", "connector"))

    lines.append(text(92, 2290, "关键路径：M97=M89/M90，M98=M93/M94，M99=M91/M92，M100=M95/M96；M101=M97/M98，M102=M99/M100。", "note"))
    lines.append(text(92, 2326, "来源：FIFA 公共赛事 API与世界杯 2026 淘汰赛官方赛程框架；第三名落位按 2026-06-29 刷新后的当前对阵。", "note"))
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
    main { padding: 18px; }
    h1 { margin: 0 0 10px; font-size: clamp(24px, 5vw, 42px); }
    p { margin: 0 0 14px; color: #fed7aa; }
    .frame { overflow: auto; border: 1px solid #92400e; border-radius: 8px; background: #160b04; }
    img { display: block; width: 1800px; max-width: none; height: auto; }
    a { color: #fde68a; }
  </style>
</head>
<body>
  <main>
    <h1>2026 世界杯淘汰赛赛程（美国东部时间）</h1>
    <p>四分之一决赛和半决赛路径已按 match number 重画。可横向滚动查看，或打开 <a href="./knockout-cn-et.svg">SVG 原图</a>。</p>
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
