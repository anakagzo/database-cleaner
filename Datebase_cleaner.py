import pandas as pd
from bar_code_filler import get_filler

# CONSTANTS
REMOVED_ITEMS = []
NEW_LIST = []
# FILE_PATH = "C:/Users/Aghanya/Desktop/NugaryStock_File_Edited.xls"

REMOVED_WORDS = [
    ['Code', 'Name', 'Cost Price', 'Sales Price', 'Quantity', 'Alert Quantity', 
     'Category Code', 'Subcategory Code',
     'Unit Code', 'Sale Unit Code', 'Purchase Unit Code', 'Brand']]


# table = pd.read_excel("C:/Users/Aghanya/Desktop/NugaryStock_File_1V.xlt")


def bar_code_cleaner(file_path, removed_items, new_list):
    # remove invalid characters from the bar code of the table
    table = pd.read_excel(file_path)

    # fill all empty cells with 'NoData' 
    # (excluding 'Name','cost price','Code','quantity','alert quantity',
    #  'brand' columns)
    column_names = list(table.columns)
    for item in column_names:
        if str(item).strip().upper() not in ['NAME', 'CODE', 'SUBCATEGORY CODE',
                    'COST PRICE', 'QUANTITY', 'ALERT QUANTITY', 'BRAND'
                                             ]:
            table[item].fillna(value='None', inplace=True)
        elif str(item).strip().upper() == 'NAME':
            # strip all records in 'name' column
            stripped_column = table[item].str.strip()
            table[item] = stripped_column

            # make the words uppercase in 'name' column
            capitalize_column = table[item].str.upper()
            table[item] = capitalize_column
            
            # sort the table using the 'name' column
            table = table.sort_values(item).reset_index(drop=True)
            table.dropna(how='all', inplace=True)
            table[item].fillna(value='Empty cell', inplace=True)
            table.rename(columns={item: 'Name'}, inplace=True)
        elif str(item).strip().upper() == 'CODE': 
            # ensure the column name is correct: 
            # no whitespace and not case sensitive
            table.rename(columns={item: 'Code'}, inplace=True)
        else:
            pass
    
    part_no = table['Code'].tolist()

    # print(part_no)
    for item in part_no:
        # print(type(item))
        if type(item) == float:
            item = 'EMPTY CELLS'
        item = str(item)
        if not item.isalnum():

            removed_items.append(item)
            for i in item:
                if not i.isalnum() and i != '-' and i != '_':
                    item = (item.replace(i, '_'))
                    # print(i)
            new_list.append(item)
        else:
            new_list.append(item)
    # print((removed_items))
    # print(new_list)
    # print(len(new_list))

    new_list_frame = pd.DataFrame(new_list)
    table['Code'] = new_list_frame
    return table


def duplicate_remover(table):
    # remove all duplicates in the desc column, and store the deleted rows in another table
    # desc = table['desc'].tolist()
    # database = table.to_list()

    duplicates = table[table.duplicated(subset=['Name']) == True]
    table.drop_duplicates(subset=['Name'], inplace=True, ignore_index=True)

    duplicated_code = table[table.duplicated(subset=['Code']) == True]
    index_list = duplicated_code.index
    for num in index_list:
        # replace duplicate barcodes with a random string
        filler = get_filler() + get_filler()
        table.loc[num, ['Code']] = filler

    return table, duplicates


"""cleaned_table = bar_code_cleaner(FILE_PATH, REMOVED_ITEMS, NEW_LIST)
# database= table.tolist()
# print(database)
result = duplicate_remover(cleaned_table, REMOVED_WORDS, INDEX)
updated_table = result[0]
REMOVED_WORDS = result[1]
print(len(REMOVED_WORDS))
print(updated_table)
"""
# removed_words_frame = pd.DataFrame(REMOVED_WORDS)
# updated_table.to_csv("C:/Users/Aghanya/Desktop/sample.csv", mode='w', index=False)
# removed_words_frame.to_csv("C:/Users/Aghanya/Desktop/removed.csv", mode='w', index=False)
