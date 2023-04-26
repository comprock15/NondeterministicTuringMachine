import csv
import re

# Название файла с описанием машины Тьюринга
machine_description_filename = "TuringMachine.csv"
# Название файла с описанием функции переходов
delta_filename = "delta.csv"


# Загрузить данные о функции переходов
def read_delta(fname):
    with open(fname) as f:
        reader_obj = csv.reader(f, delimiter=';')
        header = []
        # Функция будет представлять собой словарь, в котором
        # ключами являются пары (состояние, символ),
        # значениями являются сами переходы в виде [состояние, символ, сдвиг]
        delta_func = dict()
        # Смотрим все строки файла
        for row_count, row in enumerate(reader_obj):
            # Получаем список символов
            if row_count == 0:
                header = row
            # Получаем список переходов
            else:
                state = ''
                for i, transitions in enumerate(row):
                    # Получаем состояние
                    if i == 0:
                        state = transitions
                    else:
                        # Находим все состояния
                        transitions_list = re.findall(r'\(.*?\)', transitions)
                        # Стираем скобки
                        for t in range(len(transitions_list)):
                            transitions_list[t] = transitions_list[t].replace('(', '')
                            transitions_list[t] = transitions_list[t].replace(')', '')
                        # Добавляем в функцию переходов
                        delta_func[(state, header[i])] = [list(t.split(',')) for t in transitions_list]
    return delta_func


class TuringMachine:
    def __init__(self):
        self.Q = []
        self.Sigma = []
        self.Gamma = []
        self.delta = dict()
        self.q0 = 'q0'
        self.B = 'B'
        self.F = dict()


def format_input(s):
    s = s.replace('{', '')
    s = s.replace('}', '')
    s = list(s.split(','))
    return s

def read_machine(machine_fname, delta_fname):
    TM = TuringMachine()
    with open(machine_fname) as f:
        reader_obj = csv.reader(f, delimiter=';')
        for row_count, row in enumerate(reader_obj):
            if row_count != 0:
                TM.Q, TM.Sigma, TM.Gamma, _, TM.q0, TM.B, TM.F = [format_input(s) for s in row]
                TM.delta = read_delta(delta_fname)
    return TM


if __name__ == '__main__':
    machine = read_machine(machine_description_filename, delta_filename)