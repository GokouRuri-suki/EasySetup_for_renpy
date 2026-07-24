# Requires: 0_config.rpy (params), anims.rpy (ShakeAnim)
# 依赖：0_config.rpy（参数配置）、anims.rpy（ShakeAnim 动画类）
python early:
    def _get_img(tag, attr):
        if attr:
            return tag + ' ' + attr
        try:
            sl = renpy.scene_lists()
            for layer in renpy.config.layers:
                for t, (attrs, zorder) in sl.showing.get(layer, {}).items():
                    if t == tag and attrs:
                        return tag + ' ' + ' '.join(attrs)
        except:
            pass
        return tag

    def parse_say_shake(lex):
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
        who_str, attr_str, text, dur_str, offset_str = parsed
        who = eval(who_str)
        tag = who.image_tag
        total = float(dur_str) if dur_str else shake_total
        dur = total / 6
        offset = int(offset_str) if offset_str else shake_offset
        renpy.show(_get_img(tag, attr_str), at_list=[Transform(function=ShakeAnim(dur, offset, axis))])
        who(text)

    def execute_say_shake_x(parsed):
        exec_say_shake(parsed, 'x')

    def execute_say_shake_y(parsed):
        exec_say_shake(parsed, 'y')

    renpy.register_statement("say_shake_x",
        parse=parse_say_shake, execute=execute_say_shake_x, predict=None)
    renpy.register_statement("say_shake_y",
        parse=parse_say_shake, execute=execute_say_shake_y, predict=None)