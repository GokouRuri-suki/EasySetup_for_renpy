# Requires: nothing (standalone, uses built-in SnowBlossom)
# 依赖：无（可独立使用，仅 Ren'Py 内置 SnowBlossom）

image snow = SnowBlossom(
    Text("●", color="#fff", size=8),
    count=200,
    xspeed=(-2, 4),
    yspeed=(40, 100),
    border=50,
    start=0,
    fast=True)

image rain = SnowBlossom(
    Solid("#aabbcc", xsize=3, ysize=18),
    count=80,
    xspeed=(-5, 5),
    yspeed=(200, 500),
    border=50,
    start=0.05,
    fast=True)