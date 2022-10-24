LETTERS = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя- ().abcdefghijklmnopqrstuvwxyz'
LETTERS = LETTERS + LETTERS.upper()
group_dict = {}
overall_score = 0
label = ''


def give_data(data):
    input_text = data
    convert_data_to_list(input_text)


def convert_data_to_list(data):
    data_list = []
    data_list += data.splitlines()
    for i in range(0, 5):
        while ' ' * i in data_list:
            data_list.remove(' ' * i)
    while True:
        if '.' in data_list:
            data_list.remove('.')
        else:
            break
    create_groups(data_list)


def create_groups(input_list):
    global group_dict
    group_list = []
    for line in input_list:
        if line[0] == '.':
            continue
        if len(line.strip(LETTERS)) == 0:
            group_dict[line] = 0
    for name in group_dict:
        group_list.append(name)
    save_indexes(group_dict, input_list, group_list)


def save_indexes(group_dict, input_list, group_list):
    index_list = []
    for group in group_dict:
        index = input_list.index(group)
        index_list.append(index)
    split_list(index_list, group_dict, input_list, group_list)


def split_list(index_list, group_dict, input_list, group_list):
    for i in range(0, len(index_list)):
        start = index_list[i]
        if i < len(index_list) - 1:
            stop = index_list[i + 1]
            saved_list = input_list[start + 1:stop]
        else:
            saved_list = input_list[start + 1:]
        group_dict[group_list[i]] = saved_list
    make_final_dict(group_dict)


def make_final_dict(group_dict):
    for group in group_dict:
        group_dict[group] = count_result(group_dict[group])
    count_overall_score(group_dict)
    create_label(group_dict)
    group_dict.clear()


def count_result(item_list):
    buffer_count = 0
    for el in item_list:
        if el[0] == '.':
            continue
        buffer_list = el.split(' ')
        if len(buffer_list) == 1 or not buffer_list[1].isdigit():
            buffer_count += check_value(buffer_list)
        else:
            buffer_count += int(buffer_list[1])
    return buffer_count


def count_overall_score(group_dict):
    global overall_score
    if overall_score > 0:
        overall_score = 0
    for group in group_dict:
        overall_score += int(group_dict[group])


def create_label(group_dict):
    global label
    if len(label) > 0:
        label = ''
    for group in group_dict:
        label += f'{group}: {group_dict[group]}\n'


def check_value(value):
    new_string = ''
    output_string = ''
    for i in value:
        new_string += i
    # ---------------------------ЕСЛИ РАЗМЕР ЧИСЛОВОЙ
    try:
        if new_string[0].isdigit() and new_string[1].isdigit():
            new_string = new_string[2:]
            print(new_string)
            for char in new_string:
                if char.isdigit():
                    output_string += char
                else:
                    return int(output_string)
    except IndexError:
        return 0
    # -----------------------------ЕСЛИ РАЗМЕР БУКВЕННЫЙ
    else:
        for i in range(0, len(new_string)):
            if i == 0 and new_string[i].isdigit():
                continue
            if new_string[i].isdigit():
                output_string += new_string[i]
            elif len(output_string) > 0:
                return int(output_string)
            else:
                continue
        try:
            return int(output_string)
        except ValueError:
            return 0
