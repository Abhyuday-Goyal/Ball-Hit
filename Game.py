import tkinter as tk


class PlayComponent(object):
    def __init__(self, canvas, item):
        self.item = item
        self.canvas =canvas
    
    def move(self, x,y):
        self.canvas.move(self.item,x,y)
    
    def position(self):
        return self.canvas.coords(self.item)
    
    def delete(self):
        self.canvas.delete(self.item) 
    hitsplaycomponent = 0 
class Paddle(PlayComponent):
    def __init__(self, canvas, x, y):
        self.height =5
        self.width =100
        self.ball = None
        item = canvas.create_rectangle(x-self.width/2,
                                       y-self.height/2,
                                       x+self.width/2,
                                       y+self.height/2,
                                       fill='blue')
        super(Paddle,self).__init__(canvas, item)
   
    def set_ball(self,ball):
        self.ball = ball
            
    def move(self, dist):
        coord = self.position()
        width = self.canvas.winfo_width()
        if coord[2] +dist <=width and coord[0] +dist >=0:
            super(Paddle, self).move(dist, 0)
            if self.ball is not None:
                self.ball.move(dist,0)
   
            



                
class Ball(PlayComponent):
    def __init__(self, canvas, x, y):
        self.radius= 6
        self.speed = 5
        self.hitcount = PlayComponent.hitsplaycomponent
        self.direction = [-1,1]
        item = canvas.create_oval(x - self.radius,
                                  y - self.radius,
                                  x + self.radius,
                                  y + self.radius, 
                                  fill='red')
        super(Ball, self).__init__(canvas, item)
        
    def update(self):
        coord = self.position()
        width = self.canvas.winfo_width()
        if coord[1] <=0:
            self.direction[1]*= -1
        if coord[2] >=width or coord[0] <=0:
            self.direction[0] *= -1
        
        x = self.direction[0]*self.speed
        y = self.direction[1]*self.speed
        self.move(x, y)
    def intersect(self,components):
        coord = self.position()
        x = (coord[0] + coord[2])*.5
        
        if len(components) == 1:
            component = components[0]
            coord = component.position()
            if x < coord[0]:
                self.direction[0] =-1
                self.hitcount +=1
                PlayComponent.hitsplaycomponent = self.hitcount
               
            
            elif x> coord[2]:
                self.direction[0] = 1
                self.hitcount += 1
                PlayComponent.hitsplaycomponent = self.hitcount

            else:
                self.direction[1]*=-1
                self.hitcount +=1
                PlayComponent.hitsplaycomponent = self.hitcount
        #elif len(components)>1:
            #self.direction[1]*=-1
            
        
        
class Game(tk.Frame):
    def __init__(self,baba):

        super(Game,self).__init__(baba)
        self.lives = 3
        self.width = 1000
        self.height = 400
        self.hits = 0
        
        self.canvas = tk.Canvas(self, bg = 'cyan',
                                width = self.width,
                                height = self.height)
        
        self.canvas.pack()
        self.pack()
        
        self.items = {}
        self.ball = None
    
        self.paddle = Paddle(self.canvas, self.width/2, 320)
        self.items[self.paddle.item] = self.paddle
        
        self.hud = None
        self.init_game()
        self.canvas.focus_set()
        self.canvas.bind('<Left>',
                         lambda _:self.paddle.move(-30))
        self.canvas.bind('<Right>',
                         lambda _:self.paddle.move(30))
        

    def init_game(self):
        self.update_lives_text()
        self.display_ball()
        self.text = self.draw_text(self.width/2, self.height/2, 'Press "S" for start')
        self.canvas.bind('<s>', lambda _: self.start_game())
    

        
    def display_ball(self):
        if self.ball is not None:
            self.ball.delete()
        paddle_coords = self.paddle.position()
        x = (paddle_coords[0] + paddle_coords[2])*0.5
        self.ball = Ball(self.canvas,x,310)
        self.paddle.set_ball(self.ball)
        
    def draw_text(self, x, y, text, size='50'):
        font = ('Arial', size)
        return self.canvas.create_text(x, y, text=text, font=font)
        
    def update_lives_text(self):
        text = 'Lives:%s hits %s' % (self.lives, self.hits)
        if self.hud is None:
            self.hud= self.draw_text(70, 20, text, 15)
        else: 
            self.canvas.itemconfig(self.hud, text=text)
        
    def start_game(self):
        self.canvas.unbind('<s>')
        self.canvas.delete(self.text)
        self.paddle.ball = None
        self.game_loop()
        
    def game_loop(self):
        self.verify_inter()
        
        
        if self.ball.position()[3] >=self.height:
            self.ball.speed = None
            self.lives-=1
            if self.lives == 0:
                text2 = "Game over! Score=%s" %(self.hits)
                self.draw_text(self.width/2, self.height/2, text2)
            else:
                self.after(1000, self.init_game())
        else:
            self.ball.update()
            self.after(50, self.game_loop)
    
    def verify_inter(self):
        ball_coords = self.ball.position()
        items = self.canvas.find_overlapping(*ball_coords)
        objects = [self.items[x] for x in items if x in self.items]
        self.hits = self.ball.hitcount
        self.ball.intersect(objects)
        self.update_lives_text()
    
if __name__ =='__main__':
    root = tk.Tk()
    root.title('Ball Hit')
    game = Game(root)
    game.mainloop()
    

   
