from tkinter import *

app = Tk()

#Spider list
spider_label = Label(app, text="Choose a spider")
spider_label.grid(row=0, column=0, sticky=W, pady=10, padx=10)

spider_text = StringVar(app)
spider_text.set("Choose a spider")
spiders = ['spider 1', 'spider 2']

spider_dropdown = OptionMenu(app, spider_text, *spiders)
spider_dropdown.grid(row=0, column=1, columnspan=2)

#Feeder type
feed_label = Label(app, text="Choose a feed")
feed_label.grid(row=1, column=0, sticky=W, pady=10, padx=10)

feed_text = StringVar(app)
feed_text.set("Choose a feed")
feeds = ['feed 1', 'feed 2']

feed_dropdown = OptionMenu(app, feed_text, *feeds)
feed_dropdown.grid(row=1, column=1, columnspan=2)

#path
folder_path_text = StringVar(app)
folder_path_entry = Entry(app, textvariable=folder_path_text)
folder_path_entry.grid(row=2, column=0, padx=10, pady=10)

#data entry
data_path_text = StringVar(app)
data_path_entry = Entry(app, textvariable=data_path_text, width=10)
data_path_entry.grid(row=2, column=1, padx=10, pady=10)

browse_btn = Button(app, text='Browse')
browse_btn.grid(row=2, column=2)

execute_btn = Button(app, text='Execute')
execute_btn.grid(row=3, column=0, columnspan=3, pady=20)



app.title('Spider Executor')
app.geometry('300x200')
app.resizable(False,False)
app.mainloop()