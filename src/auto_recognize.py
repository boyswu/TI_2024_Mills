"""
    missing_in_all_move：棋子识别数据中有，但实际棋局中没有的，两种情况。
    missing_in_color_move：实际棋局中有，但棋子识别数据中没有的
"""


def find_differences(color_move, all_move):
    all_move_set = set(all_move)
    print("实际棋局", all_move_set)
    # 从 color_move 中找到不在 one_dimensional_set 的数据
    color_move_set = set(row[0] for row in color_move)
    print("图像棋子", color_move_set)

    missing_in_all_move = color_move_set - all_move_set  # color_move(识别棋局) 中有，但 all_move(实际棋局) 中没有的
    print("改动后的棋子位置", missing_in_all_move)
    # 从 one_dimensional_set 中找到不在 color_move 的数据
    missing_in_color_move = all_move_set - color_move_set  # all_move 中有，但 color_move 中没有的
    print("被改动的棋子位置", missing_in_color_move)
    if len(missing_in_all_move) == 1:
        missing_in_all_move = int(missing_in_all_move.pop())  # 从集合中取出唯一元素并转换为整数
    else:
        missing_in_all_move = None  # 多个棋子被改动，无法确定被改动的位置
        print("无法确定被改动的棋子位置")
    # 转换为字符串
    missing_in_color_move = ', '.join(map(str, missing_in_color_move))
    return missing_in_all_move, missing_in_color_move
