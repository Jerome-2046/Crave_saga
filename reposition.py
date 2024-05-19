"""
相对位置转换
以及常用区域
"""


def get_position(left: float, top: float, base_area: tuple):
    new_left = int(base_area[0] + left * base_area[2])
    new_top = int(base_area[1] + top * base_area[3])
    return new_left, new_top


def get_area(left: float, top: float, width: float, height: float, base_area: tuple):
    new_left = int(base_area[0] + left * base_area[2])
    new_top = int(base_area[1] + top * base_area[3])
    new_width = int(width * base_area[2])
    new_height = int(height * base_area[3])
    return new_left, new_top, new_width, new_height

# TODO area
# title_area = get_area(3, 88, 210, 38)
# small_title_area = get_area(0.35, 0.175, 0.65, 0.213)
# middel_title_area = get_area(0.35, 0.275, 0.65, 0.313)
