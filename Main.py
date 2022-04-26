import random
import torch
import numpy as np
from collections import deque
from Game import BlackJack

MEMORY_SIZE = 100_000
BATCH_SIZE = 64

class Deep_Q_Network(torch.nn.Module):
    def __init__(self, lr, input_size, hidden_size_one, hidden_size_two, actions):
        super(Deep_Q_Network, self).__init__()
        self.linear1 = torch.nn.Linear(*input_size, hidden_size_one)
        self.linear2 = torch.nn.Linear(hidden_size_one, hidden_size_two)
        self.linear3 = torch.nn.Linear(hidden_size_two, actions)
        self.optimizer = torch.optim.Adam(self.parameters(), lr=lr)
        self.loss = torch.nn.MSELoss()

    def forward(self, state):
        x = torch.nn.functional.relu(self.linear1(state))
        x = torch.nn.functional.relu(self.linear2(x))
        actions = self.linear3(x)
        return actions


class Agent():
    def __init__(self, input_size, actions):
        self.gamma = 0.99
        self.epsilon = 1.0
        self.epsilon_min = 0.01
        self.epsilon_decrement = 5e-4
        self.action_space = []
        for i in range(actions):
            self.action_space.append(i)
        self.mem_size = MEMORY_SIZE
        self.batch_size = BATCH_SIZE
        self.memory = deque(maxlen=self.mem_size)
        self.model = Deep_Q_Network(lr=0.001, actions=actions, input_size=input_size, hidden_size_one=256, hidden_size_two=256)

    def store_memory(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def choose_action(self, input_state):
        if np.random.random() > self.epsilon:
            state = torch.tensor([input_state])
            actions = self.model.forward(state)
            action = torch.argmax(actions).item()
        else:
            action = np.random.choice(self.action_space)
        return action

    def train(self):
        if len(self.memory) < self.batch_size:
            return
        elif len(self.memory) > self.batch_size:
            sample = random.sample(self.memory, self.batch_size)
        else:
            sample = self.memory
        states, actions, rewards, next_states, dones = zip(*sample)
        batch_index = np.arange(self.batch_size, dtype=np.int32)

        self.model.optimizer.zero_grad()

        states = torch.tensor(states, dtype=torch.float32)
        new_states = torch.tensor(next_states, dtype=torch.float32)
        rewards = torch.tensor(rewards, dtype=torch.float32)
        dones = torch.tensor(dones, dtype=torch.bool)
        actions = actions

        evaluate = self.model.forward(states)[batch_index, actions]
        next = self.model.forward(new_states)
        next[dones] = 0.0
        target = rewards + self.gamma * torch.max(next, dim=1)[0]
        loss = self.model.loss(target, evaluate)
        loss.backward()
        self.model.optimizer.step()

        if self.epsilon > self.epsilon_min:
            self.epsilon = self.epsilon - self.epsilon_decrement
        else:
            self.epsilon = self.epsilon_min


def save_policy_map(policy_map, file_name):
    with open(file_name, 'w') as f:
        f.write(',Ace,2,3,4,5,6,7,8,9,10\n')
        for index_x, x in enumerate(policy_map):
            f.write(str(index_x+4) + ',')
            for index_y, y in enumerate(x):
                f.write(y)
                if index_y < 11:
                    f.write(',')
            f.write('\n')

def make_state(dealer, player):
    state = []
    if dealer <= 21:
        state.append((dealer/21))
    else:
        state.append(0)
    if player <= 21:
        state.append((player/21))
    else:
        state.append(0)
    return state

def build_map(agent):
    blakcjack_map = []
    for x in range(18):
        temp_row = []
        for y in range(10):
            action = agent.choose_action(make_state(y+1, x+4))
            if action == 1:
                temp_row.append('Hit')
            else:
                temp_row.append('Stand')
        blakcjack_map.append(temp_row)

    return blakcjack_map

def build_map_random():
    blakcjack_map = []
    for x in range(18):
        temp_row = []
        for y in range(10):
            action = action = random.randint(0, 1)
            if action == 1:
                temp_row.append('Hit')
            else:
                temp_row.append('Stand')
        blakcjack_map.append(temp_row)

    return blakcjack_map

def Train_BlackJack_DQL(n_games):
    file = open('./data/BlackJack_DQL.csv', 'w')
    file.close()
    wins, losses, ties = 0, 0, 0
    agent = Agent(input_size=[2], actions=2)
    game = BlackJack()
    for i in range(1, n_games+1):
        score = 0
        done = False
        state = game.get_game_state()
        while not done:
            action = agent.choose_action(state)
            reward, done, tie = game.play(action)
            next_state = game.get_game_state()
            score += reward
            agent.store_memory(state, action, reward, next_state, done)
            agent.train()
            state = next_state
        game.next_game()
        if score == 100 and tie:
            ties += 1
        elif score == 100 and not tie:
            wins += 1
        else:
            losses += 1
        with open('./data/BlackJack_DQL.csv', 'a') as f:
            f.write('{},{},{},{}\n'.format(i, wins/i*100, losses/i*100, ties/i*100))
        if i % 1000 == 0 and i > 0:
            print('Game #: {} Win(%): {:.2f} Loss(%): {:.2f} Ties(%): {:.2f}'.format(i, wins/i*100, losses/i*100, ties/i*100))
        # UNCOMMENT TO BUILD NEW POLICY MAP AT THE END OF EVERY GAME
        # INCREASES RUN TIME BY A LOT!
        # BlackJack_map = build_map(agent)
        # save_policy_map(BlackJack_map, './data/BlackJack_DQL_map.csv')
    BlackJack_map = build_map(agent)
    save_policy_map(BlackJack_map, './data/BlackJack_DQL_map.csv')

def Train_BlackJack_Random(n_games):
    file = open('./data/BlackJack_Random.csv', 'w')
    file.close()
    wins, losses, ties = 0, 0, 0
    game = BlackJack()
    for i in range(1, n_games+1):
        score = 0
        done = False
        while not done:
            action = random.randint(0, 1)
            reward, done, tie = game.play(action)
            score += reward
        game.next_game()
        if score == 100 and tie:
            ties += 1
        elif score == 100 and not tie:
            wins += 1
        else:
            losses += 1
        with open('./data/BlackJack_Random.csv', 'a') as f:
            f.write('{},{},{},{}\n'.format(i, wins/i*100, losses/i*100, ties/i*100))
        if i % 1000 == 0 and i > 0:
            print('Game #: {} Win(%): {:.2f} Loss(%): {:.2f} Ties(%): {:.2f}'.format(i, wins/i*100, losses/i*100, ties/i*100))
        # UNCOMMENT TO BUILD NEW POLICY MAP AT THE END OF EVERY GAME
        # INCREASES RUN TIME BY A LOT!
        # BlackJack_map = build_map_random()
        # save_policy_map(BlackJack_map, 'BlackJack_Random_map.csv')
    BlackJack_map = build_map_random()
    save_policy_map(BlackJack_map, './data/BlackJack_Random_map.csv')

def main():
    n_games = input("How many games do you want to simulate: ")
    # Train_BlackJack_Random(n_games)
    Train_BlackJack_DQL(n_games)

if __name__ == '__main__':
    main()