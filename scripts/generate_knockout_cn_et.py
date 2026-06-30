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
    103: ("三四名比赛 · 7月18日 5:00 PM ET", "M101负者", "M102负者"),
    104: ("冠亚军决赛 · 7月19日 3:00 PM ET", "M101胜者", "M102胜者"),
}

PREDICTION_NEXT = {
    89: ("7月4日 5:00 PM ET", "巴拉圭", "法国"),
    90: ("7月4日 1:00 PM ET", "加拿大", "摩洛哥"),
    91: ("7月5日 4:00 PM ET", "巴西", "挪威"),
    92: ("7月5日 8:00 PM ET", "墨西哥", "英格兰"),
    93: ("7月6日 3:00 PM ET", "葡萄牙", "西班牙"),
    94: ("7月6日 8:00 PM ET", "美国", "比利时"),
    95: ("7月7日 12:00 PM ET", "阿根廷", "埃及"),
    96: ("7月7日 4:00 PM ET", "瑞士", "哥伦比亚"),
    97: ("7月9日 4:00 PM ET", "法国", "摩洛哥"),
    98: ("7月10日 3:00 PM ET", "西班牙", "美国"),
    99: ("7月11日 5:00 PM ET", "巴西", "英格兰"),
    100: ("7月11日 9:00 PM ET", "阿根廷", "哥伦比亚"),
    101: ("7月14日 3:00 PM ET", "法国", "西班牙"),
    102: ("7月15日 3:00 PM ET", "巴西", "阿根廷"),
    103: ("三四名比赛 · 7月18日 5:00 PM ET", "法国", "阿根廷（季军）"),
    104: ("冠亚军决赛 · 7月19日 3:00 PM ET", "西班牙", "巴西（冠军）"),
}

BLOCKS = [
    ("", "left", 40, 150, [(74, 77, 89), (73, 75, 90)], 97),
    ("", "right", 760, 150, [(76, 78, 91), (79, 80, 92)], 99),
    ("", "left", 40, 910, [(83, 84, 93), (81, 82, 94)], 98),
    ("", "right", 760, 910, [(86, 88, 95), (85, 87, 96)], 100),
]

BOX_H = 78
BOX_GAP = 102
R32_W = 86
R16_W = 84
QF_W = 66
SEMI_W = 92
FINAL_W = 108
STAGE_GAP = 40
BRANCH_GAP = STAGE_GAP // 2
LEFT_R32_X = 142
LEFT_R16_X = LEFT_R32_X + R32_W + STAGE_GAP
LEFT_QF_X = LEFT_R16_X + R16_W + STAGE_GAP
RIGHT_R32_X = 600 - LEFT_R32_X - R32_W
RIGHT_R16_X = 600 - LEFT_R16_X - R16_W
RIGHT_QF_X = 600 - LEFT_QF_X - QF_W


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
        text(x + 5, y + 22, f"M{match_no} · {label}", "time"),
        text(x + 5, y + 48, team_a, "team"),
        text(x + 5, y + 69, team_b, "team"),
        "</g>",
    ]


def draw_pair_left(x: int, y: int, first: int, second: int, target: int, next_matches: dict[int, tuple[str, str, str]]) -> list[str]:
    r32_x = x + LEFT_R32_X
    r16_x = x + LEFT_R16_X
    join_x = r32_x + R32_W + BRANCH_GAP
    target_y = y + 50
    lines: list[str] = []
    lines += box(r32_x, y, R32_W, BOX_H, "match", first, *R32[first])
    lines += box(r32_x, y + BOX_GAP, R32_W, BOX_H, "match", second, *R32[second])
    lines += box(r16_x, target_y, R16_W, BOX_H, "slot", target, *next_matches[target])
    lines.append(connector(f"M{r32_x+R32_W} {y+39} H{join_x} V{target_y+39} H{r16_x}"))
    lines.append(connector(f"M{r32_x+R32_W} {y+BOX_GAP+39} H{join_x} V{target_y+39} H{r16_x}"))
    return lines


def draw_pair_right(x: int, y: int, first: int, second: int, target: int, next_matches: dict[int, tuple[str, str, str]]) -> list[str]:
    r16_x = x + RIGHT_R16_X
    r32_x = x + RIGHT_R32_X
    join_x = r32_x - BRANCH_GAP
    target_y = y + 50
    lines: list[str] = []
    lines += box(r32_x, y, R32_W, BOX_H, "match", first, *R32[first])
    lines += box(r32_x, y + BOX_GAP, R32_W, BOX_H, "match", second, *R32[second])
    lines += box(r16_x, target_y, R16_W, BOX_H, "slot", target, *next_matches[target])
    lines.append(connector(f"M{r32_x} {y+39} H{join_x} V{target_y+39} H{r16_x+R16_W}"))
    lines.append(connector(f"M{r32_x} {y+BOX_GAP+39} H{join_x} V{target_y+39} H{r16_x+R16_W}"))
    return lines


def draw_block(name: str, side: str, x: int, y: int, pairs: list[tuple[int, int, int]], qf: int, next_matches: dict[int, tuple[str, str, str]]) -> list[str]:
    lines: list[str] = [
        f'<rect class="panel" x="{x}" y="{y}" width="600" height="540" rx="14"/>',
    ]
    pair_y = [y + 70, y + 300]
    r16_centers = []
    for idx, (first, second, target) in enumerate(pairs):
        if side == "left":
            lines += draw_pair_left(x, pair_y[idx], first, second, target, next_matches)
            r16_centers.append((x + LEFT_R16_X + R16_W, pair_y[idx] + 50 + 39))
        else:
            lines += draw_pair_right(x, pair_y[idx], first, second, target, next_matches)
            r16_centers.append((x + RIGHT_R16_X, pair_y[idx] + 50 + 39))

    qf_y = y + 232
    if side == "left":
        qf_x = x + LEFT_QF_X
        join_x = r16_centers[0][0] + BRANCH_GAP
        lines += box(qf_x, qf_y, QF_W, BOX_H, "quarter", qf, *next_matches[qf])
        lines.append(connector(f"M{r16_centers[0][0]} {r16_centers[0][1]} H{join_x} V{qf_y+39} H{qf_x}"))
        lines.append(connector(f"M{r16_centers[1][0]} {r16_centers[1][1]} H{join_x} V{qf_y+39} H{qf_x}"))
    else:
        qf_x = x + RIGHT_QF_X
        join_x = r16_centers[0][0] - BRANCH_GAP
        lines += box(qf_x, qf_y, QF_W, BOX_H, "quarter", qf, *next_matches[qf])
        lines.append(connector(f"M{r16_centers[0][0]} {r16_centers[0][1]} H{join_x} V{qf_y+39} H{qf_x+QF_W}"))
        lines.append(connector(f"M{r16_centers[1][0]} {r16_centers[1][1]} H{join_x} V{qf_y+39} H{qf_x+QF_W}"))
    return lines


def build_svg(next_matches: dict[int, tuple[str, str, str]] | None = None, prediction: bool = False) -> str:
    next_matches = next_matches or NEXT
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    title = "2026世界杯淘汰赛预测赛程" if prediction else "2026世界杯淘汰赛赛程"
    subtitle = (
        "预测版：根据 2026-06-30 最新 32 强结果，大胆预测所有淘汰赛；美国东部时间（ET）。"
        if prediction
        else "美国东部时间（ET）；右侧路径已改为左侧的镜像方向，四分之一决赛和半决赛按 match number 连接。"
    )
    footer = (
        "大胆预测冠军：巴西；亚军：西班牙；季军：阿根廷；第四名：法国。预测非官方结果。"
        if prediction
        else "关键路径：M97=M89/M90，M98=M93/M94，M99=M91/M92，M100=M95/M96；M101=M97/M98，M102=M99/M100。"
    )
    lines: list[str] = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="1400" height="1700" viewBox="0 0 1400 1700">',
        "<defs>",
        "<style>",
        ".bg{fill:#160b04}.glow{fill:#6b3f10;opacity:.32}.title{font:900 30px 'Microsoft YaHei','Noto Sans CJK SC',Arial,sans-serif;fill:#fff7ed}.subtitle{font:400 9px 'Microsoft YaHei','Noto Sans CJK SC',Arial,sans-serif;fill:#fed7aa}.section{font:800 12px 'Microsoft YaHei','Noto Sans CJK SC',Arial,sans-serif;fill:#ffedd5}.time{font:800 5.8px 'Microsoft YaHei','Noto Sans CJK SC',Arial,sans-serif;fill:#991b1b}.team{font:800 7.8px 'Microsoft YaHei','Noto Sans CJK SC',Arial,sans-serif;fill:#111827}.panel{fill:#301707;stroke:#b45309;stroke-width:1.5}.match{fill:#fffaf0;stroke:#f59e0b;stroke-width:1.5}.slot{fill:#fff7ed;stroke:#fb923c;stroke-width:2}.quarter{fill:#ffedd5;stroke:#f97316;stroke-width:2.5}.semi{fill:#fef3c7;stroke:#facc15;stroke-width:2.5}.final{fill:#fff7cc;stroke:#fbbf24;stroke-width:3}.third{fill:#f1f5f9;stroke:#94a3b8;stroke-width:2.5}.connector{fill:none;stroke:#f8fafc;stroke-width:3.5;stroke-linecap:round;stroke-linejoin:round;opacity:.86}.connectorHot{fill:none;stroke:#fbbf24;stroke-width:4;stroke-linecap:round;stroke-linejoin:round}.note{font:400 8px 'Microsoft YaHei','Noto Sans CJK SC',Arial,sans-serif;fill:#fde68a}.pathLabel{font:800 9px 'Microsoft YaHei','Noto Sans CJK SC',Arial,sans-serif;fill:#ffffff}",
        "</style>",
        '<radialGradient id="gold" cx="50%" cy="14%" r="72%"><stop offset="0%" stop-color="#a16207"/><stop offset="45%" stop-color="#3b1d09"/><stop offset="100%" stop-color="#120805"/></radialGradient>',
        "</defs>",
        '<rect class="bg" x="0" y="0" width="1400" height="1700"/>',
        '<rect x="0" y="0" width="1400" height="1700" fill="url(#gold)" opacity=".68"/>',
        '<circle class="glow" cx="700" cy="790" r="280"/>',
        text(70, 70, title, "title"),
        text(72, 102, subtitle, "subtitle"),
        text(72, 127, f"生成时间：{now}；赛程数据刷新至 2026-06-29。", "subtitle"),
    ]
    for block in BLOCKS:
        lines += draw_block(*block, next_matches)

    lines += box(600, 724, SEMI_W, 88, "semi", 101, *next_matches[101])
    lines += box(708, 724, SEMI_W, 88, "semi", 102, *next_matches[102])
    lines += box(646, 575, FINAL_W, 92, "final", 104, *next_matches[104])
    lines += box(646, 860, FINAL_W, 88, "third", 103, *next_matches[103])

    lines.append(connector("M498 421 H550 V744 H600", "connectorHot"))
    lines.append(connector("M498 1181 H550 V792 H600", "connectorHot"))
    lines.append(connector("M902 421 H850 V744 H800", "connectorHot"))
    lines.append(connector("M902 1181 H850 V792 H800", "connectorHot"))
    lines.append(connector("M646 724 V690 H700 V667", "connectorHot"))
    lines.append(connector("M754 724 V690 H700 V667", "connectorHot"))
    lines.append(connector("M646 812 V835 H700 V860", "connector"))
    lines.append(connector("M754 812 V835 H700 V860", "connector"))

    lines.append(text(70, 1624, footer, "note"))
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
    <p>左右路径已镜面对称；桌面端自动缩放显示完整图片。手机版：<a href="./knockout-cn-et-mobile.html">打开</a>；预测手机版：<a href="./knockout-cn-et-prediction-mobile.html">打开</a>；SVG 原图：<a href="./knockout-cn-et.svg">打开</a></p>
    <div class="frame"><img src="./knockout-cn-et.svg" alt="2026 世界杯淘汰赛中文赛程，美国东部时间"></div>
  </main>
</body>
</html>
"""


def build_mobile_svg() -> str:
    return build_svg().replace('width="1400" height="1700"', 'width="700" height="850"', 1)


def build_prediction_mobile_svg() -> str:
    return build_svg(PREDICTION_NEXT, prediction=True).replace('width="1400" height="1700"', 'width="700" height="850"', 1)


def build_mobile_html() -> str:
    return """<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>2026 世界杯淘汰赛赛程（手机版 ET）</title>
  <style>
    body { margin: 0; background: #120805; color: #ffedd5; font-family: "Microsoft YaHei", "Noto Sans CJK SC", Arial, sans-serif; }
    main { padding: 10px; }
    h1 { margin: 0 0 7px; font-size: clamp(18px, 5vw, 24px); }
    p { margin: 0 0 10px; color: #fed7aa; font-size: .86rem; line-height: 1.35; }
    .frame { border: 1px solid #92400e; border-radius: 8px; background: #160b04; overflow: hidden; display: flex; justify-content: center; }
    img { display: block; width: 100%; max-width: 700px; height: auto; }
    a { color: #fde68a; }
  </style>
</head>
<body>
  <main>
    <h1>2026 世界杯淘汰赛赛程（手机版）</h1>
    <p>手机版使用与桌面版完全相同的图，只缩小显示。桌面版：<a href="./knockout-cn-et.html">打开</a>；预测版：<a href="./knockout-cn-et-prediction-mobile.html">打开</a>；SVG 原图：<a href="./knockout-cn-et-mobile.svg">打开</a></p>
    <div class="frame"><img src="./knockout-cn-et-mobile.svg" alt="2026 世界杯淘汰赛中文缩小版，美国东部时间"></div>
  </main>
</body>
</html>
"""


def build_prediction_mobile_html() -> str:
    return """<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>2026 世界杯淘汰赛预测（手机版 ET）</title>
  <style>
    body { margin: 0; background: #120805; color: #ffedd5; font-family: "Microsoft YaHei", "Noto Sans CJK SC", Arial, sans-serif; }
    main { padding: 10px; }
    h1 { margin: 0 0 7px; font-size: clamp(18px, 5vw, 24px); }
    p { margin: 0 0 10px; color: #fed7aa; font-size: .86rem; line-height: 1.35; }
    .frame { border: 1px solid #92400e; border-radius: 8px; background: #160b04; overflow: hidden; display: flex; justify-content: center; }
    img { display: block; width: 100%; max-width: 700px; height: auto; }
    a { color: #fde68a; }
  </style>
</head>
<body>
  <main>
    <h1>2026 世界杯淘汰赛预测（手机版）</h1>
    <p>同桌面版结构的缩小图，已填入预测晋级队名。普通手机版：<a href="./knockout-cn-et-mobile.html">打开</a>；SVG 原图：<a href="./knockout-cn-et-prediction-mobile.svg">打开</a></p>
    <div class="frame"><img src="./knockout-cn-et-prediction-mobile.svg" alt="2026 世界杯淘汰赛中文预测手机版，美国东部时间"></div>
  </main>
</body>
</html>
"""


def main() -> None:
    DOCS.mkdir(exist_ok=True)
    (DOCS / "knockout-cn-et.svg").write_text(build_svg(), encoding="utf-8")
    (DOCS / "knockout-cn-et.html").write_text(build_html(), encoding="utf-8")
    (DOCS / "knockout-cn-et-mobile.svg").write_text(build_mobile_svg(), encoding="utf-8")
    (DOCS / "knockout-cn-et-mobile.html").write_text(build_mobile_html(), encoding="utf-8")
    (DOCS / "knockout-cn-et-prediction-mobile.svg").write_text(build_prediction_mobile_svg(), encoding="utf-8")
    (DOCS / "knockout-cn-et-prediction-mobile.html").write_text(build_prediction_mobile_html(), encoding="utf-8")
    print("Wrote desktop, mobile, and prediction knockout bracket files")


if __name__ == "__main__":
    main()
