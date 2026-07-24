# Requires: 0_config.rpy (params), anims.rpy (MoveAnim + ShakeAnim)
# 依赖：0_config.rpy（参数配置）、anims.rpy（MoveAnim + ShakeAnim 动画类）
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

    def parse_move_shake(lex):
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

    def exec_move_shake(parsed):
        global _last_pos
        who_str, attr_str, direction, target = parsed
        who = eval(who_str)
        tag = who.image_tag
        tx, ty = _resolve_position(target, None)
        sx, sy = _last_pos.get(tag, start_pos)
        _window_hide(None)
        renpy.show(_get_img(tag, attr_str), at_list=[Transform(xpos=sx, ypos=sy, function=MoveAnim(sx, sy, tx, ty, combo_move_dur))])
        _last_pos = {**_last_pos, tag: (tx, ty)}
        renpy.pause(combo_move_dur)
        renpy.show(_get_img(tag, attr_str), at_list=[Transform(function=ShakeAnim(combo_shake_total/6, combo_shake_offset, direction))])
        renpy.pause(combo_shake_total)
        store._window = "auto"

    renpy.register_statement("move_shake",
        parse=parse_move_shake, execute=exec_move_shake, predict=None)

    def parse_say_move_shake(lex):
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

    def exec_say_move_shake(parsed):
        global _last_pos
        who_str, attr_str, text, direction, target = parsed
        who = eval(who_str)
        tag = who.image_tag
        tx, ty = _resolve_position(target, None)
        sx, sy = _last_pos.get(tag, start_pos)
        renpy.show(_get_img(tag, attr_str), at_list=[Transform(xpos=sx, ypos=sy, function=MoveAnim(sx, sy, tx, ty, combo_move_dur))])
        _last_pos = {**_last_pos, tag: (tx, ty)}
        renpy.pause(combo_move_dur)
        renpy.show(_get_img(tag, attr_str), at_list=[Transform(function=ShakeAnim(combo_shake_total/6, combo_shake_offset, direction))])
        who(text)

    renpy.register_statement("say_move_shake",
        parse=parse_say_move_shake, execute=exec_say_move_shake, predict=None)