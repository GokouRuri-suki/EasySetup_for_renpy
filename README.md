# EasySetup_for_renpy — 轻松使用 Ren'Py

让 Ren'Py 新手轻松使用的便捷工具，提供简单的自定义语句和自动化角色注册功能。

## 特性

- 自定义语句：shake、move、show_at、合体语句
- 表情自动注册：文件名关键词匹配 expression_map，无对应文件时回退默认
- 侧头像自动注册：side/ 子目录，有文件就注册，无则跳过
- 全参数可调：时长、振幅、缩放比等
- 模块化：语句按类型分文件，可独立提取复用
- 零外部素材依赖：天气效果基于 Ren'Py 内置实现

## 快速开始

1\. 放入 Ren'Py 项目的 `game/` 同级
2\. 编辑 `script.rpy`：

```renpy
label start:
    show_at ch to_center
    ch "你好！"
    shake_x ch happy
    move ch to_right 1.0
    return
```

3\. 运行 `renpy .`

## 角色注册

### 素材目录结构

```
characters/ch1/
├── ch1.png              ← 默认立绘
├── ch1_happy.png        ← 表情差分
├── ch1_angry.png
├── ...
└── side/
    ├── ch1.png          ← 默认侧头像
    ├── ch1_happy.png
    ├── ch1_angry.png
    └── ...
```

### 配置表情映射

```python
# 0_config.rpy
expression_map = {
    "normal": "n",
    "angry": "a",
    "happy": "h",
    "shy": "s",
    "frown": "f",
    "frown_mouth": "fm",
    "sad": "sd",
    "surprise": "sp",
    "cry": "c",
    "upset": "ut",
}
```

### 注册角色

```python
# character_definition.rpy里面写
python early:
    character_zoom.update({
        "ch11111": {"cm": 160, "hat": 200}, #帮你一键完成身高问题,无视立绘尺寸不统一和帽子虚高问题
                                            #注意了，这个是对图片的 所以是image_tag
    })
#具体参数看0_config.rpy
define ch = new({
    "name": "角色1",            #名字
    "image_tag": "ch11111",        #你给这个角色立绘的关联记号
    "file": "../characters/ch1/",  #注册路径
    "side": True,      #有侧边头像
})
```

## 本项目的自定义语句

*表情都不是必填的 默认寻找你上次用的，记住写的是给角色的define 参数（比如上面的ch）， 不是 image_tag*

### 震动

```
shake_x 角色 [表情] [时长] [振幅]       隐藏对话框
shake_y 角色 [表情] [时长] [振幅]
say_shake_x 角色 [表情] "文本" [时长] [振幅]   正常对话框
say_shake_y 角色 [表情] "文本" [时长] [振幅]
```

### 移动

```
move 角色 [表情] to_xxx [时长]
move 角色 [表情] x y [时长]
say_move 角色 [表情] "文本" to_xxx [时长]
say_move 角色 [表情] "文本" x y [时长]
show_at 角色 [表情] to_xxx [dissolve时长]
show_at 角色 [表情] x y [dissolve时长]
```

### 合体

```
shake_move 角色 [表情] [x|y] to_xxx    先抖后移
move_shake 角色 [表情] [x|y] to_xxx    先移后抖
say_shake_move 角色 [表情] "文本" [x|y] to_xxx
say_move_shake 角色 [表情] "文本" [x|y] to_xxx
```

## 可调参数

定义在 `0_config.rpy` 的 `python early:` 块中：


| 变量                 | 默认        | 说明                   |
| -------------------- | ----------- | ---------------------- |
| `shake_total`        | 0.48        | 震动总时长（秒）       |
| `shake_offset`       | 12          | 震动振幅（像素）       |
| `move_dur`           | 0.5         | 移动时长（秒）         |
| `start_pos`          | (0.5, -1.0) | 角色首次出现位置       |
| `dissolve_dur`       | 0.3         | show_at 渐入时长（秒） |
| `combo_move_dur`     | 0.5         | 合体移动时长（秒）     |
| `combo_shake_total`  | 0.48        | 合体震动总时长（秒）   |
| `combo_shake_offset` | 12          | 合体震动振幅（像素）   |
| `side_size`          | 273         | 侧头像尺寸（像素）     |
| `ppm`                | 7.5         | 每厘米像素数           |
| `base_room`          | 0.6         | 立绘缩放回退比例       |
| `base_align`         | (0.5, 1.0)  | 默认锚点               |

## 文件结构

```
game/
├── 0_config.rpy                全局参数
├── character_definition.rpy    角色定义
├── function/
│   ├── anims.rpy               动画类
│   ├── register_api.rpy        注册 API
│   ├── shake/                  震动语句
│   ├── move/                   移动/定位语句
│   ├── combo/                  合体语句
│   └── weather.rpy             天气效果
├── script.rpy                  主脚本
└── ...
characters/ch1/
├── ch1.png
└── side/
    └── ch1.png
```

## 许可证

### 本框架

Apache 2.0

### 字体

思源黑体 SC（Source Han Sans SC）
© 2014-2025 Adobe，保留字体名称 Source。Source 是 Adobe 在美国和/或其他国家的商标。
[SIL Open Font License 1.1](https://github.com/adobe-fonts/source-han-sans)
完整许可证见 `game/fonts/OFL.txt`

### 引擎

基于 [Ren'Py](https://www.renpy.org/) 构建
Ren'Py Visual Novel Engine © 2004-2024 Tom Rothamel
MIT License · 完整许可条款：
https://www.renpy.org/doc/html/license.html
