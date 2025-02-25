import random as rd
import numpy as np

class node:

    def __init__(self, id, wealth):
        self.id = id
        self.wealth = wealth
        self.stake = 0
        self.blocks = rd.random()*100
        self.stakers = {}
        # game theory variables
        self.greed = rd.random()
        self.popularity = rd.random()

    def add_wealth(self, reward):
        self.wealth += reward

    def add_blocks(self, num_blocks):
        self.blocks += num_blocks

    def adjust_greed(self, adjustment):
        if self.greed * adjustment < 1:
            self.greed *= adjustment
    
    def adjust_popularity(self, adjustment):
        if self.popularity * adjustment < 1:
            self.popularity *= adjustment

    # node reputation is number of blocks mined times popularity
    def reputation(self):
        return self.blocks * self.popularity

    # determine how much wealth to use in order to participate based off self greed
    def participate(self, cost):
        self.stake = 0
        adjustment = 1
        while self.wealth > cost:
            if rd.random() > (self.greed / adjustment):
                break
            self.wealth -= cost
            self.stake += 1
            adjustment += 1
        return self.stake * cost

    # delegate stake to another node with amount based on self greed
    def vote(self, node):
        node.stakers[self] = self.greed * self.wealth

    # adjusts another node's popularity based on gained reward and self greed
    # TODO: investigate whether we can use a mixed strategy nash equilibrium game to determine delegate and staker behavior
    def opinion(self, node, reward):
        if (reward / self.wealth) < self.greed:
            node.adjust_popularity(0.995)
        else:
            node.adjust_popularity(1.0001)
        
    # reflect on ones self
    # TODO: investigate sharp ratio to calculate risk/greed adjustments
    def reflect(self):
        # lower self greed if popularity gets too low
        if (self.popularity < (1 - self.greed)):
            self.adjust_greed(.80)
        # increase greed when popularity is high enough
        else:
            self.adjust_greed(1.05)

    # sum of wealth staked on self
    def sum_stakers(self):
        return sum(self.stakers.values())

class network:

    def __init__(self, num_nodes):
        self.nodes = []
        self.num_nodes = num_nodes
        self.normal_distribution()
        self.prize_pool = 0

    def number_of_nodes(self):
        return self.num_nodes

    def gini_coefficient(self):
        """Compute Gini coefficient of array of values"""
        x = np.array([n.wealth for n in self.nodes])
        diffsum = 0
        for i, xi in enumerate(x[:-1], 1):
            diffsum += np.sum(np.abs(xi - x[i:]))
        return diffsum / (len(x)**2 * np.mean(x))

    def real_distribution(self):
        for low in range(int(self.num_nodes*0.8)):
            wealth = np.random.normal(loc=10, scale=2)
            self.nodes.append(node(low, wealth))
        for med in range(int(self.num_nodes*0.15)):
            wealth = np.random.normal(loc=100, scale=10)
            self.nodes.append(node(int(self.num_nodes*0.8)+med, wealth))
        for high in range(int(self.num_nodes*0.05)):
            wealth = 1000
            self.nodes.append(node(int(self.num_nodes*0.95)+high, wealth))

    def normal_distribution(self):
        for i in range(self.num_nodes):
            wealth = np.random.normal(loc=100, scale = 10)
            self.nodes.append(node(i, wealth))

    def participants(self, cost):
        self.prize_pool = 20
        participants = []
        for n in self.nodes:
            self.prize_pool += n.participate(cost)
            if (n.stake > 0):
                participants.append(n)
        return participants


