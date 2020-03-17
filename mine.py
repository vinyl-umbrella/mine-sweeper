from tkinter import *
import random
import time

row_num=5       # row
column_num=5    # column
bomb_num=20     # number of bombs

class MainWindow:
    def __init__(self):
        self.__root=Tk()
        self.__root.title("Mine Sweeper")
        self.__root.resizable(0,0)
        self.menus()

        self.game=Game(self.__root)
        self.game.start()

    def menus(self):
        self.__menu=Menu(master=self.__root)
        file_menu=Menu(master=self.__menu,tearoff=0)
        file_menu.add_command(label="New Game",command=self.new_game)
        file_menu.add_command(label="Settings",command=self.options_window)
        file_menu.add_command(label="Exit",command=self.__root.destroy)
        self.__menu.add_cascade(label="Game", menu=file_menu)
        self.__root.config(menu=self.__menu)

    def new_game(self):
        self.game.restart()

    def options_window(self):
        options=Options(self.__root)
        options.start()

    def start(self):
        self.__root.mainloop()


class Game(Frame):
    def __init__(self,parent):
        Frame.__init__(self,master=parent)
        self.__parent=parent
        self.pack()

    def initialize(self):
        self.opened=[]
        self.flagged=[]
        self.create_frame()

    def create_frame(self):
        self.outer_frame=Frame(self,relief='groove',borderwidth=3,bg='lightgray')
        self.status_frame=Frame(self.outer_frame,height=50,relief='sunken', borderwidth=3, bg= 'lightgray')
        self.game_frame=Frame(self.outer_frame,relief='sunken',borderwidth=3, bg='lightgray')
        self.outer_frame.pack()
        self.status_frame.pack(padx=5,pady=5,fill='x')
        self.game_frame.pack(padx=5,pady=5)

        # spend time
        self.__time=timer(self.status_frame)
        self.__time.start()

        # reset button
        self.reset_button=Frame(self.status_frame,relief='raised',height=30,width=30, borderwidth=3, bg='lightgray')
        if ((35*column_num)/2)-30-40<0:
            self.reset_button.pack(side=LEFT)
        else:
            self.reset_button.pack(side=LEFT,padx=((35*column_num)/2)-30-40)

        self.reset_text=Label(self.reset_button,text='New Game', bg='lightgray',fg='black')
        self.reset_text.bind("<1>",self.click_reset_button)
        self.reset_text.pack()

        # create square
        i=0
        self.frame_list=[]
        for x in range(row_num):
            for y in range(column_num):
                self.frame=Frame(self.game_frame,width=35,height=35,bd=3, relief='raised',bg= 'lightgray')
                self.frame.bind("<1>",self.left_click)
                self.frame.bind("<2>",self.right_click)
                self.frame.num=i

                self.frame_list.append(self.frame)
                self.frame.grid(row=x,column=y)
                i+=1

        # set bombs
        self.bomb_list=[]
        while len(self.bomb_list)<bomb_num:
            bomb=random.randint(0,row_num*column_num-1)
            if bomb not in self.bomb_list:
                self.bomb_list.append(bomb)

        # remain bombs
        self.remain_bomb()

    def left_click(self,event):
        self.bomb_count=self.search_bomb(event.widget.num)
        if self.bomb_count==9:
            self.__time.stop()
            # all square which have bombs turn to be red
            for i in self.bomb_list:
                bomb_label=Label(self.frame_list[i],text='✹',bg='red')
                bomb_label.place(width=29,height=29)
            # cannot click all square
            for i in self.frame_list:
                i.bind("<1>",self.stop)
                i.bind("<2>",self.stop)
            lose_message=Label(self.outer_frame,text='You Lose',bg='lightgray')
            lose_message.pack()

        elif self.bomb_count==0:
            self.opened.append(event.widget.num)
            event.widget.configure(relief='flat',bg='#AAA')
            #周りをopen
            bomb_count_label=Label(event.widget, bg="lightgray", font=('Krungthep',16))
            bomb_count_label.place(width=33,height=33)
            event.widget.bind("<1>",self.stop)
            self.chain(event.widget.num)
        else:
            self.opened.append(event.widget.num)
            event.widget.configure(relief='flat',bg='#AAA')
            # assignment color
            bomb_count_label=self.num_color(event.widget,self.bomb_count)
            bomb_count_label.place(width=32,height=32)
            event.widget.bind("<1>",self.stop)
        self.win_game()

    def right_click(self,event):
        self.flagged.append(event.widget.num)
        flag_label=Label(event.widget,text='⚐',fg='blue',bg='lightgray')
        flag_label.place(width=28,height=28)
        flag_label.num=event.widget.num
        flag_label.bind("<2>",self.down_flag)
        self.__text.destroy()
        self.remain_bomb()

    def down_flag(self,event):
        self.flagged.remove(event.widget.num)
        event.widget.destroy()
        self.__text.destroy()
        self.remain_bomb()

    def chain(self,num):
        self.around(num)
        around=self.around_list
        for i in around:
            if i not in self.opened:
                self.opened.append(i)
                self.frame_list[i].configure(relief='flat',bg='#AAA')
                count=self.search_bomb(self.frame_list[i].num)
                if self.frame_list[i].num in self.flagged:
                    self.flagged.remove(self.frame_list[i].num)
                    self.__text.destroy()
                    self.remain_bomb()

                if count==0:
                    bomb_count_label=Label(self.frame_list[i], bg="lightgray", font=('Krungthep',16))
                    self.chain(i)
                else:
                    #色指定
                    bomb_count_label=self.num_color(self.frame_list[i],count)

                bomb_count_label.place(width=32,height=32)
                self.frame_list[i].bind("<1>",self.stop)

    def num_color(self,frame,num):
        if num==1:
            return Label(frame,text=num, bg="lightgray",fg='blue',font=('Krungthep',16))
        elif num==2:
            return Label(frame,text=num, bg="lightgray",fg='darkgreen',font=('Krungthep',16))
        elif num==3:
            return Label(frame,text=num, bg="lightgray",fg='red',font=('Krungthep',16))
        elif num==4:
            return Label(frame,text=num, bg="lightgray",fg='darkblue',font=('Krungthep',16))
        elif num==5:
            return Label(frame,text=num, bg="lightgray",fg='brown',font=('Krungthep',16))
        else:
            return Label(frame,text=num, bg="lightgray",fg='black',font=('Krungthep',16))

    def around(self,num):
        # 周囲のマスのnumを配列にする
        self.around_list=[]
        if num==0:
            # upper left
            self.around_list.append(num+1)
            self.around_list.append(num+column_num)
            self.around_list.append(num+column_num+1)
        elif num==column_num-1:
            # upper right
            self.around_list.append(num-1)
            self.around_list.append(num+column_num-1)
            self.around_list.append(num+column_num)
        elif num==(row_num-1)*column_num:
            # lower left
            self.around_list.append(num-column_num)
            self.around_list.append(num-column_num+1)
            self.around_list.append(num+1)
        elif num==row_num*column_num-1:
            # lower right
            self.around_list.append(num-column_num-1)
            self.around_list.append(num-column_num)
            self.around_list.append(num-1)
        elif num%column_num==0:
            # left column
            self.around_list.append(num-column_num)
            self.around_list.append(num-column_num+1)
            self.around_list.append(num+1)
            self.around_list.append(num+column_num)
            self.around_list.append(num+column_num+1)
        elif num%column_num==column_num-1:
            # right column
            self.around_list.append(num-column_num-1)
            self.around_list.append(num-column_num)
            self.around_list.append(num-1)
            self.around_list.append(num+column_num-1)
            self.around_list.append(num+column_num)
        elif num<column_num:
            # upper row
            self.around_list.append(num-1)
            self.around_list.append(num+1)
            self.around_list.append(num+column_num-1)
            self.around_list.append(num+column_num)
            self.around_list.append(num+column_num+1)
        elif num>column_num*(row_num-1):
            # lower row
            self.around_list.append(num-column_num-1)
            self.around_list.append(num-column_num)
            self.around_list.append(num-column_num+1)
            self.around_list.append(num-1)
            self.around_list.append(num+1)
        else:
            # surrounding 8 square
            self.around_list.append(num-column_num-1)
            self.around_list.append(num-column_num)
            self.around_list.append(num-column_num+1)
            self.around_list.append(num-1)
            self.around_list.append(num+1)
            self.around_list.append(num+column_num-1)
            self.around_list.append(num+column_num)
            self.around_list.append(num+column_num+1)

    def search_bomb(self,num):
        count=0
        if num in self.bomb_list :
            # if there is a bomb
            return 9

        self.around(num)
        for i in self.around_list:
            if i in self.bomb_list:
                count += 1
        return count

    def click_reset_button(self,event):
        self.restart()

    def remain_bomb(self):
        self.__text_var=StringVar()
        self.__text=Label(self.status_frame,font=('7barP',24),textvariable=self.__text_var, fg='red', bg='black')
        self.__text.pack(side=RIGHT)
        self.__count=bomb_num-len(self.flagged)
        self.__text_var.set(str(self.__count).zfill(2))

    def win_game(self):
        if (row_num*column_num)-len(self.opened)==bomb_num:
            self.__time.stop()
            for i in self.frame_list:
                i.bind("<1>",self.stop)
            win_message=Label(self.outer_frame,text='You Win',bg='lightgray')
            win_message.pack()

    def stop(self,event):
        pass

    def restart(self):
        self.outer_frame.destroy()
        self.start()

    def start(self):
        self.initialize()


class timer(Frame):
    def __init__(self, parent):
        Frame.__init__(self, master=parent)
        self.pack(side=LEFT)
        self.__text_var=StringVar()
        self.__text=Label(self,font=('7barP',24),textvariable=self.__text_var, fg='red', bg='black')
        self.__text.pack()
        self.__count=0
        self.__text_var.set(str(self.__count).zfill(3))
        self.__state=False

    def initialize(self):
        self.__state=True
        self.tic()

    def state(self):
        if self.__state:
            self.__state=False
        else:
            self.__state=True

    def tic(self):
        if self.__state:
            self.after(1000,self.count)

    def count(self):
        if self.__state:
            self.__count+=1
            self.__text_var.set(str(self.__count).zfill(3))
        self.tic()

    def start(self):
        self.initialize()

    def stop(self):
        self.state()


class Options(Toplevel):
    def  __init__(self,parent):
        Toplevel.__init__(self,master=parent)
        self.title("Settings")
        self.geometry('300x200')
        window=Frame(self)
        window.pack()
        self.box()

    def box(self):
        self.tate=StringVar()
        self.yoko=StringVar()
        self.baku=StringVar()

        label1=Label(self,text='vertical')
        label1.place(x=30, y=30)
        label2=Label(self,text='horizontal')
        label2.place(x=30, y=70)
        label3=Label(self,text='number of bombs')
        label3.place(x=30, y=110)

        box1=Entry(self,width=10,textvariable=self.tate)
        box1.place(x=150, y=30)
        box2=Entry(self,width=10,textvariable=self.yoko)
        box2.place(x=150, y=70)
        box3=Entry(self,width=10,textvariable=self.baku)
        box3.place(x=150, y=110)

        button1=Button(self,text='Done',command=self.change_status)
        button1.place(x=70,y=160)
        button2=Button(self,text='Cancel',command=self.destroy)
        button2.place(x=130,y=160)

    def change_status(self):
        global row_num
        global column_num
        global bomb_num

        if int(self.baku.get())==0 or (int(self.tate.get())*int(self.yoko.get())) <= int(self.baku.get()):
            self.start()
        else:
            row_num=int(self.tate.get())
            column_num=int(self.yoko.get())
            bomb_num=int(self.baku.get())
            self.destroy()

    def start(self):
        self.mainloop()


main=MainWindow()
main.start()
