from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import random

root=Tk()
root.title("Сапёр")
root.config(bg="#FFFFFF")
def menu_root():
    root.geometry("300x300")
    lst = root.place_slaves()
    for l in lst:
        l.destroy()
    start_button=Button(text="Начать игру",bg="#00DA00",fg="#FFFFFF",font="20",command=choose_level)
    start_button.place(x=100,y=170)
    menu_label=Label(text="Добро пожаловать в игру 'Сапёр'!",font="15",bg="#FFFFFF")
    menu_label.place(x=25,y=80)
def choose_level():
    lst=root.place_slaves()
    for l in lst:
        l.destroy()
    choose_label=Label(text="Выберите сложность:",font="10",bg="#FFFFFF")
    choose_label.place(x=25,y=50)
    easy=lambda x="Лёгкая":restart(x)
    button_easy=Button(text="Лёгкая",font="20",command=easy)
    button_easy.place(x=25,y=90)
    medium=lambda x="Средняя":restart(x)
    button_medium=Button(text="Средняя",font="20",command=medium)
    button_medium.place(x=25,y=140)
    hard=lambda x="Сложная":restart(x)
    button_hard=Button(text="Сложная",font="20",command=hard)
    button_hard.place(x=25,y=190)
def restart(a):
    global buttons_alive,buttons,game,label,n,time,label_time,width,height,state,flag_using,flag_using1,flag_count,help_using,help_using1,help_count
    lst=root.place_slaves()
    for l in lst:
        l.destroy()

    state=a

    if a=="Лёгкая":
        n=25
        width=10
        help_count=IntVar()
        help_count.set(10)
        height=13
    elif a=="Средняя":
        n=99
        width=20
        help_count=IntVar()
        help_count.set(20)
        height=26
    else:
        n=223
        width=30
        help_count=IntVar()
        help_count.set(30)
        height=39

    game=[0]*height
    for i in range(height):
        game[i]=[0]*width

    root.geometry(str(width*20)+"x"+str(height*20 + 100))

    help_using=IntVar(0)
    help_using1=0
    help=Checkbutton(text="Подсказка",variable=help_using)
    help.place(x=10,y=height*20+60)
    help_label=Label(textvariable=help_count)
    help_label.place(x=width*20-40,y=height*20+60)

    flag_using1=int()
    flag_using=IntVar(0)
    flag=Checkbutton(text="Ставить флажок",variable=flag_using)
    flag.place(x=10,y=height*20+10)

    flag_count=IntVar()

    flag_count.set(n)

    flag_label=Label(textvariable=flag_count)
    flag_label.place(x=width*20-40,y=height*20+10)

    while n>0:
        x=random.randint(0,height-1)
        y=random.randint(0,width-1)
        if game[x][y]==0:
            game[x][y]=-1
            n-=1

    for i in range(height):
        for j in range(width):
            if game[i][j]!=-1:
                if i>0:
                    if game[i-1][j]==-1:
                        game[i][j]+=1
                    if j>0:
                        if game[i-1][j-1]==-1:
                            game[i][j]+=1
                    if j<width-1:
                        if game[i-1][j+1]==-1:
                            game[i][j]+=1
                if i<height-1:
                    if game[i+1][j]==-1:
                        game[i][j]+=1
                    if j>0:
                        if game[i+1][j-1]==-1:
                            game[i][j]+=1
                    if j<width-1:
                        if game[i+1][j+1]==-1:
                            game[i][j]+=1
                if j>0:
                    if game[i][j-1]==-1:
                        game[i][j]+=1
                if j<width-1:
                    if game[i][j+1]==-1:
                        game[i][j]+=1

    for i in range(height):
        for j in range(width):
            print(game[i][j],end=" ")
        print()

    for i in range(height):
        for j in range(width):
            if game[i][j]==-1:
                load=Image.open("techies.png")
                render=ImageTk.PhotoImage(load)
                label=Label(image=render)
                label.image=render
                label.place(x=j*20,y=i*20,width=20,height=20)

    buttons_alive=[1]*height
    for i in range(height):
        buttons_alive[i]=[1]*width

    for i in range(height):
        for j in range(width):
            if game[i][j]==-1:
                buttons_alive[i][j]=-1

    buttons=[""]*height
    for i in range(height):
        buttons[i]=[""]*width

    for i in range(height):
        for j in range(width):
            deleting=lambda x=i,y=j:delete_button(x,y)
            buttons[i][j]=Button(command=deleting,bg="#DCDCDC")
            buttons[i][j].place(x=j*20,y=i * 20,width=20,height=20)
def hide_bombs():
    global buttons,buttons_alive,height,width
    for i in range(height):
        for j in range(width):
            if (buttons_alive[i][j]!=0)and(buttons_alive[i][j]%10==0):
                buttons[i][j].config(bg="#DCDCDC")
                buttons_alive[i][j]//=10
def show_bombs(x,y):
    global buttons,buttons_alive,height,width
    if x>0:
        if buttons_alive[x-1][y]!=0:
            buttons_alive[x-1][y]*=10
            buttons[x-1][y].config(bg="#FF0000")
        if (y>0)and(buttons_alive[x-1][y-1]!=0):
            buttons_alive[x-1][y-1]*=10
            buttons[x-1][y-1].config(bg="#FF0000")
        if (y<width-1)and(buttons_alive[x-1][y+1]!=0):
            buttons_alive[x-1][y+1]*=10
            buttons[x-1][y+1].config(bg="#FF0000")
    if x<height-1:
        if buttons_alive[x+1][y]!=0:
            buttons_alive[x+1][y]*=10
            buttons[x+1][y].config(bg="#FF0000")
        if (y>0)and(buttons_alive[x+1][y-1]!=0):
            buttons_alive[x+1][y-1]*=10
            buttons[x+1][y-1].config(bg="#FF0000")
        if (y<width-1)and(buttons_alive[x+1][y+1]!=0):
            buttons_alive[x+1][y+1]*=10
            buttons[x+1][y+1].config(bg="#FF0000")
    if (y>0)and(buttons_alive[x][y-1]!=0):
        buttons_alive[x][y-1]*=10
        buttons[x][y-1].config(bg="#FF0000")
    if (y<width-1) and (buttons_alive[x][y + 1]!=0):
        buttons_alive[x][y+1]*=10
        buttons[x][y+1].config(bg="#FF0000")
def click_number(x,y):
    global game,buttons,buttons_alive,height,width,flag_using1,flag_using,help_using1,help_using
    hide_bombs()
    count=int()
    help_using1=-1

    if x>0:
        if buttons_alive[x-1][y]==-2or(game[x-1][y]==-1and buttons_alive[x-1][y]==0):
            count+=1
        if (y>0)and(buttons_alive[x-1][y-1]==-2or(game[x-1][y-1]==-1and buttons_alive[x-1][y-1]==0)):
            count+=1
        if (y<width-1)and(buttons_alive[x-1][y+1]==-2or(game[x-1][y+1]==-1and buttons_alive[x-1][y+1]==0)):
            count+=1
    if x<height-1:
        if buttons_alive[x+1][y]==-2or(game[x+1][y]==-1and buttons_alive[x+1][y]==0):
            count+=1
        if (y>0)and(buttons_alive[x+1][y-1]==-2or(game[x+1][y-1]==-1and buttons_alive[x+1][y-1]==0)):
            count+=1
        if (y<width-1)and(buttons_alive[x+1][y+1]==-2or(game[x+1][y+1]==-1and buttons_alive[x+1][y+1]==0)):
            count+=1
    if (y>0)and(buttons_alive[x][y-1]==-2or(game[x][y-1]==-1and buttons_alive[x][y-1]==0)):
        count+=1
    if (y<width-1)and(buttons_alive[x][y+1]==-2or(game[x][y+1]==-1and buttons_alive[x][y+1]==0)):
        count+=1

    if count==game[x][y]:
        if x>0:
            if (buttons_alive[x-1][y]!=0)and(buttons_alive[x-1][y]!=-2):
                if flag_using.get()==1:
                    flag_using1=-1
                delete_button(x-1,y)
                flag_using1=0
            if (y>0)and(buttons_alive[x-1][y-1]!=0)and(buttons_alive[x-1][y-1]!=-2):
                if flag_using.get()==1:
                    flag_using1=-1
                delete_button(x-1,y-1)
                flag_using1=0
            if (y<width-1)and(buttons_alive[x-1][y+1]!=0)and(buttons_alive[x-1][y+1]!=-2):
                if flag_using.get()==1:
                    flag_using1=-1
                delete_button(x-1,y+1)
                flag_using1=0
        if x<height-1:
            if (buttons_alive[x+1][y]!=0)and(buttons_alive[x+1][y]!=-2):
                if flag_using.get()==1:
                    flag_using1=-1
                delete_button(x+1,y)
                flag_using1=0
            if (y>0)and(buttons_alive[x+1][y-1]!=0)and(buttons_alive[x+1][y-1]!=-2):
                if flag_using.get()==1:
                    flag_using1=-1
                delete_button(x+1,y-1)
                flag_using1=0
            if (y<width-1)and(buttons_alive[x+1][y+1]!=0)and(buttons_alive[x+1][y+1]!=-2):
                if flag_using.get()==1:
                    flag_using1=-1
                delete_button(x+1,y+1)
                flag_using1=0
        if (y>0)and(buttons_alive[x][y-1]!=0)and(buttons_alive[x][y-1]!=-2):
            if flag_using.get()==1:
                flag_using1=-1
            delete_button(x,y-1)
            flag_using1=0
        if (y<width-1)and(buttons_alive[x][y+1]!=0)and(buttons_alive[x][y+1]!=-2):
            if flag_using.get()==1:
                flag_using1=-1
            delete_button(x,y+1)
            flag_using1=0
    else:
        show_bombs(x,y)
    help_using1=0
def delete_button(x,y):
    global game,buttons,buttons_alive,height,width,state,flag_using,flag_using1,flag_count,help_using,help_using1,help_count
    hide_bombs()
    if help_using.get()+help_using1==1and help_count.get()>0:
        help_count.set(help_count.get()-1)
        if game[x][y]==0:
            buttons[x][y].destroy()
            buttons_alive[x][y]=0
            help_using1=-1
            if x>0:
                if buttons_alive[x-1][y]==1:
                    delete_button(x-1,y)
                if (y>0)and(buttons_alive[x-1][y-1]==1):
                    delete_button(x-1,y-1)
                if (y<width-1)and(buttons_alive[x-1][y+1]==1):
                    delete_button(x-1,y+1)
            if x<height-1:
                if buttons_alive[x+1][y]==1:
                    delete_button(x+1,y)
                if (y>0)and(buttons_alive[x+1][y-1]==1):
                    delete_button(x+1,y-1)
                if (y<width-1)and(buttons_alive[x+1][y+1]==1):
                    delete_button(x+1,y+1)
            if (y>0)and(buttons_alive[x][y-1]==1):
                delete_button(x,y-1)
            if (y<width-1)and(buttons_alive[x][y+1]==1):
                delete_button(x,y+1)
        elif game[x][y]==-1:
            buttons[x][y].destroy()
            buttons_alive[x][y]=0
        else:
            click=lambda i=x,j=y:click_number(i,j)
            color="#00FF00"
            if game[x][y]==1:
                color="#0086FF"
            elif game[x][y]==2:
                color="#009608"
            elif game[x][y]==3:
                color="#FF0000"
            elif game[x][y]==4:
                color="#0000D5"
            elif game[x][y]==5:
                color="#A50000"
            elif game[x][y]==6:
                color="#00D000"
            buttons[x][y].config(text=str(game[x][y]),command=click,bg="#FFFFFF",activebackground="#FFFFFF",relief="flat",foreground=color,font=("Arial",10,"bold"))
            buttons_alive[x][y]=0
    elif help_using.get()+help_using1==1and help_count.get()==0:
        messagebox.showerror("Внимание!","Количество подсказок закончилось!")
    else:
        if flag_using1+flag_using.get()==0:
            if game[x][y]==0:
                buttons[x][y].destroy()
                buttons_alive[x][y]=0
                if x>0:
                    if buttons_alive[x-1][y]==1:
                        delete_button(x-1,y)
                    if (y>0)and(buttons_alive[x-1][y-1]==1):
                        delete_button(x-1,y-1)
                    if (y<width-1)and(buttons_alive[x-1][y+1]==1):
                        delete_button(x-1,y+1)
                if x<height-1:
                    if buttons_alive[x+1][y]==1:
                        delete_button(x+1,y)
                    if (y>0)and(buttons_alive[x+1][y-1]==1):
                        delete_button(x+1,y-1)
                    if (y<width-1)and(buttons_alive[x+1][y+1]==1):
                        delete_button(x+1,y+1)
                if (y>0)and(buttons_alive[x][y-1]==1):
                    delete_button(x,y-1)
                if (y<width-1)and(buttons_alive[x][y+1]==1):
                    delete_button(x,y+1)
            elif game[x][y]==-1:
                buttons[x][y].destroy()
                buttons_alive[x][y]=0
                answer=messagebox.askyesno(title="Сапёр",message="Вы проиграли, начать заново?")
                if answer:
                    restart(state)
                else:
                    menu_root()
            else:
                click=lambda i=x,j=y:click_number(i,j)
                color="#00FF00"
                if game[x][y]==1:
                    color="#0086FF"
                elif game[x][y]==2:
                    color="#009608"
                elif game[x][y]==3:
                    color="#FF0000"
                elif game[x][y]==4:
                    color="#0000D5"
                elif game[x][y]==5:
                    color="#A50000"
                elif game[x][y]==6:
                    color="#00D000"
                buttons[x][y].config(text=str(game[x][y]),command=click, bg="#FFFFFF",activebackground="#FFFFFF",relief="flat",foreground=color,font=("Arial", 10, "bold"))
                buttons_alive[x][y]=0
            abf=1
            for i in range(height):
                for j in range(width):
                    if buttons_alive[i][j]==1:
                        abf=0
            if abf==1:
                answer=messagebox.askyesno(title="Сапёр",message="Вы выиграли! Начать заново?")
                if answer:
                    restart(state)
                else:
                    menu_root()
        else:
            if buttons_alive[x][y]==-2:
                load=Image.open("sentry1.png")
                render=ImageTk.PhotoImage(load)
                buttons[x][y].config(image=render)
                buttons[x][y].image=render
                if game[x][y]==-1:
                    buttons_alive[x][y]=-1
                else:
                    buttons_alive[x][y]=1
                flag_count.set(flag_count.get()+1)
            else:
                load=Image.open("minefield-sign.png")
                render=ImageTk.PhotoImage(load)
                buttons[x][y].config(image=render)
                buttons[x][y].image=render
                buttons_alive[x][y]=-2
                flag_count.set(flag_count.get()-1)
menu_root()
root.mainloop()