import gym
from math import floor


def get_action_map():
    action_map = dict()
    action_map[0] = "Up"
    action_map[1] = "Right"
    action_map[2] = "Down"
    action_map[3] = "Left"
    return action_map


def read_game_file(filename):
    file = open(filename, "r")
    lines = file.readlines()
    [rows, cols] = lines[0].replace("\n", "").split("x")
    positions = list()
    goals = list()
    for l in lines[1:]:
        if '-' in l:  # TODO ver cuando este con el reward tambien puesto acá
            [current_position, goal_position] = l.replace("\n", "").split("-")
            positions.append(int(current_position))
            goals.append(int(goal_position))
    file.close()
    return int(rows), int(cols), positions, goals


class MentalChaseEnv(gym.Env):
    metadata = {'render.modes': ['human']}
    def __init__(self):
        self.reached_goal = False
        self.number_of_steps = 0
        self.rows, self.cols, self.positions, self.goals = read_game_file("/Users/natinavas/Downloads/grid_lights_experiment_nati_1.txt")
        if len(self.positions) != len(self.goals) : raise Exception("Input file was invalid, different amount of goals and positions")
        self.action_space = 4
        self.observation_space = self.rows * self.cols
        self.state = self.positions.pop()
        self.initial_state = self.state
        self.previous_state = self.positions.pop()
        self.goal = self.goals.pop()
        self.reached_goal = False

    def get_row_col_from_state(self, state):
        row = floor(state / self.cols)
        col = state - row*self.cols
        return row, col

    def calculate_reward(self): # TODO
        # Distance on x axis between goal and position increased
        row, col = self.get_row_col_from_state(self.state)
        prev_row, prev_col = self.get_row_col_from_state(self.previous_state)
        goal_row, goal_col = self.get_row_col_from_state(self.goal)

        if abs(row - goal_row) > abs(prev_row - goal_row):
            return -1
        # Distance on x axis between goal and position decreased
        if abs(row - goal_row) < abs(prev_row - goal_row):
            return 0
        # Distance on y axis between goal and position increased
        if abs(col - goal_col) > abs(prev_col - goal_col):
            return -1
        # Distance on y axis between goal and position decreased
        if abs(col - goal_col) < abs(prev_col - goal_col):
            return 0
        # If the target has been reached then give bigger prize
        if row == goal_row and col == goal_col:
            return 10
        return -1

    # TODO revisar porque no contempla casos bordes pero tampoco es necesario porque si se hizo una accion correcta no debería pasar nada bizarro
    def get_action(self):
        if self.state == self.previous_state + 1:  # Right
            return 1
        elif self.state == self.previous_state - 1:  # Left
            return 3
        elif self.state < self.previous_state:  # Up
            return 0
        else:  # Down
            return 2

    def step(self):
        self.number_of_steps += 1
        self.previous_state = self.state
        if len(self.positions) != 0:
            self.state = self.positions.pop()
            self.goal = self.goals.pop()
        if len(self.positions) == 0 or self.goal == self.state:
            self.reached_goal == True  # TODO ver que siempre llegue al goal
        return self.state, self.calculate_reward(), self.reached_goal, self.get_action()

    def reset(self):  # TODO revisar
        self.number_of_steps = 0
        self.state = self.initial_state
        self.reached_goal = False
        return self.state

    def render(self, mode='human', close=False):
        for i in range(self.rows):
            for j in range(self.cols):
                if i*self.cols + j == self.state:
                    print("X", end='')
                else:
                    print("-", end='')
            print()
