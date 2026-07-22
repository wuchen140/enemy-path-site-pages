import json
import math
import os
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


REPO_ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = Path(os.environ.get(
    "DUNGEON_SOURCE_ROOT",
    "/Users/wuchen/Desktop/破解工具/不服来通关/安卓资源解密输出/decrypted_by_original_path",
))

CONFIGS = [
    (1, 3, 999, 20, "a96c5578-45c7-4856-8647-fe23c6ff40ca.182bb.json"),
    (2, 5, 998, 30, "c9454bd6-79ef-4178-9b9e-d68929f6534f.e0aef.json"),
    (3, 9, 997, 40, "847d4835-0466-47f6-a871-f805863e1b26.880c5.json"),
    (4, 36, 996, 50, "972bde0b-e5a6-4ccf-8849-e53ed3107432.8242b.json"),
    (5, 64, 995, 60, "c83f275e-7cb3-4f38-bcf2-b7e1a32b9d76.b8872.json"),
    (6, 71, 994, 70, "8efc556c-2820-4147-a96f-6f6f121eded6.a9f02.json"),
    (7, 84, 993, 80, "da72f0e5-61f4-4a6b-9602-1b98dc30f6f3.d0d65.json"),
    (8, 95, 992, 90, "03cc18a3-dadf-48a9-a866-f33bc6948dc2.88eaa.json"),
    (9, 100, 991, 100, "360056ef-a6ce-4cfa-be26-b06d1c98e394.b718e.json"),
    (10, 97, 990, 110, "d954ab7c-62ab-436e-a33d-75bbf799270e.349d5.json"),
]


def load_points(file_name):
    container = json.loads((SOURCE_ROOT / file_name).read_text())
    points = container[5][0][2]["1"]
    return [[float(point["x"]), float(point["y"])] for point in points]


def runtime_point_count(points, interval=50):
    count = 1 if points else 0
    for start, end in zip(points, points[1:]):
        distance = math.hypot(end[0] - start[0], end[1] - start[1])
        count += 1 + (math.floor(distance / interval) if distance > interval else 0)
    return count


def path_length(points):
    return sum(math.hypot(end[0] - start[0], end[1] - start[1]) for start, end in zip(points, points[1:]))


def load_font(size):
    for path in (
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    ):
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def render_path(record, output_path):
    width, height = 1200, 900
    margin_top, margin_side, margin_bottom = 110, 90, 80
    image = Image.new("RGB", (width, height), "#ffffff")
    draw = ImageDraw.Draw(image)
    points = record["points"]
    xs = [point[0] for point in points]
    ys = [point[1] for point in points]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    plot_w = width - margin_side * 2
    plot_h = height - margin_top - margin_bottom
    scale = min(plot_w / max(1, max_x - min_x), plot_h / max(1, max_y - min_y))
    offset_x = margin_side + (plot_w - (max_x - min_x) * scale) / 2
    offset_y = margin_top + (plot_h - (max_y - min_y) * scale) / 2

    def convert(point):
        x = offset_x + (point[0] - min_x) * scale
        y = height - margin_bottom - (offset_y - margin_top) - (point[1] - min_y) * scale
        return x, y

    for index in range(6):
        x = margin_side + plot_w * index / 5
        y = margin_top + plot_h * index / 5
        draw.line((x, margin_top, x, height - margin_bottom), fill="#e5e7eb", width=2)
        draw.line((margin_side, y, width - margin_side, y), fill="#e5e7eb", width=2)

    if min_x <= 0 <= max_x:
        axis_x = convert([0, min_y])[0]
        draw.line((axis_x, margin_top, axis_x, height - margin_bottom), fill="#94a3b8", width=3)
    if min_y <= 0 <= max_y:
        axis_y = convert([min_x, 0])[1]
        draw.line((margin_side, axis_y, width - margin_side, axis_y), fill="#94a3b8", width=3)

    screen_points = [convert(point) for point in points]
    draw.line(screen_points, fill="#e11d48", width=6, joint="curve")
    radius = 6
    for x, y in screen_points:
        draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill="#f59e0b", outline="#92400e", width=2)
    for point, color in ((screen_points[0], "#16a34a"), (screen_points[-1], "#2563eb")):
        x, y = point
        draw.ellipse((x - 11, y - 11, x + 11, y + 11), fill=color, outline="#ffffff", width=4)

    title_font = load_font(34)
    meta_font = load_font(22)
    draw.text((45, 28), f"Dungeon {record['difficulty']:02d}  |  Map {record['mapId']}  |  Enemy {record['enemyId']}", fill="#111827", font=title_font)
    draw.text((47, 72), f"{record['rawPointCount']} control points  |  {record['runtimePointCount']} runtime points  |  length {record['pathLength']:.1f}", fill="#64748b", font=meta_font)
    image.save(output_path, optimize=True)


def main():
    records = {}
    assets = REPO_ROOT / "assets"
    assets.mkdir(exist_ok=True)
    for difficulty, map_id, enemy_id, coin, file_name in CONFIGS:
        points = load_points(file_name)
        record = {
            "difficulty": difficulty,
            "mapId": map_id,
            "enemyId": enemy_id,
            "coinPerEnemy": coin,
            "points": points,
            "rawPointCount": len(points),
            "runtimePointCount": runtime_point_count(points),
            "pathLength": round(path_length(points), 3),
            "image": f"assets/dungeon_level_{difficulty:02d}.png",
        }
        records[str(difficulty)] = record
        render_path(record, assets / f"dungeon_level_{difficulty:02d}.png")

    payload = json.dumps(records, ensure_ascii=False, separators=(",", ":"))
    (assets / "dungeon-paths.js").write_text(f"window.dungeonPathData={payload};\n")
    print(f"Generated {sum(item['rawPointCount'] for item in records.values())} control points")
    print(f"Generated {sum(item['runtimePointCount'] for item in records.values())} runtime points")


if __name__ == "__main__":
    main()
