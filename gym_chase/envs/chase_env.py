import gym


def get_state_map(num_rows_cols):
    state_map = dict()
    state_number = 0
    for i in range(num_rows_cols):
        for j in range(num_rows_cols):
            base_matrix = [['-' for _ in range(num_rows_cols)] for _ in range(num_rows_cols)]
            base_matrix[i][j] = 'X'
            state_map[get_matrix_string(base_matrix)] = state_number
            state_number += 1
    return state_map


def get_action_map():
    action_map = dict()
    action_map[0] = "Up"
    action_map[1] = "Right"
    action_map[2] = "Down"
    action_map[3] = "Left"


def get_matrix_string(matrix):
    matrix_string = ""
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            if matrix[i][j] == "G":
                matrix_string += "-,"
            else:
                matrix_string += matrix[i][j] + ","
    return matrix_string


class ChaseEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, num_row_cols=5, initial_pos=(0, 0), goal=(2, 3)):
        self.reached_goal = False
        self.state = [['-' for _ in range(num_row_cols)] for _ in range(num_row_cols)]
        self.state[initial_pos[0]][initial_pos[1]] = "X"
        self.num_rows_cols = num_row_cols
        self.current_position = initial_pos
        self.goal = goal
        self.state[goal[0]][goal[1]] = "G"
        self.number_of_steps = 0
        self.initial_position = initial_pos
        self.state_map = get_state_map(num_row_cols)
        self.action_map = get_action_map()
        self.observation_space = len(self.state_map.keys())
        self.action_space = 4

    def is_valid_action(self, action):
        if action == 0 and self.current_position[0] == 0:
            return False
        if action == 1 and self.current_position[1] == self.num_rows_cols - 1:
            return False
        if action == 2 and self.current_position[0] == self.num_rows_cols - 1:
            return False
        if action == 3 and self.current_position[1] == 0:
            return False
        return True

    def step(self, action):
        reward = 0

        if not self.is_valid_action(action):
            print("Invalid action")
            print("Direction was towards " + self.action_map[action])
            return self.state_map[get_matrix_string(self.state)], reward, self.reached_goal, self.number_of_steps

        if action == 0:  # Upwards Direction
            self.state[self.current_position[0]][self.current_position[1]] = "-"
            self.state[self.current_position[0] - 1][self.current_position[1]] = "X"
            self.current_position = (self.current_position[0] - 1, self.current_position[1])

        elif action == 1:  # Right Direction
            self.state[self.current_position[0]][self.current_position[1]] = "-"
            self.state[self.current_position[0]][self.current_position[1] + 1] = "X"
            self.current_position = (self.current_position[0], self.current_position[1] + 1)

        elif action == 2:  # Downwards Direction
            self.state[self.current_position[0]][self.current_position[1]] = "-"
            self.state[self.current_position[0] + 1][self.current_position[1]] = "X"
            self.current_position = (self.current_position[0] + 1, self.current_position[1])

        elif action == 3:  # Left Direction
            self.state[self.current_position[0]][self.current_position[1]] = "-"
            self.state[self.current_position[0]][self.current_position[1] - 1] = "X"
            self.current_position = (self.current_position[0], self.current_position[1] - 1)

        else:
            raise Exception("Action is not valid since it is not in the action space")

        if self.current_position == self.goal:
            print("You reached your goal!")
            self.reached_goal = True
            reward = 1  # TODO ver tema del reward
            return self.state_map[get_matrix_string(self.state)], reward, self.reached_goal, self.number_of_steps

        return self.state_map[get_matrix_string(self.state)], reward, self.reached_goal, self.number_of_steps

    def reset(self):
        self.state = [['-' for _ in range(self.num_rows_cols)] for _ in range(self.num_rows_cols)]
        self.state[self.initial_position[0]][self.initial_position[1]] = "X"
        self.state[self.goal[0]][self.goal[1]] = "G"
        print("Reseted state")
        self.render()

    def render(self, mode='human', close=False):
        for i in range(self.num_rows_cols):
            for j in range(self.num_rows_cols):
                print(self.state[i][j] + " ", end = '')
            print()


# chase_env = ChaseEnv()
# chase_env.render()
# print(chase_env.step(2))
# chase_env.render()
# print(chase_env.step(2))
# chase_env.render()
# print(chase_env.step(1))
# chase_env.render()
# print(chase_env.step(1))
# print(chase_env.step(1))
#
# chase_env.render()

