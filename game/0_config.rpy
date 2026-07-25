# ═══════════════════════════════════════════════════════════════
#  0_config.rpy — 全局配置参数
#  可修改区域：以下标记为 [MODIFIABLE] 的参数
#  不可修改区域：标记为 [DO NOT MODIFY] 的部分
# ═══════════════════════════════════════════════════════════════

python early:
    # ── [MODIFIABLE] 可调参数 ──
    shake_total = 0.48            # 震动总时长（秒）
    shake_offset = 12             # 震动振幅（像素）
    move_dur = 0.5                # 移动时长（秒）
    start_pos = (0.5, -1.0)       # 角色首次出现位置 (xpos, ypos)
    dissolve_dur = 0.3            # show_at 的 默认渐入时长（秒）
    combo_move_dur = 0.7          # 合体语句（move_shake/shake_move）的移动时长（秒）
    combo_shake_total = 0.48      # 合体语句（move_shake/shake_move）的震动总时长（秒）
    combo_shake_offset = 12       # 合体语句（move_shake/shake_move）的震动振幅（像素）
    side_size = 273               # 侧头像尺寸（像素，正方形边长）
    ppm = 7.5                     # 像素每厘米（立绘缩放计算用） 
                        #一般啊 这个像素下默认还可以
                        #你在gui的搜索(ctrl+f)  gui.init可以改屏幕像素的

    # ── [MODIFIABLE] 预设位置 ──
    # renpy的坐标系 左上角为原点(0,0) 往下为y正半轴 往右是x正半轴
    preset_map = {
        'to_left':   (0.2, 1.3),
        'to_center': (0.5, 1.3),
        'to_right':  (0.8, 1.3),#这个默认是遮住小腿(大概)脚了的不想遮住就第二个数字都改为1.0
    }

    # ── [MODIFIABLE] 表情关键词→代码映射 ──
    expression_map = {
        "normal": "n",
        "angry": "a",
        "happy": "h",
        "shy": "s",
        "frown": "f",
        "sad": "sd",
        "surprise": "sp",
        "think": "t",
        "doubt": "d",
        "panic": "p",
        "cry": "c",
        "frown_mouth": "fm",
        "upset": "ut",
    }

    # ── [MODIFIABLE] 角色样式默认配置 ──
    base_style = {
        "who_size": 55,                          # 名字字号
        "who_color": "#ffffff",                  # 名字颜色
        "who_outlines": [(1, "#1a3037", 0, 0)],  # 名字描边
        "what_size": 40,                         # 对话字号
        "what_color": "#fff",                    # 对话颜色,这个是角色说话的颜色,看你需要了 我不建议这里改,建议你自己赋值传入,除非你全部角色都是这个颜色那可以
        "what_outlines": [(1, "#1a3037", 0, 0)], # 对话描边,默认小黑边 很小的 字体会清晰一点立体
        "sub_name_size": -15,                    # 副名称字号（相对缩小）,结果字号就是who_size+sub_name_size
        "sub_name_color": "#88dbff",             # 副名称颜色,你不写sub_name那就不会显示的
        "suff": False,                           # 对话框后缀图片
    }









#═══════════════════════════════════════════════════════════════════════════════════#
# ── [DO NOT MODIFY] 以下为框架常量与运行状态 ──
#不知道为什么要这个请不要修改 会造成位置bug
    character_zoom = {}            # 角色身高数据容器，由角色定义文件填充格式: {image_tag: {"cm": 身高, "hat": 帽子虚高}}
    base_room = 0.6                # 立绘整体缩放比例（回退值，角色未在 character_zoom 中定义时使用）
    base_align = (0.5, 1.0)        # 立绘默认锚点（底部居中）
    MOVE_PRESETS = set(preset_map.keys())  # 预设位置名集合，用于自定义语句解析时的判断
    _last_pos = {}                 # 角色最后位置记录 {tag: (x, y)}，用于 move 语句计算起点
    _last_expr = {}                # 角色最后表情记录 {tag: attr}，用于表情记忆回退

#为了实现move shake不写参数和上次调用一致 做的拦截
init python:
    _original_renpy_show = renpy.show
    def _capture_renpy_show(name, *args, **kwargs):
        if isinstance(name, tuple):
            if len(name) > 1:
                _last_expr[name[0]] = ' '.join(name[1:])
        elif isinstance(name, str):
            parts = name.split()
            if len(parts) >= 2:
                _last_expr[parts[0]] = ' '.join(parts[1:])
        return _original_renpy_show(name, *args, **kwargs)
    renpy.show = _capture_renpy_show