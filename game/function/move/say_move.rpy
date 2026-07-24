# Requires: 0_config.rpy (params), anims.rpy (MoveAnim)
# 依赖：0_config.rpy（参数配置）、anims.rpy（MoveAnim 动画类）
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

    def parse_say_move(lex):
        who = lex.simple_expression()
        cp = lex.checkpoint()
        text = lex.string()
        if text is not None:
            attr = None
        else:
            lex.revert(cp)
            attr = lex.word()
            text = lex.string()
        nxt = lex.match(r'[\w.]+')
        if nxt is None:
            return (who, attr, text, None, None, None)
        if nxt in MOVE_PRESETS:
            return (who, attr, text, nxt, None, lex.match(r'[\d.]+'))
        try:
            float(nxt)
            return (who, attr, text, nxt, lex.match(r'[\d.]+'), lex.match(r'[\d.]+'))
        except ValueError:
            return (who, attr, text, None, None, None)

    def exec_say_move(parsed):
        global _last_pos
        who_str, attr_str, text, x_or_preset, y_str, dur_str = parsed
        who = eval(who_str)
        tag = who.image_tag
        tx, ty = _resolve_position(x_or_preset, y_str)
        dur = float(dur_str) if dur_str else move_dur
        sx, sy = _last_pos.get(tag, start_pos)
        renpy.show(_get_img(tag, attr_str), at_list=[Transform(xpos=sx, ypos=sy, function=MoveAnim(sx, sy, tx, ty, dur))])
        _last_pos = {**_last_pos, tag: (tx, ty)}
        who(text)

    renpy.register_statement("say_move",
        parse=parse_say_move, execute=exec_say_move, predict=None)