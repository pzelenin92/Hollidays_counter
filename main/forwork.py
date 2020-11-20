"""This script allows user to add data to .csv file by writing it with the keyboard.
Input format: Name, Holiday[, stop]. Output format: Name, HolidayCounter,
Holiday(0),...,Holiday(n)"""

import csv
import os


def dict_format(input_data, fileindir=False):
    """This function converts input data from [Name,Count, Holidays] to {Name:[Count,[Holidays]]}"""
    dict_output = {}

    if fileindir:
        locvar = 2

        def subs_func(dict_key):
            return int(dict_key[1])
    else:
        locvar = 1

        def subs_func(dict_key):
            return len(dict_key[1:])

    if len(input_data) != 0:
        for inp in input_data:
            if inp[0] in dict_output:
                dict_output[inp[0]][0] += 1
                dict_output[inp[0]][1].extend(a for a in inp[locvar:])
            else:
                dict_output[inp[0]] = [subs_func(inp), inp[locvar:]]
        if input_data == read_keyboard:
            print('dict_from_keyboard= ', dict_output)
        else:
            print('dict_from_csv= ', dict_output)
    else:
        if input_data == read_keyboard:
            print('dict_from_keyboard= ', dict_output, "Ни одного значения не введено")
        else:
            print('dict_from_csv= ', dict_output, "Ни одного значения не введено")
    return dict_output


def list_maker(dict_value):
    """This function uses inside list_format() function to make list=(Counter,Holidays)"""
    loc_list = []
    for j in dict_value:
        if isinstance(j, list):
            loc_list.extend(list_maker(j))
        else:
            loc_list.append(j)
    return loc_list


def func_merger(inp_dict_from_csv, inp_dict_from_keyboard):
    """This function merges two dictionaries. 1 dictionary was produced from keyboard input +
    1 dictionary was produced from data from .csv file"""
    loc_dict_merged = {}
    loc_dict_merged.update(inp_dict_from_csv)
    for key in inp_dict_from_keyboard:
        if key in loc_dict_merged:
            counter = loc_dict_merged[key][0] + inp_dict_from_keyboard[key][0]
            holidays = loc_dict_merged[key][1] + inp_dict_from_keyboard[key][1]
            loc_dict_merged[key] = [counter, holidays]
        else:
            loc_dict_merged[key] = inp_dict_from_keyboard[key]
    print('dict_merged= ', loc_dict_merged)
    return loc_dict_merged


def list_format(inp_dict):
    """This funcion produces nested lists from merged dictionary.
    These lists will be written to .csv file after"""
    loc_dict_to_list = []
    for key in inp_dict:
        listi = [key]
        # listi.append(i)
        listi.extend(list_maker(inp_dict[key]))
        loc_dict_to_list.append(listi)
    print("dict_to_list= ", loc_dict_to_list)
    return loc_dict_to_list


def write_to_csv(inp_filename, inp_dict_to_list):
    """This function writes header and nested lists to .csv file"""
    with open(inp_filename, 'w', newline='') as loc_testfile:
        writer = csv.writer(loc_testfile)
        header = ["Name", "Counter", "Holidays"]
        writer.writerow(header)
        for row in inp_dict_to_list:
            writer.writerow(row)


# 0 ввод новых данных с консоли и запись их для дальнейшей обработки
read_keyboard = []
print("введите новые значения в формате: "
      "'Имя, Праздник' через запятую затем нажмите enter. Когда закончите вводить наберите 'stop'")
while True:
    keyboard_input = input().split(',')
    for i in range(len(keyboard_input)):
        keyboard_input.insert(i, keyboard_input.pop(i).strip().lower())
    if 'stop' in keyboard_input:
        if len(keyboard_input) == 1:
            break
        if 'stop' in keyboard_input[:-1]:
            print("введен 'stop' не на последнем месте")
            continue
        if 'stop' in keyboard_input[-1]:
            if len(keyboard_input[:-1]) < 2:
                print("введено < 2 значений")
                continue
            read_keyboard.append(keyboard_input[:-1])
            break
    else:
        if len(keyboard_input) < 2:
            print("введено < 2 значений")
            continue
        read_keyboard.append(keyboard_input)
print('read_keyboard= ', read_keyboard)

# 1 обработка полученных данных - приведение к формату {Name:[count,[Holiday]]}
dict_from_keyboard = dict_format(read_keyboard)

# 2 проверка на наличие старого файла в текущей директории для сбора оттуда даты
FILENAME = "test1.csv"
if FILENAME in os.listdir():
    FILE_IN_DIR = True
    # 2.1 считываем файл который есть в директории
    with open("test1.csv", 'r', newline='') as testfile:
        reader = csv.reader(testfile)
        # 2.2 собираем дату в лист
        read_csv = []
        for rw in reader:
            k = []
            for i in rw:
                istrip = i.strip().lower()
                if istrip in ['name', 'counter', 'holidays']:
                    continue
                k.append(istrip)
            if k:
                read_csv.append(k)
        print('read_csv= ', read_csv)

    # 2.3 обработка полученных данных - приведение к формату {Name:[count,[Holiday]]}
    dict_from_csv = dict_format(read_csv, FILE_IN_DIR)

    # 2.4 merge словари в новый словать
    if len(dict_from_csv) != 0 and len(dict_from_keyboard) != 0:  # T and T -> T
        dict_merged = func_merger(dict_from_csv, dict_from_keyboard)
    elif len(dict_from_csv) != 0 or len(dict_from_keyboard) != 0:  # F or T -> T, T or F -> T
        if len(dict_from_csv) != 0:
            dict_merged = dict_from_csv
        else:
            dict_merged = dict_from_keyboard
    else:  # F or F -> F
        dict_merged = {}
        print('dict_merged= ', dict_merged, "Словари для merge были пустые")

    # 2.5 Преобразуем обратно из словаря во вложенные списки
    dict_to_list = list_format(dict_merged)

    # 2.6 перезапишем дату в файл
    if len(dict_to_list) != 0:
        write_to_csv(FILENAME, dict_to_list)
    else:
        print("Не было получено даты ни с консоли, ни с текстового файла")
else:
    # 1.1 преобразуем из словаря в списки
    dict_to_list = list_format(dict_from_keyboard)

    # 1.2 запишем дату в файл
    if len(dict_to_list) != 0:
        write_to_csv(FILENAME, dict_to_list)
    else:
        print("Не было получено даты с консоли")
