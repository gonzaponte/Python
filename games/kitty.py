from __future__ import division
import Tkinter
import time
time.sleep(1)


speed     = 50
timelapse = 5000//speed

mainwindow = Tkinter.Tk()
mainwindow.title('Kitty')
mainwindow.geometry('800x600')


states = {}
states['hungry']    = "I want to eat something!"
states['starving']  = "I'm starving! Meeeeu"
states['dirty']     = ""
states['goodmood']  = "Meeeeeeeeu =)"
states['depressed'] = "Nobody loves me! =("
states['dead']      = "You're a horrible person! You killed this cute kitty!"

pictures = {}
pictures['goodmood']  = Tkinter.PhotoImage( file = "goodmood.gif"  )
pictures['hungry']    = Tkinter.PhotoImage( file = "hungry.gif"    )
pictures['starving']  = Tkinter.PhotoImage( file = "starving.gif"  )
pictures['sad']       = Tkinter.PhotoImage( file = "sad.gif"       )
pictures['depressed'] = Tkinter.PhotoImage( file = "depressed.gif" )
pictures['dead']      = Tkinter.PhotoImage( file = "dead.gif"      )

statusstring = Tkinter.StringVar()
statusstring.set( states['goodmood'] )
status  = Tkinter.Label ( mainwindow, textvariable = statusstring, font = ('Times',26) );status.pack()
picture = Tkinter.Label ( mainwindow, image = pictures['goodmood'] );picture.pack()

class Kitty(Tkinter.Label):
    '''
        A kitty.
    '''
    def __init__( self, name, hunger = 1000, mimos = 100 ):
        Tkinter.Label.__init__( self, mainwindow )
        self.name           = name
        self.hunger         = hunger
        self.mimos          = mimos
        self.alive          = True
        self.hungry         = False
        self.starving       = False
        self.sad            = False
        self.depressed      = False

        self.hungrylevel    = hunger/2
        self.starvinglevel  = hunger/5
        self.sadlevel       = mimos/2
        self.depressedlevel = mimos/5


        self.TimeStep()
    
    def __str__( self ):
        return '''
hunger level = {0}
mimos  level = {1}'''.format(self.hunger,self.mimos)
    
    def SetStatus( self ):
        if self.hunger <= 0 or self.mimos <= 0:
            self.alive = False
            statusstring.set( states['dead'] )
            picture.configure( image = pictures['dead'] )
            return
        
        elif self.hunger < self.hungrylevel and not self.hungry:
            self.hungry = True
            statusstring.set( states['hungry'] )
            picture.configure( image = pictures['hungry'] )

        elif self.hunger >= self.hungrylevel and self.hungry:
            self.hungry = False
            statusstring.set( states['goodmood'] )
            picture.configure( image = pictures['goodmood'] )

        elif self.hunger < self.starvinglevel and not self.starving:
            self.starving = True
            statusstring.set( states['starving'] )
            picture.configure( image = pictures['starving'] )

        elif self.hunger >= self.starvinglevel and self.starving:
            self.starving = False
            statusstring.set( states['hungry'] )
            picture.configure( image = pictures['hungry'] )

        elif self.mimos < self.sadlevel and not self.sad:
            self.sad = True
            statusstring.set( states['depressed'] )
            picture.configure( image = pictures['sad'] )

        elif self.mimos >= self.sadlevel and self.sad:
            self.depressed = False
            statusstring.set( states['goodmood'] )
            picture.configure( image = pictures['goodmood'] )

    def TimeStep( self ):
        self.hunger -= 1
        self.mimos  -= 1
        print self
        self.SetStatus()
        if self.alive:
            self.after( timelapse, self.TimeStep )

    def Feed( self, N = 10):
        self.hunger += N

    def Pamper( self, N = 10 ):
        self.mimos += N

kitty = Kitty('jjj')

feed   = Tkinter.Button( mainwindow, text = 'Feed', command = kitty.Feed );feed.pack()
pamper = Tkinter.Button( mainwindow, text = 'Pamper', command = kitty.Pamper );pamper.pack()
mainwindow.mainloop()


