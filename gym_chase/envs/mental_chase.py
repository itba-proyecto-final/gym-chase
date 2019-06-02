import gym
from math import floor

POSITION = 0
GOAL = 1
REWARD = 2

__END_OF_EXPERIENCE = "--\n"


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
    experiences = list()
    experience = (list(), list(), list())
    for l in lines[1:]:
        if l != "\n":
            if '-' in l and l != __END_OF_EXPERIENCE and not l.startswith("-"):
                [current_position, goal_position] = l.replace("\n", "").split("-")
                experience[POSITION].append(int(current_position))
                experience[GOAL].append(int(goal_position))
            elif l == __END_OF_EXPERIENCE:
                check_experience_validity(experience)
                experiences.append(experience)
                experience = (list(), list(), list())
            else:
                experience[REWARD].append(int(l.replace("\n", "")))
    file.close()
    return int(rows), int(cols), experiences


def check_experience_validity(experience):
    if len(experience[REWARD]) != len(experience[POSITION]):
        raise Exception("Input file was invalid, different amount of rewards and positions")
    if len(experience[REWARD]) != len(experience[GOAL]):
        raise Exception("Input file was invalid, different amount of goals and positions")


def read_rewards_file(filename):
    rewards = list()
    file = open(filename, "r")
    lines = file.readlines()
    for l in lines:
        rewards.append(int(l.replace("\n", "")))
    return rewards


class MentalChaseEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        self.reached_goal = False
        self.number_of_steps = 0
        self.rows, self.cols, self.experiences = read_game_file(
            "/Users/franbartolome/Desktop/rewards_states.txt")
        self.action_space = 4
        # TODO: change if goal moves
        self.observation_space = self.rows * self.cols
        self.amount_of_experiences = len(self.experiences)
        self.state = self.experiences[0][POSITION][0]
        self.initial_state = self.state
        self.previous_state = self.state
        self.goal = self.experiences[0][GOAL][0]
        self.reached_goal = False
        self.turn = 0
        self.already_reset = False

    def get_row_col_from_state(self, state):
        row = floor(state / self.cols)
        col = state - row * self.cols
        return row, col

    def calculate_reward(self):
        return self.experiences[0][REWARD].pop(0)

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
        if len(self.experiences[0][POSITION]) != 0:
            self.state = self.experiences[0][POSITION].pop(0)
            self.goal = self.experiences[0][GOAL].pop(0)
        if len(self.experiences[0][POSITION]) == 0 or self.goal == self.state:
            self.reached_goal = True  # TODO ver que siempre llegue al goal
        return self.state, self.calculate_reward(), self.reached_goal, self.get_action()

    def reset(self):
        if self.already_reset:
            self.experiences.pop(0)
            self.initial_state = self.experiences[0][POSITION][0]
        self.number_of_steps = 0
        self.state = self.initial_state
        self.reached_goal = False
        self.already_reset = True
        return self.state

    def render(self, mode='human', close=False):
        for i in range(self.rows):
            for j in range(self.cols):
                if i * self.cols + j == self.state:
                    print("X", end='')
                else:
                    print("-", end='')
            print()
