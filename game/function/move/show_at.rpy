# Requires: 0_config.rpy (params), anims.rpy (FadeInAnim)
# 依赖：0_config.rpy（参数配置）、anims.rpy（FadeInAnim 动画类）
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

    def _resolve_position(x_or_preset, y_str):
        if x_or_preset in preset_map:
            return preset_map[x_or_preset]
        return float(x_or_preset), float(y_str)

    def parse_show_at(lex):
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
        global _last_pos
        who_str, attr_str, x_or_preset, y_str, dissolve_str = parsed
        who = eval(who_str)
        tag = who.image_tag
        tx, ty = _resolve_position(x_or_preset, y_str)
        dd = float(dissolve_str) if dissolve_str else dissolve_dur
        if dd > 0:
            renpy.show(_get_img(tag, attr_str), at_list=[Transform(xpos=tx, ypos=ty, function=FadeInAnim(dd, tx, ty))])
            renpy.pause(dd)
        else:
            renpy.show(_get_img(tag, attr_str), at_list=[Transform(xpos=tx, ypos=ty)])
        _last_pos = {**_last_pos, tag: (tx, ty)}

    renpy.register_statement("show_at",
        parse=parse_show_at, execute=exec_show_at, predict=None)