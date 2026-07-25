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

    def parse_say_shake(lex):
        """解析 say_shake_x / say_shake_y 语句。

        Args:
            lex: Ren'Py 词法分析器对象
        Returns:
            (who, attr, text, dur, offset) 元组
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
        dur = lex.match(r'[\d.]+')
        offset = lex.match(r'[\d.]+')
        return (who, attr, text, dur, offset)

    def exec_say_shake(parsed, axis):
        """执行震动+说话动画（通用函数，由 execute_say_shake_x/y 调用）。

        Args:
            parsed: parse_say_shake 返回的元组 (who, attr, text, dur, offset)
            axis: 震动轴（'x' 或 'y'）
        """
        who_str, attr_str, text, dur_str, offset_str = parsed
        who = eval(who_str)
        tag = who.image_tag
        total = float(dur_str) if dur_str else shake_total
        dur = total / 6
        offset = int(offset_str) if offset_str else shake_offset
        renpy.show(_get_img(tag, attr_str), at_list=[Transform(function=ShakeAnim(dur, offset, axis))])
        who(text)

    def execute_say_shake_x(parsed):
        """执行 say_shake_x 语句（x 轴震动 + 说话）。

        Args:
            parsed: parse_say_shake 返回的元组
        """
        exec_say_shake(parsed, 'x')

    def execute_say_shake_y(parsed):
        """执行 say_shake_y 语句（y 轴震动 + 说话）。

        Args:
            parsed: parse_say_shake 返回的元组
        """
        exec_say_shake(parsed, 'y')

    renpy.register_statement("say_shake_x",
        parse=parse_say_shake, execute=execute_say_shake_x, predict=None)
    renpy.register_statement("say_shake_y",
        parse=parse_say_shake, execute=execute_say_shake_y, predict=None)