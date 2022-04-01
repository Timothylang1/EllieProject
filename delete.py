import tkinter as tk

root = tk.Tk()

enterButton = tk.Button(root, font = "Futura 16", text="first button",
                          relief = tk.RAISED, bd = 2)
enterButton.grid(row = 1, padx = 5, pady = 5)

enteButton = tk.Button(root, font = "Futura 16", text="second button",
                          relief = tk.RAISED, bd = 2)
enteButton.grid(row = 0, padx = 5, pady = 5)

# enteButton.grid(row = 2)

root.mainloop()