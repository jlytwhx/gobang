import json


class Renju:
    def __init__(self):
        self.requests_data = []
        self.responses_data = []
        self.last_msg = None
        self._read_json()
        self._reload_data()
        self._board = [[0 for _ in range(15)] for _ in range(15)]  # 创建15x15棋盘 0为空 1为黑棋 2为白棋

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
            print(my_input, my_output)

    def analyse(self):
        pass

    @staticmethod
    def output(x: int, y: int, msg: str = None):
        print(json.dumps({
            "response": {'x': x, 'y': y},
            "data": msg
        }))
