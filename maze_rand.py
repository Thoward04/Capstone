import matplotlib.pylab as plt 
from skimage.morphology import skeletonize
import numpy as np
from pygame.locals import *
import pygame
from time import sleep
from math import sqrt
import random
import os
import create_maze

MAZE_WIDTH = 25
MAZE_HEIGHT = 20
WINDOW_X = MAZE_WIDTH * 44
WINDOW_Y = MAZE_HEIGHT * 44 + 40
WHITE = (255, 255, 255)
TEXT_Y = WINDOW_Y - 30#WINDOW_Y * 23/24
TEXT_X = 110 #WINDOW_X/8
TEXT_SIZE = 16

class Player():
    # x = 46
    # y = 46
    # speed = PLAYER_SPEED
    # num_moves = NUM_MOVES

    def __init__(self, spawn_position):
        self.move_list = []
        self.fitness = 0
        self.id = None
        self.positions = []
        self.made_goal = 0
        self.spawn_position = spawn_position
        self.unique_positions = {self.spawn_position}
        self.x = spawn_position[0] + 2
        self.y = spawn_position[1] + 2

class App:

    window_width = WINDOW_X
    window_height = WINDOW_Y
    # num_players = NUM_PLAYERS
    # fps = FPS
    # fitness_func = FIT_FUNC # distance Or unique
    # generations = 1
    # average_fitness = []
    # best_fitness = []

    def __init__(self):
        self._running = True
        self._display_surf = None
        self._image_surf = None
        self._dead_surf = None
        self._block_surf = None

        self.maze = Maze()

        # self.players = [Player(self.maze.spawn_pos) for i in range(self.num_players)]

        # id = 0
        # for player in self.players:
        #     player.id = id
        #     id+=1

        # self.FPSclock = None
        self.bootup = True
        # self.turn = 1
        # self.num_moves = NUM_MOVES
        # self.moves_array = create_moves_array()
        # self.player_known_walls = set()
        # self.made_it_proportion = 0

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode((self.window_width, self.window_height))

        pygame.display.set_caption("Maze Game!")
        self._running = True
        self._image_surf = pygame.image.load("start.png").convert()
        # self._dead_surf = pygame.image.load("dead_duck.png").convert()
        self._block_surf = pygame.image.load("walls.png").convert()
        self._goal_surf = pygame.image.load("finish.png").convert()
        self.FPSclock = pygame.time.Clock()
        # self.victory_quack = pygame.mixer.Sound("victory_ding.mp3")
        # self.random_quacks = os.listdir(QUACKS_FILEPATH)

    # def restart(self, moves_list):
    #     self.turn = 1
    #     self.generations += 1
    #     self.moves_array = np.array(moves_list)
    #     self.players = [Player(self.maze.spawn_pos) for i in range(self.num_players)]

    #     id = 0
    #     for player in self.players:
    #         player.id = id
    #         id+=1

    #     print("Game restarted, on to the next generation")

    def on_event(self, event):
        if event.type == QUIT:
            self._running = False

    def on_loop(self):
        for block_x, block_y in self.maze.collision_coords:
            for player in self.players:
                if self.is_collision(player.x, player.y, block_x, block_y,
                                     bsize=44):
                    # *** THINK OF SOMETHING BETTER ****
                    player.speed = 0
                    self.player_known_walls.add((player.x, player.y))

        for player in self.players:
            if self.is_collision(player.x, player.y, self.maze.goal[0], self.maze.goal[1],
                                 bsize=44):
                player.made_goal = 1
                player.speed = 0
                print("HOORAY!!! I DUCK HAS MADE IT!! WHAT A BLOODY RIPPA!")
                self.victory_quack.play()

    def on_render(self):
        #maze halls
        self._display_surf.fill((0, 0, 0))
        # self._display_surf.blit(self._image_surf)
        # for player in self.players:
        #     if player.speed > 0:
        #        self._display_surf.blit(self._image_surf, (player.x, player.y))
        #     elif player.speed == 0:
        #         self._dead_surf.blit(self._dead_surf, (player.x, player.y))

        # try:
        #     message_display("FPS: {}  |  Generation {}  |  Best Fit {} | Prop Madeit {}".format(str(self.fps),
        #                                                                    str(self.generations),
        #                                                                    str(int(min(self.best_fitness))),
        #                                                                    self.made_it_proportion),
        #                     self._display_surf,
        #                     x=5.5 * TEXT_X, y=TEXT_Y)

        # except:
        #     message_display("FPS: {}  |  Generation {}  |  Best Fit | Prop Madeit ".format(str(self.fps),
        #                                                                    str(self.generations)),
        #                     self._display_surf,
        #                     x=5.5 * TEXT_X, y=TEXT_Y)

        self.maze.draw(self._display_surf, self._block_surf, self._goal_surf, self._image_surf)
        pygame.display.flip()

        if self.bootup:
            sleep(3)
            self.bootup = False

    def on_cleanup(self):
        pygame.display.quit()

        # Uncomment the following for plots

        # plt.subplot(1, 2, 1)
        # plt.plot([i for i in range(self.generations-1)], self.average_fitness)
        # plt.title("Average Fitness per Generation")
        # plt.xlabel("Generation")
        # plt.ylabel("Fitness, Distance to Target (lower is better)")
        #
        # plt.subplot(1, 2, 2)
        # plt.plot([i for i in range(self.generations-1)], self.best_fitness)
        # plt.title("Best Fitness per Generation")
        # plt.xlabel("Generation")
        # plt.ylabel("Fitness, Distance to Target (lower is better)")
        # plt.waitforbuttonpress()

    # def is_collision(self, x1, y1, x2, y2, bsize):
    #     if x1 >=x2 and x1 <= x2 + bsize:
    #         if y1 >= y2 and y1 <= y2 + bsize:
    #             return True
    #     else:
    #         return False

    # def calc_madeit_prop(self):
    #     madeit_sum = 0

    #     for player in self.players:
    #         if player.made_goal == 1:
    #             madeit_sum += 1

    #     return madeit_sum/NUM_PLAYERS

    # def play_random_quack(self, likelihood = 0.0002):
    #     if random.random() <= likelihood:
    #         fp = QUACKS_FILEPATH + "/" + random.choice(self.random_quacks)
    #         pygame.mixer.music.load(fp)
    #         pygame.mixer.music.play()

    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        while( self._running ):
            pygame.event.pump()
            keys = pygame.key.get_pressed()

            # # CALC FITNESS *****************************************************
            # # If we're on the final turn or all of the players have hit a wall
            # if self.turn == self.num_moves or max(player.speed for player in self.players)==0:
            #     self.made_it_proportion = self.calc_madeit_prop()

            #     if self.made_it_proportion > MADEIT_THRESH:
            #         print("{}% HAVE MADE IT, BLOODY WELL DONE LEGENDS".format(self.made_it_proportion*100))
            #         self.on_cleanup()
            #         break

            #     if self.generations == GENERATION_THRESH:
            #         print("NO ONE MADE IT IN TIME!!!!!!!!!!!!!! NEW DUCKS PLZ")
            #         self.on_cleanup()
            #         break

            #     # Calculate the fitness
            #     if self.fitness_func == "distance":

            #         for player in self.players:
            #             player.fitness = calc_goal_distance(player.x, player.y,
            #                                                 self.maze.goal[0], self.maze.goal[1],
            #                                                 measure = "manhattan")
            #             total_visited = len(player.positions)
            #             unique_visited = len(set(player.positions))

            #             num_backtracks = total_visited - unique_visited
            #             player.fitness = player.fitness + (3*num_backtracks)

            #         sum = 0
            #         for player in self.players:
            #             sum += player.fitness

            #     else:
            #         for player in self.players:
            #             player.fitness = len(player.unique_positions)

            #             if player.speed==0 and player.made_goal == 0:
            #                 player.fitness = player.fitness + 20

            #         sum = 0
            #         for player in self.players:
            #             sum += player.fitness

            #     self.average_fitness.append((sum/self.num_players))
            #     print("Average fitness of {}".format(sum/self.num_players))


           
            # self.on_loop()
            self.on_render()
            # self.FPSclock.tick(self.fps)
            # self.turn +=1


        self.on_cleanup()
class Maze:
    def __init__(self):
        self.M = MAZE_WIDTH
        self.N = MAZE_HEIGHT

        # The test maze seen in the blog post
        # self.maze = [ 1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,
        #               1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,
        #               1,0,1,1,1,1,1,1,1,0,1,0,1,1,1,0,1,1,0,1,
        #               1,0,1,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,1,
        #               1,0,1,0,1,0,1,0,1,1,1,0,1,0,0,0,1,0,1,1,
        #               1,0,0,0,1,0,1,0,0,0,1,0,1,0,0,0,1,0,1,1,
        #               1,1,1,1,1,0,1,1,1,0,0,0,1,0,1,1,1,0,0,1,
        #               1,0,0,0,0,0,1,0,1,1,1,1,1,0,1,0,1,1,0,1,
        #               1,1,1,1,1,1,1,0,0,0,0,0,0,0,1,0,0,0,0,1,
        #               1,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,
        #               1,0,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,1,
        #               1,0,0,0,0,0,0,0,0,0,0,1,0,1,0,1,1,0,1,1,
        #               1,0,1,1,1,1,1,1,1,1,0,1,0,1,1,1,1,1,1,1,
        #               1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,2,
        #               1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,]

        self.maze = create_maze.make_maze(self.M, self.N)

        self.collision_coords = []
        self.goal = None

        # Populate the collision coords
        bx = 0
        by = 0
        for i in range(0, self.M * self.N):
            if self.maze[ bx + (by*self.M) ] == 1:
                self.collision_coords.append((bx * 44, by * 44))

            elif self.maze[ bx + (by * self.M) ] == 2:
                  self.goal = ((bx * 44, by * 44))

            elif self.maze[ bx + (by * self.M) ] == 3:
                  self.spawn_pos = ((bx * 44, by * 44))

            bx += 1

            if bx > self.M-1:
                bx = 0
                by += 1

        self.collision_coords = np.array(self.collision_coords)

    def draw(self, display_surf, image_surf, goal_surf, block_surf):
        bx = 0
        by = 0

        # This for loop looks along each row of the maze and determines if there is
        # a 1 or 0 at that place. If there is a one, it draws a square on the surface
        for i in range(0, self.M * self.N):
            if self.maze[ bx + (by*self.M) ] == 1:
                display_surf.blit(image_surf, (bx * 44, by * 44))

            if self.maze[bx + (by * self.M)] == 2:
                display_surf.blit(goal_surf, (bx * 44, by * 44))

            if self.maze[bx + (by * self.M)] == 3:
                display_surf.blit(block_surf, (bx * 44, by * 44))

            bx += 1

            if bx > self.M-1:
                bx = 0
                by += 1

        pygame.image.save(display_surf, "maze.jpg")

while True:
    maze_game = App()
    maze_game.on_execute()


