# -*- coding: utf-8 -*-
from tkinter import *
import tkinter.messagebox as tkm
import sys
from random import randint
 
class Grid(object):
    def __init__(self,master=None,window_width=600,window_height=600,grid_width=20,offset=10):
        #嗯，怎么说呢。每一个gui程序都有一个称为
        #顶层(toplevel)的窗口管理器用于管理那些窗口部件
        #如按钮，输入框之类的，这个窗口管理器
        #就是这些下级部件的master，顶级窗口的master是None
        #即，它自己管理自己。
        self.height = window_height
        self.width = window_width
        self.grid_width = grid_width
        self.offset = offset
        self.grid_x = self.width//self.grid_width
        self.grid_y = self.height//self.grid_width
        self.bg = "#EBEBEB"
        # x1--x2  y1--y2为蛇活动的区域
        self.topBlank = 100;
        x0 = 0
        x1 = self.offset-1
        x2 = self.offset   + self.width+1
        x3 = self.offset*2 + self.width
        y0 = self.topBlank
        y1 = self.offset-1 + self.topBlank
        y2 = self.offset   + self.height+1 + self.topBlank
        y3 = self.offset*2 + self.height + self.topBlank
        #画底色

        self.canvas = Canvas(master, width = x3, height = y3, bg=self.bg)
        self.canvas.create_text(self.width//2,self.topBlank//2, text = '贪吃蛇', fill = 'blue')  
        self.drawScore(0)       
        #画边框
        self.canvas.create_rectangle(x0, y0, x1, y3, fill = "#000000", outline = "#000000")
        self.canvas.create_rectangle(x0, y0, x3, y1, fill = "#000000", outline = "#000000")
        self.canvas.create_rectangle(x0, y2, x3, y3, fill = "#000000", outline = "#000000")
        self.canvas.create_rectangle(x2, y0, x3, y3, fill = "#000000", outline = "#000000")
        #第一个是宽，第二个是高
        self.canvas.pack()
        self.grid_list()

    #绘制开始按钮
    def drawButton(self, status):
        self.canvas.create_rectangle(
            self.width//2+220, self.topBlank//2-20, self.width//2+280, self.topBlank//2+20, 
            fill = "#1E90FF", outline = "#0000CD")
        print(status)
        text = {"run":"暂停","stop":"开始"}
        self.canvas.create_text(
            self.width//2+250,self.topBlank//2, text = '%s'%text[status],
            activefill= "#4169E1", fill = 'red')
    #绘制分数
    def drawScore(self, score):
        self.canvas.create_rectangle(
            self.width//2+70,self.topBlank//2-10, self.width//2+130,self.topBlank//2 +10,
            fill = self.bg, outline = self.bg)
        self.canvas.create_text(
            self.width//2+100,self.topBlank//2,
            text = '得分:%3.i'%score, fill = 'red')
    #在pos位置的格子上绘颜色块
    def draw(self, pos, color,):
        x = pos[0]*self.grid_width + self.offset
        y = pos[1]*self.grid_width + self.offset+self.topBlank
        self.canvas.create_rectangle(x, y, x+self.grid_width, y+self.grid_width,fill=color,outline=self.bg)
    def grid_list(self):
        grid_list = []
        for y in range(0,self.grid_y):
            for x in range(0,self.grid_x):
                grid_list.append((x,y))
        self.grid_list = grid_list
 
class Food(object):
    def __init__(self, Grid, snakeBody):
        self.grid = Grid
        self.color = "#DDA0DD"
        self.set_pos(snakeBody)
    #生成食物位置  #食物不出现在边界旁
    def set_pos(self, snakeBody):
        x = randint(1, self.grid.grid_x - 2)
        y = randint(1, self.grid.grid_y - 2)
        while((x, y) in snakeBody):
            x = randint(1, self.grid.grid_x - 2)
            y = randint(1, self.grid.grid_y - 2)
        self.pos = (x, y)
    #画食物
    def display(self):
        self.grid.draw(self.pos, self.color)
 
class Snake(object):
    def __init__(self, Grid):
        self.grid = Grid
        self.body = [(1,1),(1,2),(1,3)]
        self.direction = "Right"
        self.status = 'stop'
        self.speed = 600	#数值越小速度越快,得分越高速度越快
        self.bodyColor = "#87CEEB"     
        self.headColor = "#4169E1"   
        self.food = Food(self.grid, self.body)
        self.gameover = False
        self.score = 0
    def change_status(self):
        if self.status == 'run':
            self.status = 'stop'
        else:
            self.status = 'run'
        self.grid.drawButton(self.status)
    #返回不被蛇所占用的格子    
    def available_grid(self):
        return [i for i in self.grid.grid_list if i not in self.body]
    #蛇改变方向
    def change_direction(self, direction):
        self.direction = direction

    #画蛇的身体和头
    def display(self):
        head = self.body[0]
        self.grid.draw(head, self.headColor)
        for (x, y) in self.body[1:]:
            self.grid.draw((x, y), self.bodyColor)
    #蛇移动
    def move(self):
        #计算新蛇头位置
        head = self.body[0]

        dirChange = {'Up':(0, -1), 'Down':(0, 1), 'Left':(-1, 0), 'Right':(1, 0)}
        newHead = (head[0] + dirChange[self.direction][0], head[1] + dirChange[self.direction][1])

        #判断新蛇头的位置是否合法
        if not newHead in self.available_grid():#不合法
            self.change_status()          
            self.gameover = True
        else:#合法
            self.grid.draw(head,self.bodyColor)
            self.grid.draw(newHead,color=self.headColor)
            self.body.insert(0, newHead)

        #判断是否吃到食物
        if self.food.pos != head:#没吃到
            pop = self.body.pop()
            self.grid.draw(pop,self.grid.bg)
        else:#吃到了(生成新食物并显示)
            self.score += 1
            self.grid.drawScore(self.score)
            self.speed = 600 - 100*self.score #600--200 0--8
            if self.score > 4:
                self.speed = 200 - 10*(self.score-8)
            if self.score > 9:
                self.speed = 150 - 5 *(self.score-13)
            if self.score > 19:
                self.speed = 150 - 2 *(self.score-23)
            if self.score > 44:
                self.speed = 100
            self.food.set_pos(self.body)
            self.food.display()

class SnakeGame(Frame):
    def __init__(self,master=None, *args, **kwargs):
        ## 当函数的参数不确定时，可以使用*args和**kwargs。*args没有key值，**kwargs有key值
        Frame.__init__(self, master)
        self.master = master
        self.grid = Grid(master=master,*args, **kwargs)
        self.snake = Snake(self.grid)
        self.nowDir = self.snake.direction
        self.nextDir = self.snake.direction
        self.round = 0;
        self.bind_all("<KeyRelease>", self.key_release) #将<KeyRelease>事件绑定到self.run()来处理
        self.bind_all("<Button-1>", self.button1_click)
        self.snake.display()
        self.snake.food.display()
        self.grid.drawButton(self.snake.status)

    def run(self):
        #游戏运行中
        if self.snake.status == 'run':
            if self.nextDir != self.nowDir:
                self.snake.change_direction(self.nextDir)
            self.snake.move()
        self.round+=1
        print(self.round)
        
        if self.snake.gameover == True:
            message =  tkm.showinfo("Game Over", "your score: %d" % self.snake.score)
            if message == 'ok':
                sys.exit()

        self.after(self.snake.speed,self.run)#延时

    def button1_click(self, event):
        x1 = self.grid.width//2+220
        y1 = self.grid.topBlank//2-20
        x2 = self.grid.width//2+280
        y2 = self.grid.topBlank//2+20
        posx = event.x
        posy = event.y
        if (x1 < posx) and (posx < x2) and (y1 < posy) and (posy < y2):
            self.snake.change_status()

    #<KeyRelease>事件处理函数
    def key_release(self,event):
        #key为键盘按下的键
        key = event.keysym
        oppDir = {"Up":"Down","Down":"Up","Left":"Right","Right":"Left"}
        self.nowDir = self.snake.direction
        self.nextDir = self.nowDir

        #响应方向键，如果不与当前方向相同或相反则响应
        if key in oppDir and key != oppDir[self.nowDir]:
            self.nextDir = key
        elif key == 'space':#如果按下了'space'暂停键
            self.snake.change_status()

if __name__ == '__main__':
    root = Tk()
    root.title("TR的贪吃蛇————————空格 暂停/继续")
    snakegame = SnakeGame(root)
    snakegame.run()
    snakegame.mainloop()