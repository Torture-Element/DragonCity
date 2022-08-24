import tkinter
import level

class Helper_window:
    def __init__(self):
        self.window = tkinter.Tk()

        # set window title
        self.window.title('Test Window')

        # set size and pos : size(300 * 100), pos(250, 150)
        self.window.geometry("300x100+250+150")

        # label text
        label = tkinter.Label(self.window,              # label in window
                                text = 'Hello, world',  # show text
                                bg = '#EEBB00',         # bg color
                                font = ('Arial', 12),   # font and size
                                width = 15, height = 2) # word tag size   
        label.pack() # default way to pos

        button = tkinter.Button(self.window,    # in window
                    text = 'test',              # display text on button
                    command = self.print_test)
        button.pack()

        # 標示文字
        label = tkinter.Label(self.window, text = '姓名')
        label.pack()

        # 輸入欄位
        self.entry = tkinter.Entry(self.window,     # 輸入欄位所在視窗
                        width = 20) # 輸入欄位的寬度
        self.entry.pack()

        # 按鈕
        button = tkinter.Button(self.window, text = "OK", command = self.onOK)
        button.pack()


    def run(self):
        # executed main func
        self.window.mainloop()
    
    def print_test(self):
        print('test')
    
    def onOK(self):
        print("Hello, {}.".format(self.entry.get()))

def Helper_window_run():
    gui = Helper_window()
    gui.run()