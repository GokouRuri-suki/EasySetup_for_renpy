# Requires: 0_config.rpy (params), anims.rpy (FadeInAnim)
# 依赖：0_config.rpy（参数配置）、anims.rpy（FadeInAnim 动画类）
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

    def parse_show_at(lex):
        """解析 show_at 语句。

        Args:
            lex: Ren'Py 词法分析器对象
        Returns:
            (who, attr, x_or_preset, y, dissolve_dur) 元组
        """
        who = lex.simple_expression()
        nxt = lex.match(r'[\w.]+')
        if nxt is None:
            return (who, None, None, None, None)
        if nxt in MOVE_PRESETS:
            return (who, None, nxt, None, lex.match(r'[\d.]+'))
        try:
            float(nxt)
            y = lex.match(r'[\d.]+')
            return (who, None, nxt, y, lex.match(r'[\d.]+'))
        except ValueError:
            attr = nxt
            nxt2 = lex.match(r'[\w.]+')
            if nxt2 is None:
                return (who, attr, None, None, None)
            if nxt2 in MOVE_PRESETS:
                return (who, attr, nxt2, None, lex.match(r'[\d.]+'))
            y = lex.match(r'[\d.]+')
            return (who, attr, nxt2, y, lex.match(r'[\d.]+'))

    def exec_show_at(parsed):
        """执行 show_at 语句，以淡入方式显示角色。

        Args:
            parsed: parse_show_at 返回的元组 (who, attr, x_or_preset, y, dissolve_dur)
        """
        global _last_pos
        who_str, attr_str, x_or_preset, y_str, dissolve_str = parsed
        who = eval(who_str)
        tag = who.image_tag
        tx, ty = _resolve_position(x_or_preset, y_str)
        dd = float(dissolve_str) if dissolve_str else dissolve_dur
        if dd > 0:
            renpy.show(_get_img(tag, attr_str), at_list=[Transform(xpos=tx, ypos=ty, function=FadeInAnim(dd, tx, ty))])
            if animation_skip_mode:
                if renpy.pause(dd):
                    renpy.show(_get_img(tag, attr_str), at_list=[Transform(xpos=tx, ypos=ty)])
            else:
                renpy.pause(dd, hard=True)
        else:
            renpy.show(_get_img(tag, attr_str), at_list=[Transform(xpos=tx, ypos=ty)])
        _last_pos = {**_last_pos, tag: (tx, ty)}

    renpy.register_statement("show_at",
        parse=parse_show_at, execute=exec_show_at, predict=None)