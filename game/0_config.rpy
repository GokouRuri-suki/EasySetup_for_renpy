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
    combo_move_dur = 0.5          # 合体语句的移动时长（秒）
    combo_shake_total = 0.48      # 合体语句的震动总时长（秒）
    combo_shake_offset = 12       # 合体语句的震动振幅（像素）
    side_size = 273               # 侧头像尺寸（像素）
    ppm = 7.5                       # 像素每厘米（立绘缩放计算用） 
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
    character_zoom = {}            # 角色身高数据容器（由角色定义文件填充）
    base_room = 0.6                # 立绘整体缩放比例
    base_align = (0.5, 1.0)        # 立绘默认锚点（底部居中）
    MOVE_PRESETS = set(preset_map.keys())
    _last_pos = {}