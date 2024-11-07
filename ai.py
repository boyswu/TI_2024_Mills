import time

from connect_comd import connect, receive_feedback
from opencv_phone import opencv_phone
from auto_recognize import find_differences


def dis_board(board):
    # 显示出棋盘
    print("\t{} | {} | {}".format(board[0], board[1], board[2]))
    print("\t_ | _ | _")
    print("\t{} | {} | {}".format(board[3], board[4], board[5]))
    print("\t_ | _ | _")
    print("\t{} | {} | {}".format(board[6], board[7], board[8]))


def _moves(board):
    # 寻求可落子的位置
    moves = []
    for i in range(9):
        if board[i] in list("012345678"):  # 遍历了棋盘的位置如果位置为0-8那么这个位置可以落子
            moves.append(i)
    return moves


def computermove(board, computerletter, playerletter):
    # 核心算法：计算AI的落子位置
    boardcopy = board.copy()

    # 规则一：判断如果某位置落子可以获胜，则选择这个位置
    for move in _moves(boardcopy):
        boardcopy[move] = computerletter
        if winner(boardcopy):
            return move
        boardcopy[move] = str(move)

    # 规则二：某个位置玩家下一步落子就可以获胜，则选择该位置
    for move in _moves(boardcopy):
        boardcopy[move] = playerletter
        if winner(boardcopy):
            return move
        boardcopy[move] = str(move)

    # 规则三：按照中心、角、边的选择空的位置
    for move in (4, 0, 2, 6, 8, 1, 3, 5, 7):
        if move in _moves(board):
            return move


def winner(board):
    # 判断所给棋子是否获胜
    _to_win = {(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)}
    for r in _to_win:
        if board[r[0]] == board[r[1]] == board[r[2]]:
            return True
    return False


def Tie(board):
    # 判断是否平局
    for i in list("012345678"):
        if i in board:
            return False
    return True


def playermove(board, all_move):
    # 询问并确定玩家的选择落子位置，无效落子重复询问
    different_data = []

    while True:
        # 等待1.5秒
        time.sleep(1.5)
        color_move = opencv_phone()
        one_dimensional_set = set(all_move)

        if len(set(color_move)) < len(one_dimensional_set):
            continue
        # 遍历二维数组的第一列，查找不同的数据
        """
            找出人机下的棋子数据，后期检测人机下的棋子数据是否被修改
        """

        for row in color_move:
            if row[0] not in one_dimensional_set:
                # 清空集合
                different_data.clear()
                different_data.append(row[0])

        if len(different_data) == 0:
            # print("玩家没有选择有效落子的位置！")
            # 这里可以选择添加用户输入新的操作的提示
            continue  # 继续下一轮循环，重新检查可落子位置

        player_move = different_data[0]
        print("玩家落子位置:", different_data[0])

        if player_move in _moves(board):  # 检查move是否在可落子的位置中
            return player_move, color_move  # 如果有效，返回move


"""
    电脑下，无机械臂
"""

# def tic_tac_toe(all_move):
#     ai_move = []
#     while True:
#         color_move = opencv_phone()
#         if color_move is None or len(color_move) == 0:
#             # print("没有检测到棋子，请重新开始游戏！")
#             continue
#         playerletter = color_move[0][1]
#         print("玩家选择的棋子颜色：", playerletter)
#         # 井字棋
#         board = list("012345678")
#         if playerletter in "black":
#             turn = "player"
#             playerletter = "x"
#             computerletter = "o"
#         else:
#             turn = "AI"
#             computerletter = "x"
#             playerletter = "o"
#         print("{}先走！".format(turn))
#         # 建列表保存玩家落子位置
#
#         while True:
#             dis_board(board)
#             if turn == 'player':
#                 move, color_move = playermove(board, all_move)  # 询问并确定玩家的选择落子位置
#
#                 """
#                     判断人是否修改棋盘,改变了就返回数据，重新turn = 'player'
#                 """
#                 false_new_move, real_old_move = find_differences(color_move, all_move)
#
#                 if len(real_old_move) > 0 and len(false_new_move) > 0:
#                     print("人修改棋盘")
#                     # connect(real_old_move)
#                     # connect(false_new_move)
#                     continue
#                 all_move.append(move)
#
#                 board[move] = playerletter  # 落子
#                 if winner(board):
#                     dis_board(board)  # 显示出棋盘
#                     print("恭喜玩家获胜！")
#                     ai_move.clear()  # 清空ai_move列表
#                     # again = connect("again")  # 连接AI的落子位置
#                     # if again == "1":
#                     #     break
#                 else:
#                     turn = "AI"  # 切换到AI的回合
#             else:
#
#                 move = computermove(board, computerletter, playerletter)
#                 # connect(move)
#                 all_move.append(move)
#                 ai_move.append(move)  # 保存AI的落子位置
#                 print("人工智能AI落子位置：", move)
#                 board[move] = computerletter
#                 if winner(board):
#                     dis_board(board)
#                     print("人工智能AI获胜！")
#                     ai_move.clear()  # 清空ai_move列表
#                     # again = connect("again")  # 连接AI的落子位置
#                     # if again == "1":
#                     #     break
#                 else:
#                     turn = "player"
#             if Tie(board):
#                 dis_board(board)
#                 print('平局！')
#                 ai_move.clear()  # 清空ai_move列表
#                 # again = connect("again")  # 连接AI的落子位置
#                 # if again == "1":
#                 #     break
#         continue
"""
    带机械臂
"""


def tic_tac_toe(all_move):
    actions_white = ['o', 'p', 'q', 'r', 't']  # 定义动作列表
    actions_black = ['j', 'k', 'l', 'm', 'n']  # 定义动作列表
    actions_brought = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']  # 棋盘上已有的棋子位置

    action_index = 0  # 当前动作的索引

    while True:

        # 井字棋
        playerletter_1 = receive_feedback()
        print("playerletter_1选择的棋子颜色：", playerletter_1)
        color_move = opencv_phone()
        print("color_move:", color_move)
        if len(color_move) > 0:
            playerletter_2 = color_move[0][1]
        else:
            playerletter_2 = ""
        print("playerletter_2选择的棋子颜色：", playerletter_2)
        if len(playerletter_1) == 0 and len(playerletter_2) == 0:
            print("没有检测到棋子，请重新开始游戏！")
            continue

        board = list("012345678")
        if playerletter_1 == "again":
            return  # 结束游戏

        if playerletter_1 == "baiqi" or playerletter_2 == "black":  # baiqi：玩家先走，heiqi:AI先走
            turn = "player"
            playerletter = "x"
            computerletter = "o"
        if playerletter_1 == "heiqi":
            turn = "AI"
            computerletter = "x"
            playerletter = "o"
        print("{}先走！".format(turn))
        # 建列表保存玩家落子位置

        while True:
            dis_board(board)
            if turn == 'player':
                print("玩家")
                move, color_move = playermove(board, all_move)  # 询问并确定玩家的选择落子位置

                """
                    判断人是否修改棋盘,改变了就返回数据，重新turn = 'player'
                """
                false_new_move, real_old_move = find_differences(color_move, all_move)

                if false_new_move is not None and len(real_old_move) > 0:
                    print("人修改棋盘")
                    while True:
                        connect(actions_brought[false_new_move])  # 依次连接 actions_white 列表中的动作
                        receive_info = receive_feedback()
                        if receive_info.strip() == "again":
                            return  # 结束游戏
                        if receive_info.strip() == actions_brought[false_new_move].strip():
                            connect(real_old_move)
                            receive_info = receive_feedback()
                            if receive_info.strip() == "again":
                                return  # 结束游戏
                            if receive_info.strip() == real_old_move.strip():
                                break  # 接收到反馈信息，退出循环
                    continue
                all_move.append(move)
                board[move] = playerletter  # 落子
                if winner(board):
                    dis_board(board)  # 显示出棋盘
                    print("恭喜玩家获胜！")
                    return  # 结束游戏
                else:
                    turn = "AI"  # 切换到AI的回合
            else:
                print("AI正在思考中...")
                move = computermove(board, computerletter, playerletter)
                """
                玩家先走
                """
                if playerletter_1 == "baiqi" and playerletter_2 == "black":
                    while True:
                        connect(actions_white[action_index])  # 依次连接 actions_white 列表中的动作
                        receive_info = receive_feedback()
                        if receive_info.strip() == "again":
                            return  # 结束游戏
                        if receive_info.strip() == actions_white[action_index].strip():
                            action_index += 1  # 移动到下一个动作
                            connect(move)
                            print("AI落子位置：", move)
                            print(type(move))
                            receive_info = receive_feedback()
                            print("receive_info:", receive_info)
                            if receive_info.strip() == "again":
                                return  # 结束游戏
                            if receive_info.strip() == str(move).strip():
                                break  # 接收到反馈信息，退出循环
                            if action_index >= len(actions_white):  # 如果已经到达动作列表终点，重置索引
                                action_index = 0
                """
                     AI先走
                """
                if playerletter_1 == "heiqi":
                    while True:
                        connect(actions_black[action_index])  # 依次连接 actions_black 列表中的动作
                        receive_info = receive_feedback()
                        if receive_info.strip() == "again":
                            return  # 结束游戏
                        if receive_info.strip() == actions_black[action_index].strip():

                            action_index += 1  # 移动到下一个动作
                            connect(move)
                            receive_info = receive_feedback()
                            if receive_info.strip() == "again":
                                return  # 结束游戏

                            if receive_info.strip() == str(move).strip():
                                break  # 接收到反馈信息，退出循环
                            if action_index >= len(actions_black):  # 如果已经到达动作列表终点，重置索引
                                action_index = 0

                all_move.append(move)
                print("人工智能AI落子位置：", move)
                board[move] = computerletter
                if winner(board):
                    dis_board(board)
                    print("人工智能AI获胜！")
                    return  # 结束游戏
                else:
                    turn = "player"
            if Tie(board):
                dis_board(board)
                print('平局！')

                return
        continue
