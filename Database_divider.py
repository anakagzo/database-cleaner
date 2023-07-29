def section_rows(table,savedir):
    # create sub tables each of 1000 records (maximum )
    no_of_rows = table.shape[0]
    no_of_colums = table.shape[1]
    groups = int(no_of_rows / 1000)
    rem_groups = int(no_of_rows % 1000)
    start_num = 0
    stop_num = 1000

    if no_of_rows > 1000:
        for num in range(groups):
            table_sect = table.iloc[start_num:stop_num, 0:no_of_colums]
            dir = f'{savedir}' + f'/table{num + 1}.csv'
            table_sect.to_csv(dir, mode='w', index=False)
            start_num = stop_num
            stop_num += 1000
        num = groups
        dir = f'{savedir}' + f'/table{num + 1}.csv'
        table_sect = table.iloc[start_num:, 0:no_of_colums]
        table_sect.to_csv(dir, mode='w', index=False)

    else:
        pass

