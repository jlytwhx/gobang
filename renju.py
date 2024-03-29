import json
from algorithm import Algorithm


class Renju:
    def __init__(self):
        self.requests_data = []
        self.responses_data = []
        self.last_msg = None  # 上回合保存信息
        self._board = [[0 for _ in range(15)] for _ in range(15)]  # 创建15x15棋盘 0为空 1为黑棋 2为白棋
        self._my_color = 2  # 1为黑手 2为白手 默认黑手 每收到或者发出{-1,-1}请求后换手
        self._chess_flag = 1  # 棋子临时变量 1时下一步应为黑手 2时下一步为白手
        self._step = 1
        self._read_json()
        self._reload_data()

    def _read_json(self):
        """
        从json中读取数据
        :return:
        """
        full_input = json.loads(input())
        self.requests_data = full_input["requests"]  # [{'x':-1,'y':-1}]
        self.responses_data = full_input['responses']
        if 'data' in full_input:
            self.last_msg = full_input['data']

    def _reload_data(self):
        """
        从数据中恢复棋盘
        :return:
        """
        for i in range(len(self.responses_data)):
            my_input = self.requests_data[i]  # i回合我的输入
            my_output = self.responses_data[i]  # i回合我的输出
            self.place_at(my_input['y'], my_input['x'])
            self.place_at(my_output['y'], my_output['x'])
        self.place_at(self.requests_data[-1]['y'], self.requests_data[-1]['x'])

    def place_at(self, x: int, y: int):
        """
        安放棋子
        :param x:
        :param y:
        :return:
        """
        if x == -1 and y == -1:
            self._my_color = 1 if self._my_color == 2 else 2  # 交换颜色
            return
        if x == 255:
            return
        self._board[x][y] = self._chess_flag  # 下棋
        self._chess_flag = 1 if self._chess_flag == 2 else 2  # 更改棋子临时变量
        self._step += 1

    def analyse(self):
        lx = self.requests_data[-1]['y']
        ly = self.requests_data[-1]['x']
        x, y, data = Algorithm(self._board, self._step, self._my_color, self.last_msg).analyse([lx, ly])
        self.output(x, y, data)

    @staticmethod
    def output(x: int, y: int, msg: str = None):
        print(json.dumps({
            "response": {'x': y, 'y': x},
            "data": msg
        }))


if __name__ == '__main__':
    Renju().analyse()
