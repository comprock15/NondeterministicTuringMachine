import csv
import re

# Название файла с описанием машины Тьюринга
machine_description_filename = "TuringMachine.csv"
# Название файла с описанием функции переходов
lambda_filename = "lambda.csv"


# Загрузить данные о функции переходов
def read_lambda(fname):
    with open(fname) as f:
        reader_obj = csv.reader(f, delimiter=';')
        header = []
        # Функция будет представлять собой словарь, в котором
        # ключами являются пары (состояние, символ),
        # значениями являются сами переходы в виде [состояние, символ, сдвиг]
        lambda_func = dict()
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
                        lambda_func[(state, header[i])] = [list(t.split(',')) for t in transitions_list]
            row_count += 1
    return lambda_func


if __name__ == '__main__':
    lambda_func = read_lambda(lambda_filename)
    print(lambda_func)