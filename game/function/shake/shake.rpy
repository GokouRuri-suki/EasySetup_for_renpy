# Requires: 0_config.rpy (params), anims.rpy (ShakeAnim)
# 依赖：0_config.rpy（参数配置）、anims.rpy（ShakeAnim 动画类）
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

    def parse_shake(lex):
        """解析 shake_x / shake_y 语句。

        Args:
            lex: Ren'Py 词法分析器对象
        Returns:
            (who, attr, dur, offset) 元组
        """
        who = lex.simple_expression()
        nxt = lex.word()
        if nxt is None:
            dur_str = lex.match(r'[\d.]+')
            if dur_str:
                return (who, None, dur_str, lex.match(r'[\d.]+'))
            return (who, None, None, None)
        try:
            float(nxt)
            return (who, None, nxt, lex.match(r'[\d.]+'))
        except:
            return (who, nxt, lex.match(r'[\d.]+'), lex.match(r'[\d.]+'))

    def exec_shake(parsed, axis):
        """执行震动动画（通用函数，由 execute_shake_x/y 调用）。

        Args:
            parsed: parse_shake 返回的元组 (who, attr, dur, offset)
            axis: 震动轴（'x' 或 'y'）
        """
        who_str, attr_str, dur_str, offset_str = parsed
        who = eval(who_str)
        tag = who.image_tag
        total = float(dur_str) if dur_str else shake_total
        dur = total / 6
        offset = int(offset_str) if offset_str else shake_offset
        _window_hide(None)
        renpy.show(_get_img(tag, attr_str), at_list=[Transform(function=ShakeAnim(dur, offset, axis))])
        renpy.pause(total)
        store._window = "auto"

    def execute_shake_x(parsed):
        """执行 shake_x 语句（x 轴震动）。

        Args:
            parsed: parse_shake 返回的元组
        """
        exec_shake(parsed, 'x')

    def execute_shake_y(parsed):
        """执行 shake_y 语句（y 轴震动）。

        Args:
            parsed: parse_shake 返回的元组
        """
        exec_shake(parsed, 'y')

    renpy.register_statement("shake_x",
        parse=parse_shake, execute=execute_shake_x, predict=None)
    renpy.register_statement("shake_y",
        parse=parse_shake, execute=execute_shake_y, predict=None)