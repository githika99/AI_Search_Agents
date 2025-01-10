import numpy as np
import helper
import random

#   This class has all the functions and variables necessary to implement snake game
#   We will be using Q learning to do this

class SnakeAgent:

    #   This is the constructor for the SnakeAgent class
    #   It initializes the actions that can be made,
    #   Ne which is a parameter helpful to perform exploration before deciding next action,
    #   LPC which ia parameter helpful in calculating learning rate (lr) 
    #   gamma which is another parameter helpful in calculating next move, in other words  
    #            gamma is used to blalance immediate and future reward
    #   Q is the q-table used in Q-learning
    #   N is the next state used to explore possible moves and decide the best one before updating
    #           the q-table
    def __init__(self, actions, Ne, LPC, gamma):
        self.actions = actions
        self.Ne = Ne
        self.LPC = LPC
        self.gamma = gamma
        self.reset()

        # Create the Q and N Table to work with
        self.Q = helper.initialize_q_as_zeros()
        self.N = helper.initialize_q_as_zeros()


    #   This function sets if the program is in training mode or testing mode.
    def set_train(self):
        self._train = True

     #   This function sets if the program is in training mode or testing mode.       
    def set_eval(self):
        self._train = False

    #   Calls the helper function to save the q-table after training
    def save_model(self):
        helper.save(self.Q)

    #   Calls the helper function to load the q-table when testing
    def load_model(self):
        self.Q = helper.load()

    #   resets the game state
    def reset(self):
        self.points = 0
        self.s = None
        self.a = None

    #   This is a function you should write. 
    #   Function Helper:IT gets the current state, and based on the 
    #   current snake head location, body and food location,
    #   determines which move(s) it can make by also using the 
    #   board variables to see if its near a wall or if  the
    #   moves it can make lead it into the snake body and so on. 
    #   This can return a list of variables that help you keep track of
    #   conditions mentioned above.


    # Transforms 
    def helper_func(self, state):
        # Unpack state components
        head_x, head_y, body, food_x, food_y = state
        # print("snake head_x at", head_x)
        # print("snake head_y at", head_y)

        # Calcuate self.s for the given state
        # Adjoining wall states

        wall_x = 0 if head_x <= helper.BOARD_LIMIT_MIN else 1 if head_x >= helper.BOARD_LIMIT_MAX else 2
        wall_y = 0 if head_y <= helper.BOARD_LIMIT_MIN else 1 if head_y >= helper.BOARD_LIMIT_MAX else 2

        # Food direction
        food_dir_x = 0 if food_x < head_x else 1 if food_x > head_x else 2
        food_dir_y = 0 if food_y < head_y else 1 if food_y > head_y else 2

        # Adjoining body states
        body_top = 1 if (head_x, head_y - helper.SNAKE_UNIT_SIZE) in body else 0
        body_bottom = 1 if (head_x, head_y + helper.SNAKE_UNIT_SIZE) in body else 0
        body_left = 1 if (head_x - helper.SNAKE_UNIT_SIZE, head_y) in body else 0
        body_right = 1 if (head_x + helper.SNAKE_UNIT_SIZE, head_y) in body else 0

        # Update s
        s = (wall_x, wall_y, food_dir_x, food_dir_y, body_top, body_bottom, body_left, body_right)

        return s


    # Computing the reward, need not be changed.
    def compute_reward(self, points, dead):
        if dead:
            return -1
        elif points > self.points:
            return 1
        else:
            return -0.1

    #   This is the code you need to write. 
    #   This is the reinforcement learning agent
    #   use the helper_func you need to write above to
    #   decide which move is the best move that the snake needs to make 
    #   using the compute reward function defined above. 
    #   This function also keeps track of the fact that we are in 
    #   training state or testing state so that it can decide if it needs
    #   to update the Q variable. It can use the N variable to test outcomes
    #   of possible moves it can make. 
    #   the LPC variable can be used to determine the learning rate (lr), but if 
    #   you're stuck on how to do this, just use a learning rate of 0.7 first,
    #   get your code to work then work on this.
    #   gamma is another useful parameter to determine the learning rate.
    #   based on the lr, reward, and gamma values you can update the q-table.
    #   If you're not in training mode, use the q-table loaded (already done)
    #   to make moves based on that.
    #   the only thing this function should return is the best action to take
    #   ie. (0 or 1 or 2 or 3) respectively. 
    #   The parameters defined should be enough. If you want to describe more elaborate
    #   states as mentioned in helper_func, use the state variable to contain all that.
    
    def agent_action(self, state, points, dead):
        # Step 1: Process current state
        curr_state = self.helper_func(state)

        # Step 2: Compute reward
        reward = self.compute_reward(points, dead)
        #print("reward is", reward)

        if not self._train: #Test
            # Choose action with the highest Q-value
            action = np.argmax(self.Q[curr_state])

        # Step 3: Update Q-values if in training mode
        if self._train:
            if self.s is not None and self.a is not None:
                # Get maximum Q-value for the current state
                Q_max = np.max(self.Q[curr_state])
                #print("Q_max is", Q_max)

                # Increment visit count for state-action pair
                self.N[self.s][self.a] += 1
                #print("self.N[self.s][self.a] is", self.N[self.s][self.a])

                # Compute learning rate
                #lr = self.LPC / (self.LPC + self.N[self.s][self.a])
                lr = .7

                # Update Q-value for the state-action pair
                self.Q[self.s][self.a] += lr * (reward + self.gamma * Q_max - self.Q[self.s][self.a])
                #print("updated self.Q[self.s][self.a] to", self.Q[self.s][self.a])
            
            # Pick a new state

            # Exploration: Use epsilon to determine if action will be random
            self.Ne = 0.1
            if random.random() < self.Ne:
                action = random.choice(self.actions)
            # Exploitation: If not, pick the action with the highest Q-Value
            else:
                action = np.argmax(self.Q[curr_state])            

        # Step 5: Update state and action tracking
        if not dead:
            self.s = curr_state
            self.a = action
            self.points = points  # Update current points (redundant line if points doesn't change)

        else:
            self.s = None
            self.a = None
        #print("action is", action)
        # Step 6: Return selected action
        return action



    # def agent_action(self, state, points, dead): 
    #     curr_s = self.helper_func(state)
    #     reward = self.compute_reward(points, dead)
    #     if self._train:
    #         learning_rate = 0.7
    #         reward = self.compute_reward(points, dead)
    #         def q_training(learning_rate, reward, curr_s):
    #             # update q table for previous state
    #             if self.s is not None: #bc for first call it will be Null
    #                 self.N[self.s][self.a] += 1
    #                 max_q = np.max(self.Q[curr_s])
    #                 self.Q[self.s][self.a] += learning_rate * (reward + self.gamma * max_q - self.Q[self.s][self.a])

    #             # now pick an action for current state to take
    #             # if random.uniform(0, 1) < self.Ne * max(1, np.max(self.N)):
    #             #     action = random.choice([0,1,2,3])  # Explore
    #             # else: #pick highest Q valued action
    #             #     max_q = float("-inf")
    #             #     action = None
    #             #     for a in [0,1,2,3]:
    #             #         curr_q = self.Q[curr_s][a] > max_q
    #             #         if curr_q > max_q:
    #             #             max_q = curr_q
    #             #             action = a
    #             # return action
                
            
    #             f_values = []
    #             for a in [0,1,2,3]:
    #                 print("self.Ne is", self.Ne)
    #                 print("self.N[curr_s][a] is", self.N[curr_s][a])
    #                 if self.N[curr_s][a] < self.Ne * max(1, np.max(self.N)):
    #                     f_value = 10
    #                 else:
    #                     f_value = self.Q[curr_s][a]
    #                 f_values.append(f_value)
    #             # get action that has highest f_value
    #             print("f_values is", f_values, "max is", np.argmax(f_values))
    #             return np.argmax(f_values)
            
    #         # update q-table
    #         action = q_training(learning_rate, reward, curr_s)
    #         self.save_model()
        
    #     else:
    #         max_q = float("-inf")
    #         action = None
    #         for a in [0,1,2,3]:
    #             curr_q = self.Q[curr_s][a] > max_q
    #             if curr_q > max_q:
    #                 max_q = curr_q
    #                 action = a
    
    #     print("chosing action", action)
        
    #     if dead:
    #         self.s = None
    #         self.a = None
    #     else:
    #         self.s = curr_s
    #         self.a = action
    #     return action




    # going into this function, self.s is the previous state and self.a is the previously chosen action that result in state
    # so in q-learning we actually update the value in the q table at the previous state with the previously chosen action (bc it resulted in the current state)
    # def agent_action(self, state, points, dead): 
        
    #     # LPC is used to calculate learning rate
    #     # gamma is discount factor (0-1)
    #     # keep lr (learning rate) = 0.7 
    #     # maxQ(s',a') is maximum Q value of state after taking action a'
    #         # highest Q-value for all possible actions a' in the next state s'

    #     self.load_model()

    #     if self._train == True:
    #         # if we are in train update q-table
    #         # N variable - tracks how many times an agent has taken a specific action in a specific state
    #         # we want to take actions with lower N variables, to explore more
    #         # update N variable

    #         # from the valid actions (helper_func) we have, check the reward (compute_reward) and N values to make an action
            
    #         # self.Ne set in do_training()

    #         # calculate the Q table appropriate state for current state
    #         head_x, head_y, body, food_x, food_y = state
    #         wall_x = 0 if head_x == 0 else 1 if head_x == helper.GRID_SIZE - 1 else 2
    #         wall_y = 0 if head_y == 0 else 1 if head_y == helper.GRID_SIZE - 1 else 2

    #         # Food direction
    #         food_dir_x = 0 if food_x < head_x else 1 if food_x > head_x else 2
    #         food_dir_y = 0 if food_y < head_y else 1 if food_y > head_y else 2

    #         # Adjoining body states
    #         body_top = 1 if (head_x, head_y - 1) in body else 0
    #         body_bottom = 1 if (head_x, head_y + 1) in body else 0
    #         body_left = 1 if (head_x - 1, head_y) in body else 0
    #         body_right = 1 if (head_x + 1, head_y) in body else 0

    #         # Update q_table_state
    #         q_table_state = [wall_x, wall_y, food_dir_x, food_dir_y, body_top, body_bottom, body_left, body_right]



    #         # update q table using lr, reward, and gamma 
    #         learning_rate = 0.7
    #         reward = self.compute_reward(points, dead)
    #         def q_training(learning_rate, reward, q_table_state):
    #             # update q table for previous state
    #             if self.s is not None: #bc for first call it will be Null
    #                 # print("self.s:", self.s)
    #                 # print("self.a:", self.a)
    #                 self.N[self.s][self.a] += 1
    #                 max_q = np.max(self.Q[q_table_state])
    #                 self.Q[self.s][self.a] += learning_rate * (reward + self.gamma * max_q - self.Q[self.s][self.a])
            
    #             # now pick an action for current state to take
    #             possible_actions = self.helper_func(state) # now that we did calculations with self.s, we can call this which updates self.s
    #             if random.uniform(0, 1) < self.Ne:
    #                 action = random.choice(possible_actions)  # Explore
    #             else: #pick highest Q valued action
    #                 action = np.max(self.Q[q_table_state])
    #             return action
            
    #         # update q-table
    #         action = q_training(learning_rate, reward, q_table_state)
    #         self.save_model()
            

    #     else:
    #     # if we are in test, do not update q table
    #         # get all valid actions (helper_func)
    #         # use the exisitng q table to look up corresponding q values for all actions
    #         # return the aciton with the highest q-value
    #         possible_actions = self.helper_func(state) # call this which updates self.s
    #         action = np.max(self.Q[self.s]) # not sure if you need to pick one of the values returned by helper_func?

    #     return action

        # returns which action to take 0, 1, 2, or 3
        # 0 is move down, 1 is move up, 2 is move left, 3 is move right







    # def agent_action(self, state, points, dead):
    #     # Unpack state components
    #     head_x, head_y, body, food_x, food_y = state

    #     # Convert state to a unique hashable key for indexing

    #     # Compute the reward for the current state
    #     reward = self.compute_reward(points, dead)

    #     # If the agent was previously in a state and took an action
    #     if self.s is not None and self.a is not None and self._train:
    #         max_q_next = max(self.Q[state_key][a] for a in self.actions)
    #         learning_rate = self.LPC / (self.LPC + self.N[self.s][self.a])
    #         self.Q[self.s][self.a] += learning_rate * (
    #             reward + self.gamma * max_q_next - self.Q[self.s][self.a]
    #         )

    #     # If the game is over, reset state and action
    #     if dead:
    #         self.reset()
    #         return random.choice(self.actions)

    #     # Get valid actions for the current state
    #     valid_actions = self.helper_func(state)

    #     # Decide next action using epsilon-greedy
    #     if random.uniform(0, 1) < self.Ne / (self.Ne + self.N[state_key][0]):
    #         action = random.choice(valid_actions)  # Explore
    #     else:
    #         action = max(valid_actions, key=lambda a: self.Q[state_key][a])  # Exploit

    #     # Update the visit count for the state-action pair
    #     if self._train:
    #         self.N[state_key][action] += 1

    #     # Save the current state and action
    #     self.s = state_key
    #     self.a = action

    #     return action
