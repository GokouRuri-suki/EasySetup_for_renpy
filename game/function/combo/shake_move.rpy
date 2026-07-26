# Requires: 0_config.rpy (params), anims.rpy (MoveAnim + ShakeAnim)
# 依赖：0_config.rpy（参数配置）、anims.rpy（MoveAnim + ShakeAnim 动画类）
python early:
    def _get_img(tag, attr):
        """根据角色标签和表情代码构造图片名称。

        Args:
            tag: 角色图片标签
            attr: 表情代码（如 'n'、'h'），为 None 时使用上次记录的表情
        Returns:
            图片名称字符串（如 "kkn n"）
        """
        if attr:
            _last_expr[tag] = attr
            return tag + ' ' + attr
        last = _last_expr.get(tag)
        if last:
            return tag + ' ' + last
        return tag

    def _resolve_position(x_or_preset, y_str):
        """解析位置参数，支持预设名或数值坐标。

        Args:
            x_or_preset: x 坐标值或预设名（如 'to_left'）
            y_str: y 坐标值（字符串），x_or_preset 为预设名时可传 None
        Returns:
            (float, float) 坐标元组
        """
        if x_or_preset in preset_map:
            return preset_map[x_or_preset]
        return float(x_or_preset), float(y_str)

    def parse_shake_move(lex):
        """解析 shake_move 语句（先震动后移动）。

        Args:
            lex: Ren'Py 词法分析器对象
        Returns:
            (who, attr, direction, target) 元组
        """
        who = lex.simple_expression()
        direction = 'x'
        target = None
        attr = None
        for _ in range(3):
            tok = lex.word()
            if tok is None:
                break
            if tok in ('x', 'y'):
                direction = tok
            elif tok in MOVE_PRESETS:
                target = tok
            else:
                attr = tok
        return (who, attr, direction, target)

    def exec_shake_move(parsed):
        """执行 shake_move 语句：先在原地震动，再移动到目标位置。

        Args:
            parsed: parse_shake_move 返回的元组 (who, attr, direction, target)
        """
        global _last_pos
        who_str, attr_str, direction, target = parsed
        who = eval(who_str)
        tag = who.image_tag
        tx, ty = _resolve_position(target, None)
        sx, sy = _last_pos.get(tag, start_pos)
        _window_hide(None)
        renpy.show(_get_img(tag, attr_str), at_list=[Transform(function=ShakeAnim(combo_shake_total/6, combo_shake_offset, direction))])
        if animation_skip_mode:
            if renpy.pause(combo_shake_total):
                renpy.show(_get_img(tag, attr_str))
        else:
            renpy.pause(combo_shake_total, hard=True)
        renpy.show(_get_img(tag, attr_str), at_list=[Transform(xpos=sx, ypos=sy, function=MoveAnim(sx, sy, tx, ty, combo_move_dur))])
        _last_pos = {**_last_pos, tag: (tx, ty)}
        if animation_skip_mode:
            if renpy.pause(combo_move_dur):
                renpy.show(_get_img(tag, attr_str), at_list=[Transform(xpos=tx, ypos=ty)])
        else:
            renpy.pause(combo_move_dur, hard=True)
        store._window = "auto"

    renpy.register_statement("shake_move",
        parse=parse_shake_move, execute=exec_shake_move, predict=None)

    def parse_say_shake_move(lex):
        """解析 say_shake_move 语句（震动 + 移动 + 说话）。

        Args:
            lex: Ren'Py 词法分析器对象
        Returns:
            (who, attr, text, direction, target) 元组
        """
        who = lex.simple_expression()
        cp = lex.checkpoint()
        text = lex.string()
        if text is not None:
            attr = None
        else:
            lex.revert(cp)
            attr = lex.word()
            text = lex.string()
        direction = 'x'
        target = None
        for _ in range(2):
            tok = lex.word()
            if tok is None:
                break
            if tok in ('x', 'y'):
                direction = tok
            elif tok in MOVE_PRESETS:
                target = tok
        return (who, attr, text, direction, target)

    def exec_say_shake_move(parsed):
        """执行 say_shake_move 语句：先震动，再移动，然后说话。

        Args:
            parsed: parse_say_shake_move 返回的元组 (who, attr, text, direction, target)
        """
        global _last_pos
        who_str, attr_str, text, direction, target = parsed
        who = eval(who_str)
        tag = who.image_tag
        tx, ty = _resolve_position(target, None)
        sx, sy = _last_pos.get(tag, start_pos)
        renpy.show(_get_img(tag, attr_str), at_list=[Transform(function=ShakeAnim(combo_shake_total/6, combo_shake_offset, direction))])
        if animation_skip_mode:
            if renpy.pause(combo_shake_total):
                renpy.show(_get_img(tag, attr_str))
        else:
            renpy.pause(combo_shake_total, hard=True)
        renpy.show(_get_img(tag, attr_str), at_list=[Transform(xpos=sx, ypos=sy, function=MoveAnim(sx, sy, tx, ty, combo_move_dur))])
        _last_pos = {**_last_pos, tag: (tx, ty)}
        if animation_skip_mode:
            if renpy.pause(combo_move_dur):
                renpy.show(_get_img(tag, attr_str), at_list=[Transform(xpos=tx, ypos=ty)])
        else:
            renpy.pause(combo_move_dur, hard=True)
        who(text)

    renpy.register_statement("say_shake_move",
        parse=parse_say_shake_move, execute=exec_say_shake_move, predict=None)