# Requires: 0_config.rpy (params, expression_map, character_zoom, base_room, base_align)
# 依赖：0_config.rpy（参数配置、表情映射表、角色数据容器、框架常量）

python early:
    import os
    _gamedir = config.gamedir

    def calc_zoom(path, tag):
        """计算角色立绘的缩放比例，使不同尺寸的立绘在屏幕上身高一致。

        Args:
            path: 图片文件路径
            tag: 角色 image_tag，用于查 character_zoom 中的身高数据
        Returns:
            缩放比例 float
        """
        if tag not in character_zoom:
            return base_room
        d = character_zoom[tag]
        w, h = renpy.image_size(path)
        body_h = h - d["hat"]
        return (d["cm"] * ppm) / body_h

    def _register_images(tag, dir_path, use_side):
        """批量注册角色立绘及其表情差分、侧头像。

        Args:
            tag: 角色图片标签（如 "kkn"）
            dir_path: 立绘目录路径（如 "../students/kokona/"）
            use_side: 是否同时注册侧头像
        """
        dir_path = dir_path.rstrip("/\\")
        base_name = dir_path.rsplit("/", 1)[-1].rsplit("\\", 1)[-1]
        ext = ".png"

        default_path = f"{dir_path}/{base_name}{ext}"

        # 默认立绘
        renpy.image(tag,
            Transform(default_path, anchor=(0.5, 1.0),
                        zoom=calc_zoom(default_path, tag)))

        # 表情差分 — 有文件用差分，没有用默认回退
        for keyword, code in expression_map.items():
            variant = f"{dir_path}/{base_name}_{keyword}{ext}"
            abs_variant = os.path.normpath(os.path.join(_gamedir, variant))
            img_path = variant if os.path.exists(abs_variant) else default_path
            renpy.image(f"{tag} {code}",
                Transform(img_path, anchor=(0.5, 1.0),
                            zoom=calc_zoom(img_path, tag)))

        # 侧头像 — 有文件才注册
        if use_side:
            side_default = f"{dir_path}/side/{base_name}{ext}"
            abs_side = os.path.normpath(os.path.join(_gamedir, side_default))
            if os.path.exists(abs_side):
                renpy.image(f"side {tag}",
                    Transform(side_default, xysize=(side_size, side_size),
                                anchor=(0.5, 0.5)))
            for keyword, code in expression_map.items():
                side_variant = f"{dir_path}/side/{base_name}_{keyword}{ext}"
                abs_sv = os.path.normpath(os.path.join(_gamedir, side_variant))
                if os.path.exists(abs_sv):
                    renpy.image(f"side {tag} {code}",
                        Transform(side_variant, xysize=(side_size, side_size),
                                    anchor=(0.5, 0.5)))

    

    def new(config):
        """创建角色 Character 对象。

        Args:
            config: 角色配置字典，支持以下键:
                name (str): 角色显示名
                sub_name (str): 副名称（可选）
                image_tag (str): 图片关联标签
                file (str): 立绘文件路径
                side (bool): 是否有侧头像
                who_size (int): 名字字号
                who_color (str): 名字颜色
                what_size (int): 对话字号
                what_color (str): 对话颜色
                who_outlines (list): 名字描边
                what_outlines (list): 对话描边
                sub_name_size (int): 副名称相对字号
                sub_name_color (str): 副名称颜色
                suff (bool): 对话框后缀图片
        Returns:
            Character 对象
        """
        name = config.get("name", "")
        sub_name = config.get("sub_name", "")
        image_tag = config.get("image_tag", "")

        file_path = config.get("file", "")
        if file_path:
            _register_images(image_tag, file_path, config.get("side", False))

        display_name = name
        if sub_name:
            sz = config.get("sub_name_size", base_style["sub_name_size"])
            cl = config.get("sub_name_color", base_style["sub_name_color"])
            display_name += '{size=' + str(sz) + '}' + \
                            '{color=' + cl + '}' + \
                            '  ' + sub_name + '{/color}{/size}'

        use_suff = config.get("suff", base_style["suff"])
        suffix = "{image=character_suff}" if use_suff else ""
        return Character(display_name,
                            who_size=config.get("who_size", base_style["who_size"]),
                            who_color=config.get("who_color", base_style["who_color"]),
                            what_size=config.get("what_size", base_style["what_size"]),
                            what_color=config.get("what_color", base_style["what_color"]),
                            what_outlines=config.get("what_outlines", base_style["what_outlines"]),
                            who_outlines=config.get("who_outlines", base_style["who_outlines"]),
                            image=image_tag,
                            what_suffix=suffix)