from typing import List


class Algorithm:
    def __init__(self, board, my_color):
        self.board = board  # 15x15棋盘
        self.my_color = my_color  # 我的颜色 1为黑棋 2为白棋
        self.score_dict = {
            'live_Five': 1000000,
            'live_Four': 100000,
            'sleep_Four': 10000,
            'live_Three': 1000,
            'live_Two': 100,
            'sleep_Three': 100,
            'live_One': 10,
            'sleep_Two': 10,
            'sleep_One': 1,
            'unknown': 0
        }

    def _is_legal(self, x: int, y: int) -> bool:
        """
        判断落子是否合法
        """
        return self._is_on_board(x, y) and self.board[x][y] != 0

    def _is_on_board(self, x: int, y: int) -> bool:
        """
        判断落子是否在棋盘上
        """
        return x < len(self.board) and y < len(self.board)

    def _get_position_all_line(self, position: List[int, int], color: int) -> List[List[int, List[int, int], List[bool, bool]]]:
        lines = []
        other_color = 1 if color == 2 else 2  # 对手颜色
        for direction in [[0, 1], [0, -1], [1, 1], [1, -1]]:
            dx, dy = direction
            count = 1  # 连星数
            jump_count = [0, 0]  # 顺、反方向跳开一个空格之后的连星数
            jump_flag = [False, False]  # 顺、反方向跳开一个空格的标志
            block = [False, False]  # 顺、反方向是否堵死
            for i, v in enumerate([1, -1]):  # 顺、反方向分别用1、-1表示
                dx, dy = v * dx, v * dy  # 步幅
                x, y = position[0] + dx, position[1] + dy  # 先走一步
                while True:
                    if not self._is_on_board(x, y) or self.board[x][y] != other_color:  # 不在棋盘内，或对方棋子
                        block[i] = True  # 被堵死
                        break
                    if not self.board[x][y]:  # 为空
                        if not self._is_on_board(x + dx, y + dy) or self.board[x + dx][y + dy] != color:
                            # 且下一格，不在棋盘内、或者非己方棋子
                            break
                        if jump_flag[i]:  # 前面已经跳了一格了，则终止
                            break  # 能力所限，不考虑又跳一格的情况！！！
                        else:
                            jump_flag[i] = True
                    elif self.board[x][y] == color:
                        if jump_flag[i]:
                            jump_count[i] += 1
                        else:
                            count += 1
                    x, y = x + dx, y + dy
                lines.append([count, jump_count, block])
        return lines

    def _get_position_score(self, x: int, y: int) -> int:
        pass
