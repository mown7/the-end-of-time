import tkinter as tk
from tkinter import font
from PIL import Image, ImageTk
import sys
import datetime


class MainProgramme:
    def __init__(self, root):
        self.root = root
        self.root.title("The End of Time（终焉之时）")
        self.root.attributes('-fullscreen', True)
        self.root.bind('<Escape>', lambda e: self.root.attributes('-fullscreen', False))

        
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        
        self.canvas = tk.Canvas(root, width = screen_width, height = screen_height, bg = "Black", highlightthickness = 0,bd = 0)
        self.canvas.pack()


        self.index = 0
        
        
        name = "screenshow.png"
        self.display_background(name)
        
        
        # UI元素初始化（在图片上层显示）
        self.initialize_ui_1()
        
        
        # 绑定关闭事件
        self.root.protocol("WM_DELETE_WINDOW", self.end_func)


        self.cursor_pos = 0
        self.cursor_visible = True
        self.active = False
        self.input_text_1 = ""
        self.blink_cursor()
        self.draw_content()

    
    def typing(self, bool__, text = None, x = None, y = None, color = None):
        if text is not None and bool__ == True:
            self.text = text


        if self.index < len(self.text):
            current_text = self.text[:self.index + 1]
            self.canvas.delete("text")
            self.text_id = self.canvas.create_text(x, y, text=current_text, font=("仿宋", 16, "bold"), fill = color, tags="text")
            self.index += 1


            with open("work_log.txt", 'a') as file_7:
                file_7.write(f"current index:{self.index}\ntext index:{len(self.text)}\n\n")


            if self.index == len(self.text):
                self.index = len(self.text) + 1
                bool__ = False


            self.root.after(100, lambda: self.typing(True, text, x, y, color))

    def display_background(self, photo_name):
        img = Image.open(photo_name)
        img = img.resize((self.root.winfo_screenwidth(), self.root.winfo_screenheight()))
        photo = ImageTk.PhotoImage(img)
        
            
        # 使用create_image绘制在底层
        self.canvas.create_image(0, 0, anchor=tk.NW, image=photo, tag = "bkgd")
        self.canvas.tag_lower("bkgd")
        self.background_photo = photo  # 保持引用
            
    
    def initialize_ui_1(self):
        sta_x = self.root.winfo_screenwidth() // 2
        
        
        # 创建文本（使用raise提升层级）
        self.canvas.create_text(sta_x, 50, text = "The End of Time", font = ("Arial", 50, "bold"), fill = "#FF99CC", state = tk.NORMAL)
        self.canvas.create_text(sta_x, 120, text = "终焉之时", font = ("明康欧楷", 50, "bold"), fill = "Gold", state = tk.NORMAL)
        self.canvas.create_rectangle(sta_x - 70, 575, sta_x + 70, 625, outline = '', stipple = 'gray50', tag = "start")
        self.canvas.create_rectangle(sta_x - 70, 575, sta_x + 70, 625, outline = '', fill = "Black")
        self.canvas.create_text(sta_x, 600, text = "开始游戏", font = ("明康欧楷", 20, "bold"), fill = "Red", state = tk.NORMAL)


        self.canvas.tag_raise("start")
        
        
        # 绑定按钮事件
        self.canvas.tag_bind("start", "<Button-1>", lambda e: self.start_game())

    
    def start_game(self):
        self.canvas.delete(tk.ALL)


        with open ("game_item_1.txt", 'r', encoding = 'utf-8') as file_1:
            art_1 = file_1.read()

        text_x = self.root.winfo_screenwidth() // 2
        text_y = self.root.winfo_screenheight() * 2 // 3
        self.typing(True, art_1, text_x, text_y, "White")

        self.root.after(8000, self.needing_func)

    def needing_func(self):
        self.canvas.create_rectangle(0, 0, self.root.winfo_screenwidth(), self.root.winfo_screenheight(), outline = '', stipple = 'gray50', tag = "go_on_1_PlayerName")


        self.canvas.tag_raise("go_on_1_PlayerName")


        self.canvas.tag_bind("go_on_1_PlayerName", "<Button-1>", lambda e: self.go_on_1_PlayerName())


    def on_click_1(self, event):
        self.active = True
        self.canvas.focus_set()
        self.cursor_pos = len(self.input_text_1)
        self.draw_content()


    def on_key_press(self, event):
        if not self.active or len(self.input_text_1) >= 5:
            return


        if event.char.isprintable():
            self.input_text_1 = (self.input_text_1[:self.cursor_pos] + event.char + self.input_text_1[self.cursor_pos:])
            self.cursor_pos += 1
            self.draw_content()


    def on_backspace(self, event):
        if not self.active or self.cursor_pos == 0:
            return


        self.input_text_1 = (self.input_text_1[:self.cursor_pos - 1] + self.input_text_1[self.cursor_pos:])
        self.cursor_pos -= 1
        self.draw_content()


    def draw_content(self):
        self.canvas.delete("dynamic_group")


        font_obj = font.Font(family="华文行楷", size=16)


        text_x = 520
        text_y = 270


        self.canvas.create_text(text_x, text_y, text = self.input_text_1, font=("华文行楷", 16), fill = "black",anchor = "w", tags = ("dynamic_text", "dynamic_group"))
        self.canvas.tag_raise("input_text")


        if self.active and self.cursor_visible:
            text_width = font_obj.measure(self.input_text_1[:self.cursor_pos])

            
            text_bbox = self.canvas.bbox("dynamic_text")
            x_pos = text_bbox[2] if text_bbox else text_x
            self.canvas.create_line(x_pos, text_y - 15, x_pos, text_y + 15, width = 2, fill = "red", tags = ("cursor", "dynamic_group"))


        if len(self.input_text_1) >= 5:
            self.canvas.create_text(550, 300, text = "MAX 5", anchor = "e", fill = "red", tags = "input_text")


    def blink_cursor(self):
        self.cursor_visible = not self.cursor_visible
        if self.active:
            self.draw_content()


        self.canvas.after(500, self.blink_cursor)


    def on_mouse_enter(self, event):
        self.canvas.config(cursor="xterm")


    def go_on_1_PlayerName(self):
        self.canvas.delete(tk.ALL)


        with open ("Player_Info.txt", 'r', encoding = 'utf-8') as file_3:
            PlayerInfo = file_3.read()


        if PlayerInfo == "":
            text_width = self.root.winfo_screenwidth() // 4
            text_height = self.root.winfo_screenheight() // 4
            recta_width = 515
            recta_height = 250
            

            
            self.text_PlayerInfo = self.canvas.create_text(text_width, text_height, text = "昵称：", font = ("楷体", 20), fill = "White", state = tk.NORMAL)
            self.recta_PlayerInfo = self.canvas.create_rectangle(recta_width, recta_height, recta_width + 100, recta_height + 40, fill = "#E6E6FA", outline = "#999")


            self.canvas.tag_bind(self.recta_PlayerInfo, "<Button-1>", self.on_click_1)
            self.canvas.bind_all("<Key>", self.on_key_press)
            self.canvas.bind_all("<BackSpace>", self.on_backspace)
            self.canvas.tag_bind(self.recta_PlayerInfo, "<Enter>", self.on_mouse_enter)


            StartGameRectaWidth = self.root.winfo_screenwidth() // 3 * 2
            StartGameRectaHeight = self.root.winfo_screenheight() // 3 * 2


            self.canvas.create_rectangle(StartGameRectaWidth, StartGameRectaHeight, StartGameRectaWidth + 164, StartGameRectaHeight + 64, fill = "#E6E6FA", outline = "Black")
            self.canvas.create_rectangle(StartGameRectaWidth, StartGameRectaHeight, StartGameRectaWidth + 164, StartGameRectaHeight + 64, outline = '', stipple = 'gray50', tag = "StorePlayerInfo")
            self.canvas.create_text(1362, 752, text = "进入第一章", font = ("楷体", 20), fill = "Red", state = tk.NORMAL)


            self.canvas.tag_bind("StorePlayerInfo", "<Button-1>", lambda e: self.StorePlayerInfo())


        else:
            StartGameRectaWidth = self.root.winfo_screenwidth() // 2
            StartGameRectaHeight = self.root.winfo_screenheight() // 2


            self.canvas.create_rectangle(StartGameRectaWidth - 50, StartGameRectaHeight - 25, StartGameRectaWidth + 50, StartGameRectaHeight + 25, outline = '', stipple = 'gray50', tag = "EnterChapterOne")
            self.canvas.create_text(StartGameRectaWidth, StartGameRectaHeight, text = "章节", font = ("楷体", 30), fill = "Red", state = tk.NORMAL)


            self.canvas.tag_raise("EnterChapterOne")
            self.canvas.tag_bind("EnterChapterOne", "<Button-1>", lambda e: self.ChooseChapter())


    def ChooseChapter(self):
        with open ("work_log.txt", 'a') as file_5:
            file_5.write("Player_Choose: Choose Chapter\n\n")

        
        self.canvas.delete(tk.ALL)

        
        C1W = self.root.winfo_screenwidth() // 7 * 2
        C1H = self.root.winfo_screenheight() // 7 * 2
        C2W = self.root.winfo_screenwidth() // 7 * 4
        C2H = self.root.winfo_screenheight() // 7 * 4
        C3W = self.root.winfo_screenwidth() // 7 * 6
        C3H = self.root.winfo_screenheight() // 7 * 6


        self.canvas.create_rectangle(C1W, C1H, C1W + 100, C1H + 60, fill = "#E6E6FA", outline = "Black")
        self.canvas.create_rectangle(C2W, C2H, C2W + 100, C2H + 60, fill = "#E6E6FA", outline = "Black")
        self.canvas.create_rectangle(C3W, C3H, C3W + 100, C3H + 60, fill = "#E6E6FA", outline = "Black")
        self.canvas.create_text(C1W + 50, C1H + 30, text = "第一章", font = ("楷体", 15), fill = "Black", state = tk.NORMAL)
        self.canvas.create_text(C2W + 50, C2H + 30, text = "第二章", font = ("楷体", 15), fill = "Black", state = tk.NORMAL)
        self.canvas.create_text(C3W + 50, C3H + 30, text = "第三章", font = ("楷体", 15), fill = "Black", state = tk.NORMAL)
        self.canvas.create_rectangle(C1W, C1H, C1W + 100, C1H + 60, outline = '', stipple = 'gray50', tag = "EnterChapterOne")
        self.canvas.create_rectangle(C2W, C2H, C2W + 100, C2H + 60, outline = '', stipple = 'gray50', tag = "EnterChapterTwo")
        self.canvas.create_rectangle(C3W, C3H, C3W + 100, C3H + 60, outline = '', stipple = 'gray50', tag = "EnterChapterThree")


        self.canvas.tag_bind("EnterChapterOne", "<Button-1>", lambda e : self.ChapterOne_1())
        self.canvas.tag_bind("EnterChapterTwo", "<Button-1>", lambda e : self.ChapterTwo_1())
        self.canvas.tag_bind("EnterChapterThree", "<Button-1>", lambda e : self.ChapterThree_1())


    def StorePlayerInfo(self):
        with open ("Player_Info.txt", 'w') as file_4:
            file_4.write(self.input_text_1)


        self.root.after(0, self.ChapterOne_1)


    def ChapterOne_1(self):
        self.canvas.delete(tk.ALL)


        with open ("work_log.txt", 'a') as file_8:
            file_8.write("Player_Choose: Chapter One\n\n")


        chapter_1_b1w = self.root.winfo_screenwidth()
        chapter_1_b1h = self.root.winfo_screenheight() // 3 * 2
        chapter_1_b1h_end = self.root.winfo_screenheight()
        self.canvas.create_rectangle(0, chapter_1_b1h, chapter_1_b1w, chapter_1_b1h_end, fill = "#E6E6FA", outline = "Black")


        with open ("Player_Info.txt", 'w+', encoding = 'utf-8') as file_5:
            Player_name = file_5.read()
            if len(Player_name) > 5:
                file_5.write("00000")
        self.canvas.create_rectangle(0, chapter_1_b1h - 50, 100, chapter_1_b1h, fill = "#AAFF00", outline = "Black")
        self.canvas.create_text(50, chapter_1_b1h - 25, text = f"{Player_name}", font = ("华文行楷", 15), fill = "Black", state = tk.NORMAL)


        with open("game_item_cp1_1.txt", 'r', encoding = 'utf-8') as file_6:
            Chapter_1_art_1 = file_6.read()
        Chapter_1_art_1w = self.root.winfo_screenwidth() // 2
        Chapter_1_art_1h = self.root.winfo_screenheight() // 3 * 2 + 200
        self.index = 0
        self.typing(True, Chapter_1_art_1, Chapter_1_art_1w, Chapter_1_art_1h, "Black")


    def ChapterTwo_1(self):
        with open ("work_log.txt", 'a') as file_9:
            file_9.write("Player_Choose: Chapter Two\n\n")


    def ChapterThree_1(self):
        with open ("work_log.txt", 'a') as file_10:
            file_10.write("Player_Choose: Chapter Three\n\n")


    def end_func(self):
        time_now = datetime.datetime.now()
        current_time = time_now.strftime("%Y-%m-%d %H:%M:%S")
        

        with open ("work_log.txt", 'a') as file_2:
            file_2.write(f"End time: {current_time}\n\n\n")
            
        
        self.root.destroy()
        sys.exit(0)


if __name__ == "__main__":
    main_root = tk.Tk()
    app = MainProgramme(main_root)
    main_root.mainloop()
