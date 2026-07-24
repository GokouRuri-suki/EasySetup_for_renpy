# Requires: nothing (standalone, only import math)
# 依赖：无（可独立使用，仅 import math）
python early:
    import math

    class ShakeAnim:
        def __init__(self, dur, offset, axis):
            self.dur = dur
            self.offset = offset
            self.axis = axis
            self.total = dur * 6

        def __call__(self, trans, st, at):
            attr = self.axis + 'offset'
            if st > self.total:
                setattr(trans, attr, 0)
                return None
            dur, offset = self.dur, self.offset
            if st < dur:
                t = st / dur
                v = 0.5 - math.cos(math.pi * t) / 2.0
                setattr(trans, attr, -offset * v)
            elif st < dur * 3:
                t = (st - dur) / (dur * 2)
                v = 0.5 - math.cos(math.pi * t) / 2.0
                setattr(trans, attr, -offset + offset * 2 * v)
            elif st < dur * 5:
                t = (st - dur * 3) / (dur * 2)
                v = 0.5 - math.cos(math.pi * t) / 2.0
                setattr(trans, attr, offset - offset * 2 * v)
            else:
                t = (st - dur * 5) / dur
                v = 0.5 - math.cos(math.pi * t) / 2.0
                setattr(trans, attr, -offset * (1 - v))
            return 0

    class MoveAnim:
        def __init__(self, start_x, start_y, target_x, target_y, duration):
            self.start_x = start_x
            self.start_y = start_y
            self.target_x = target_x
            self.target_y = target_y
            self.duration = duration

        def __call__(self, trans, st, at):
            if self.duration == 0:
                trans.xpos = self.target_x
                trans.ypos = self.target_y
                return None
            if st > self.duration:
                trans.xpos = self.target_x
                trans.ypos = self.target_y
                return None
            t = st / self.duration
            v = 0.5 - math.cos(math.pi * t) / 2.0
            trans.xpos = self.start_x + (self.target_x - self.start_x) * v
            trans.ypos = self.start_y + (self.target_y - self.start_y) * v
            return 0

    class FadeInAnim:
        def __init__(self, duration, x, y):
            self.duration = duration
            self.x = x
            self.y = y

        def __call__(self, trans, st, at):
            if st >= self.duration:
                trans.xpos = self.x
                trans.ypos = self.y
                trans.alpha = 1.0
                return None
            trans.xpos = self.x
            trans.ypos = self.y
            trans.alpha = st / self.duration
            return 0