from typing import List
import json


class Algorithm:
    def __init__(self, board, my_color, status=None):
        self.board = board  # 15x15棋盘
        self.my_color = my_color  # 我的颜色 1为黑棋 2为白棋
        if not status:
            self.score = [[self._get_position_score(x, y) for x in range(15)] for y in range(15)]
        else:
            self.score = [[0 for _ in range(15)] for _ in range(15)]
            self._load_status(json.loads(status))

    def _cal_score(self, line: str) -> List[int]:
        """
        计算得分
        :param line:五子
        :return:
        """
        if self.my_color == 2:  # 自己为白棋,按位取反
            my_line = ''.join([x if x == '0' else ('2' if x == '1' else '1') for x in line])
            other_line = line.replace('@', '1')
        else:  # 自己为黑棋
            my_line = line.replace('@', '1')
            other_line = ''.join([x if x == '0' else ('2' if x == '1' else '1') for x in line])
        score_table = {
            '11111': 100000,  # 己方获胜
            '011110': 10000,  # 活四
            '011112': 500,  # 眠四
            '211110': 500,
            '10111': 500,
            '11011': 500,
            '11101': 500,
            '01110': 200,  # 活三,
            '010110': 200,
            '011010': 200,
            '001112': 50,  # 眠三，
            '211100': 50,
            '010112': 50,
            '011012': 50,
            '211010': 50,
            '210110': 50,
            '10011': 50,
            '10101': 50,
            '2011102': 50,
            '00110': 5,  # 活二
            '01100': 5,
            '01010': 5,
            '010010': 5,
            '000112': 3,  # 眠二
            '001012': 3,
            '010012': 3,
            '211000': 3,
            '210100': 3,
            '210010': 3,
            '10001': 3,
            '2010102': 3,
            '2011002': 3,
            '2001102': 3,
            '2112': -5,  # 死棋
            '21112': -5,
            '211112': -5
        }
        max_my = 0
        max_other = 0
        for k, v in score_table.items():
            if not max_my and k in my_line:
                max_my = v
            if not max_other and k in other_line:
                max_other = v
            if all([max_other, max_my]):
                return [max_my, max_other]
        return [max_my, max_other]

    def _is_legal(self, x: int, y: int) -> bool:
        """
        判断落子是否合法
        """
        return self._is_on_board(x, y) and self.board[x][y] == 0

    def _is_on_board(self, x: int, y: int) -> bool:
        """
        判断落子是否在棋盘上
        """
        return 0 <= x < len(self.board) and 0 <= y < len(self.board)

    @staticmethod
    def _get_position_score(x, y):
        """
        计算位置分
        """
        line_position_score = [0, 1, 2, 3, 4, 5, 6, 7, 6, 5, 4, 3, 2, 1, 0]
        return min(line_position_score[x], line_position_score[y])

    def _get_move_score(self, move: List[int]):

        def cal_final_score(line_score):
            """
            计算最终得分
            :param line_score:
            :return:
            """
            double_score = 0
            score_dict = {}
            for score in line_score:
                if score not in score_dict:
                    score_dict[score] = 1
                else:
                    score_dict[score] += 1
            if 500 in score_dict and score_dict[500] == 2:  # 双冲四
                double_score = 10000
            elif 500 in score_dict and 200 in score_dict:  # 冲四活三
                double_score = 10000
            elif 200 in score_dict and score_dict[200] == 2:  # 双活三
                double_score = 5000
            elif 200 in score_dict and 50 in score_dict:  # 活三眠三
                double_score = 1000
            elif 5 in score_dict and score_dict[5] == 2:  # 双活二
                double_score = 100
            elif 5 in score_dict and 3 in score_dict:  # 活二眠二
                double_score = 10
            return max(double_score, max(line_score))

        my_line_score = []
        other_line_score = []
        for dx, dy in [(0, 1), (1, 0), (1, 1), (1, -1)]:
            x, y = move
            line = []
            x, y = x + dx, y + dy
            while self._is_on_board(x, y):
                line.append(str(self.board[x][y]))
                x, y = x + dx, y + dy
            line.insert(0, '@')
            x, y = move
            x, y = x - dx, y - dy
            while self._is_on_board(x, y):
                line.insert(0, str(self.board[x][y]))
                x, y = x - dx, y - dy
            my_score, other_score = self._cal_score(''.join(line))
            my_line_score.append(my_score)
            other_line_score.append(other_score)
        return cal_final_score(my_line_score) + cal_final_score(other_line_score) + self._get_position_score(move[0],
                                                                                                             move[1])

    def _save_status(self):
        score_list = []
        for x in range(15):
            for y in range(15):
                score_list.append(self.score[x][y])
        return json.dumps(score_list)

    def _load_status(self, score_list):
        for i in range(len(score_list)):
            x, y = divmod(i, 15)
            self.score[x][y] = score_list[i]

    def _cal_neighbor(self, x, y):
        for dx in range(-7, 7):
            for dy in range(-7, 7):
                nx, ny = x + dx, y + dy
                if self._is_legal(nx, ny):
                    self.score[nx][ny] = self._get_move_score([nx, ny])

    def analyse(self, x: int, y: int):
        """
        x,y为最后一手下的棋位置
        """
        max_position = (0, 0)
        max_score = 0
        for x in range(15):
            for y in range(15):
                if self._is_legal(x, y):
                    self.score[x][y] = self._get_move_score([x, y])
                else:
                    self.score[x][y] = -100
        # for line in self.score:
        #     print(line)

        # for x in range(15):
        #     for y in range(15):
        #         if not self._is_legal(x, y):
        #             continue
        #         if self.score[x][y] > max_score:
        #             max_position = (x, y)
        #             max_score = self.score[x][y]
        one_d_score = [self.score[x][y] for x in range(15) for y in range(15)]
        max_score = max(one_d_score)
        max_score_index = one_d_score.index(max_score)
        x, y = divmod(max_score_index, 15)
        return x, y, self._save_status()
