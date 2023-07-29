from tkinter import *
from tkinter import filedialog as fd
import Datebase_cleaner as dc
import Database_divider as dd
import bar_code_filler as bf

# design the window
window = Tk()
window.title("Nugary Pharms")
window.minsize(600, 400)
window.maxsize(600, 400)
window.config(bg='#07072D')

# Constants
WORD = "Let's clean your database"
NOTE = 'Done.!'  # ✔
REMOVED_ITEMS = []
NEW_LIST = []

call_back = ''


def change_text():
    # hide the notify label, after showing it for a specified period of time
    global call_back

    window.after_cancel(call_back)
    notify.grid(row=0, column=0, padx=280, pady=40)
    notify.configure(bg='#07072D', text='')


def invalid_column_name():
    # show error message when a column name of the inputted table
    # does not match with the set of column names in the code

    notify.grid_forget()
    notify.grid(row=0, column=0, padx=150, pady=40)
    notify.configure(bg='#07072D', text='column name does not exist', padx=10)


def invalid_format():
    # show error message when the user inputs a file format not .xlt,.xls,.xlsx

    notify.grid_forget()
    notify.grid(row=0, column=0, padx=200, pady=40)
    notify.configure(bg='#07072D', text='wrong file format', padx=2)


def run():
    # keep the app running, perform all necessary tasks here
    # call_back is used with the window_after method
    global call_back

    # returns the file-path of the selected file
    file_path = show_dialog()
    # displays the text "just wait" on the screen
    show_note()
    # this handles the error when the user selects a wrong file format
    try:
        """ checks the 'bar-code' column of the table, alters invalid inputs to make valid ones,
        takes 3 args:file-path, an empty list to store only altered values,
         an empty list to store all values after making alterations.
         this returns the altered table.
        """
        table = dc.bar_code_cleaner(file_path, REMOVED_ITEMS, NEW_LIST)
        print('0')
        """ checks for duplicated records in the 'name' column of the table, then in the 'code' column
            keeps one record, deletes the other entries and stores them in another table,
            this returns a tuple: the updated table and the list for deleted entries.
        """
        result = dc.duplicate_remover(table)

        # stores the updated table (this is a dataframe)
        updated_table = result[0]
        # the list for deleted entries (this is a dataframe)
        removed_words_table = result[1]
        # this takes the updated table and fills all empty cells in the 'bar-code' field,
        # then returns the updated table after editing it
        updated_table = bf.fill_all(updated_table)
        # this takes the updated table and creates a number of sub-tables
        savedir = fd.askdirectory(title="Save to")
        dd.section_rows(updated_table, savedir)
        # converts the dataframes to .csv files
        dir = f'{savedir}' + '/Maintable.csv'
        dir2 = f'{savedir}' + '/removed.csv'
        updated_table.to_csv(dir, mode='w', index=False)
        removed_words_table.to_csv(dir2, mode='w', index=False)

        # displays the notify label with a text informing the user of the completion of the job
        notify.configure(bg='#07072D', text=NOTE)
        # calls the change_text func to hide the notify label
        call_back = window.after(3000, change_text)

    except ValueError:
        invalid_format()
    except TypeError:
        invalid_format()
    except NameError:
        invalid_column_name()
    except KeyError:
        invalid_column_name()    


def show_dialog():
    # show file dialog box

    dialog = fd.askopenfile(title='select a file')

    return dialog.name


def show_note():
    # show the notify label, and display a text

    notify.configure(bg='#07072D', text='Just wait..')
    window.update()


# creates the notify label
notify = Label(window, bg='#07072D', fg='white', justify='center', font=("Arial", 18, "bold"))
notify.grid(row=0, column=0, padx=280, pady=40)

# creates the canvas for displaying the heading
label = Canvas(width=500, height=70, highlightthickness=0, bg='#07072D')
label_text_word = label.create_text(250, 50, text=WORD, justify="center", fill='white', font=("Arial", 24, "bold"))
label.grid(row=1, column=0, columnspan=3, padx=2, pady=5)

# creates the click button for running the task
button_click = Button(window, bg="green", fg='white', text="RUN TABLE CHECKER", border=0, overrelief=SUNKEN,
                      font=("Arial", 12, "bold"), command=run, width=25, height=2, relief="solid")
button_click.grid(row=2, column=0, columnspan=2, padx=50)

window.mainloop()
