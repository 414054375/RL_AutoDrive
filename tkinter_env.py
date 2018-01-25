
import numpy as np
import time
import sys
import Tkinter as tk

np.random.seed(1)

ORIGIN = [1, 1]
TARGET = [9, 9]
OBS_DENSITY = 0.2
UNIT = 20   # pixels
MAZE_H = 10  # grid height
MAZE_W = 10  # grid width

class Env(tk.Tk, object):
    def __init__(self, Show):
        super(Env, self).__init__()
        self.show = Show
        self._action = ['up', 'down', 'left', 'right']
        self._action_num = len(self._action)
        self._current_pos = np.array(ORIGIN)
        self._isHell = np.zeros((MAZE_H, MAZE_W)) > 0
        self._build_bg()
        self._create_obstacles()


    def _build_bg(self):
        if (self.show == True):
            self.title('maze')
            self.geometry('{0}x{1}'.format(MAZE_H * UNIT, MAZE_H * UNIT))
            self.canvas = tk.Canvas(self, bg='white',
                      height=MAZE_H*UNIT,
                      width=MAZE_W*UNIT)
            #write lines
            for c in range(0, MAZE_W * UNIT, UNIT):
                x0, y0, x1, y1 = c, 0, c, MAZE_H * UNIT
                self.canvas.create_line(x0, y0, x1, y1)
            for r in range(0, MAZE_H * UNIT, UNIT):
                x0, y0, x1, y1 = 0, r, MAZE_H * UNIT, r
                self.canvas.create_line(x0, y0, x1, y1)
            self.canvas.pack()
        # write target and origin
        self.origin = self.create_block(ORIGIN, 'yellow')
        self.target = self.create_block(TARGET, 'pink')

    def _create_obstacles(self):
        for i in range(MAZE_H):
            for j in range(MAZE_W):
                if (np.random.uniform() < OBS_DENSITY and [i+1, j+1] != ORIGIN and [i+1, j+1] != TARGET):
                    if (self.show):
                        self.create_block([i+1, j+1], 'black')
                    self._isHell[i, j] = True

    def create_block(self, posi, color):
        if posi[0] > MAZE_H or posi[1] > MAZE_W or posi[0] < 0 or posi[1] < 0:
           return False
        return self.canvas.create_rectangle((posi[1] - 1) * UNIT,
                                     (posi[0] - 1) * UNIT,
                                     posi[1] * UNIT,
                                     posi[0] * UNIT,
                                     fill=color)

    def move_block(self, action):
        if action == 0:
            if self._current_pos[1] > 1:
                self._current_pos[1] += -1
                if (self.show):
                    self.canvas.move(self.origin, 0, -UNIT)
        elif action == 1:
            if self._current_pos[1] < MAZE_H:
                self._current_pos[1] += 1
                if (self.show):
                    self.canvas.move(self.origin, 0, UNIT)
        elif action == 2:
            if self._current_pos[0] > 1:
                self._current_pos[0] += -1
                if (self.show):
                    self.canvas.move(self.origin, -UNIT, 0)
        elif action == 3:
            if self._current_pos[0] < MAZE_H:
                self._current_pos[0] += 1
                if (self.show):
                    self.canvas.move(self.origin, UNIT, 0)

        return self._isHell[self._current_pos[0]-1, self._current_pos[1]-1], self._current_pos == TARGET

    def step(self, action):
        is_hell, is_target = self.move_block(action)
        done = False
        if (is_hell):
            done = True
            reward = -1
        elif (is_target):
            done = True
            reward = 1
        else:
            done = False

    def reset(self):
        self._current_pos = ORIGIN

        self.canvas.delete(self.origin)
        print ORIGIN[0], ORIGIN[1]
        self.origin = self.create_block(ORIGIN, 'yellow')

if __name__ == '__main__':
    env = Env(True)
    print env.canvas.coords(env.origin)[:2]


    #env.reset()
    env.mainloop()

