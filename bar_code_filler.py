import random

fillers = ['a', 'b', 'c', 'o', 'p', 'q', 'r', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']


def get_filler():
    # generate a random string
    random.shuffle(fillers)
    filler = random.choice(fillers) + random.choice(fillers) + random.choice(fillers) + random.choice(
        fillers) + random.choice(fillers) + random.choice(fillers)
    return filler


def fill_all(table):
    # fill all empty cells in the 'bar-code' field

    new_table = table[table['Code'] == 'EMPTY_CELLS']
    index_list = new_table.index

    for num in index_list:
        # fill all Nan in 'bar-code' field with a random string
        filler = get_filler()
        table.loc[num, ['Code']] = filler

    return table
