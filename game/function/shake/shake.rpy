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

    def parse_shake(lex):
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
        exec_shake(parsed, 'x')

    def execute_shake_y(parsed):
        exec_shake(parsed, 'y')

    renpy.register_statement("shake_x",
        parse=parse_shake, execute=execute_shake_x, predict=None)
    renpy.register_statement("shake_y",
        parse=parse_shake, execute=execute_shake_y, predict=None)