import csv
import re
import copy

# Название файла с описанием машины Тьюринга
machine_description_filename = "TuringMachine.csv"
# Название файла с описанием функции переходов
delta_filename = "delta.csv"
# Название файла с входными словами
input_filename = "input.txt"

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
                        if len(transitions_list) > 0:
                            # Стираем скобки
                            for t in range(len(transitions_list)):
                                transitions_list[t] = transitions_list[t].replace('(', '')
                                transitions_list[t] = transitions_list[t].replace(')', '')
                            # Добавляем в функцию переходов
                            delta_func[(state, header[i])] = [t.split(',') for t in transitions_list]
    return delta_func

# Класс машины Тьюринга
class TuringMachine:
    def __init__(self, printInvalid=False):
        # Множество состояний
        self.Q = []
        # Входной алфавит
        self.Sigma = []
        # Ленточный алфавит
        self.Gamma = []
        # Функция переходов
        self.delta = dict()
        # Начальное состояние
        self.q0 = 'q0'
        # Пробельный символ
        self.B = 'B'
        # Множество допускающих состояний
        self.F = dict()
        # Печать недопустимых слов
        self.printInvalid = printInvalid

    # Запуск машины на заданном слове
    def launch(self, word, q, pos=0, transitions=[]):
        # Проверка, не вышли ли мы за пределы текущего слова
        if pos < 0:
            word = self.B + word
        elif pos >= len(word):
            word = word + self.B

        # Сохраним текущее состояние
        current_state = word[:pos] + f'({q})' + word[pos:]
        transitions = copy.deepcopy(transitions) + [current_state]

        # Если попали в допускающее состояние
        if q in self.F:
            print(' |- '.join(transitions) + ' OK!')
            return

        # Если попали в неописанное состояние
        if (q, word[pos]) not in self.delta:
            if self.printInvalid:
                print(' |- '.join(transitions) + ' Undefined')
            return

        # Если текущее состояние уже было
        if transitions.count(current_state) > 1:
            if self.printInvalid:
                print(' |- '.join(transitions) + ' Cycle')
            return

        # Прогоняем машину дальше на каждом из следующих состояний
        for state in self.delta[(q, word[pos])]:
            self.launch(word[:pos] + state[1] + word[pos + 1:], state[0], pos + 1 if state[2] == 'R' else pos - 1, transitions)



# Убирает фигурные скобкии в строке и разделяет по запятой
def format_input(s):
    s = s.replace('{', '')
    s = s.replace('}', '')
    s = s.split(',')
    return s


# Считать машину Тьюринга из файла
def read_machine(machine_fname, delta_fname):
    TM = TuringMachine()
    with open(machine_fname) as f:
        reader_obj = csv.reader(f, delimiter=';')
        for row_count, row in enumerate(reader_obj):
            if row_count != 0:
                TM.Q, TM.Sigma, TM.Gamma, _, TM.q0, TM.B, TM.F = [format_input(s) for s in row]
                TM.q0 = TM.q0[0]
                TM.B = TM.B[0]
                TM.delta = read_delta(delta_fname)
    return TM


if __name__ == '__main__':
    machine = read_machine(machine_description_filename, delta_filename)
    #machine.printInvalid = True
    with open(input_filename) as f:
        for word in f.readlines():
            word = word.strip()
            machine.launch(word, machine.q0)
            print()
    input()