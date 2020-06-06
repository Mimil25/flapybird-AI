#!/usr/bin/python3.8

import tkinter as tk
import time
import random as r
from copy import deepcopy

class Bird:
    def __init__(self, canvas, ancetre=None):
        self.canvas = canvas
        if ancetre is None:
            self.id = self.canvas.create_oval(100, 200, 140, 240, fill="#F00")
            self.v = 0
            self.poids = [r.uniform(-100, 100) for i in range(5)]
        else :
            h = self.canvas.coords(ancetre.id)[1]
            self.id = self.canvas.create_oval(100, h, 140, h+40, fill="#F00")
            self.v = ancetre.v
            self.poids = deepcopy(ancetre.poids)

    def computer(self):
        s = self.poids[0]
        s += self.v * self.poids[1]
        s += self.canvas.coords(self.id)[1] * self.poids[2]
        s += self.canvas.coords(self.canvas.tuyaux[0][1])[0] * self.poids[3]
        s += self.canvas.coords(self.canvas.tuyaux[0][1])[1] * self.poids[4]
        if s > 0:
            self.v = -7

    def mutation(self, n=1):
        for i in range(5):
            self.poids[i] += r.uniform(-100/n, 100/n)


class Jeu(tk.Canvas):
    g = 0.5
    csv = open("flapybird.csv",'a')
    def __init__(self, root=None):
        tk.Canvas.__init__(self, root, bg="#88F", height=500, width=800)

        #self.bird = self.create_oval(100, 200, 140, 240, fill="#F00")
        self.birds = [Bird(self) for i in range(100)]
        #self.v = 0

        self.score = 0
        self.best = 0

        self.t = 60
        
        h = r.randint(0,200)
        self.tuyaux = [(self.create_rectangle(900, 0, 960, 100+h, fill="#0F0"),
                       self.create_rectangle(900,250+h,960, 500, fill="#0F0"))]
        for i in range(3):
            self.addtuyau()

        self.update()

    def play(self, _=None):
        print("ok")
        t = time.time()
        while True:

            for e in self.tuyaux:
                self.move(e[0], -5, 0)
                self.move(e[1], -5, 0)
                if self.coords(e[0])[2] < 0:
                    self.delete(*e)
                    del self.tuyaux[0]
                    self.addtuyau()
                    self.score += 1
                    print(self.score, "tuyaux sont passés")
            
            for i, bird in enumerate(self.birds):
                bird.computer()
                self.move(bird.id, 0, bird.v)
                bird.v += Jeu.g

                cb = self.coords(bird.id)
                ct = self.coords(self.tuyaux[0][1])
                if cb[2] > ct[0] and cb[0] < ct[2]:
                    if cb[1] < ct[1]-150 or cb[3] > ct[1]:
                        #self.best = max(self.score,self.best)
                        #print("Perdu", self.score, self.best)
                        #self.score = 0
                        print(bird.id, "est mort, heureusement il en reste", len(self.birds)-1)
                        self.delete(bird.id)
                        del self.birds[i]
            
            if len(self.birds) <= 5:
                print(*[bird.id for bird in self.birds], "se reproduisent")
                for i in range(len(self.birds)):
                    for loop in range(20):
                        new = Bird(self, self.birds[i])
                        new.mutation(self.score+1)
                        self.birds.append(new)

            self.update()
            s = (1/self.t + t - time.time())
            time.sleep(s if s > 0 else 0)
            t = time.time()

    def saut(self, _=None):
        self.v = -10

    def vplus(self, _=None):
        self.t *= 2

    def vmoins(self, _=None):
        self.t /= 2

    def addtuyau(self):
        h = r.randint(0, 200)
        w = self.coords(self.tuyaux[-1][0])[0]
        self.tuyaux.append((self.create_rectangle(w+300, 0, w+360, 100+h, fill="#0F0"),
                            self.create_rectangle(w+300,250+h,w+360, 500, fill="#0F0")))

def main():
    root = tk.Tk()
    root.title("Flapy Bird")

    jeu = Jeu(root)
    jeu.pack(fill=tk.BOTH, expand=True)
    jeu.bind('<Button-2>', jeu.play)
    jeu.bind('<Key-A>', jeu.play)
    jeu.bind('<Button-1>', jeu.vplus)
    jeu.bind('<Button-3>', jeu.vmoins)

    root.mainloop()

if __name__ == "__main__":
    main()
