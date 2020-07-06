# -*- coding: utf-8 -*-
import numpy as np
from configs import comission, PRICE_MAG


class environment:
    def __init__(self, data_frame, leng):
        self.big_data = data_frame.values
        self.len = leng
        self.start_len = self.big_data.shape[0] - leng
        #print(self.start_len, leng)
        start_point = int(np.random.rand() * self.start_len)
        self.data = self.big_data[start_point:start_point + leng, :]
        # close_prices
        self.prices = self.data[:, 3]
        self.iter = 0
        self.n_shares = 0
        self.cash = 0
        self.max_shares = 1
        self.max_iter = self.prices.shape[0]
        self.done = False
        self.prev_equity = 0
        self.equity = 0
        self.comission = comission
        self.same_steps = 0
        self.prev_act = 0

    def calc_reward(self, act):
        # if(act != self.n_shares
        # if abs(self.n_shares + act) <= self.max_shares:
        # print(PRICE_MAG)
        if(self.n_shares != act):
            self.cash = self.cash - self.prices[self.iter - 1] * \
                (act - self.n_shares) - self.comission * PRICE_MAG * (1 + 0 * (self.same_steps < 3))
        self.n_shares = act
        self.equity = self.cash + self.prices[self.iter] * self.n_shares
        reward = self.equity - self.prev_equity
        self.prev_equity = self.equity
        return reward - self.comission * PRICE_MAG * (int(self.same_steps / 1000))

    def step(self, act):
        if not self.done:
            self.iter += 1

        observation = self.data[self.iter]
        reward = self.calc_reward(act)

        self.same_steps += 1
        if act != self.prev_act:
            self.same_steps = 0

        if self.iter >= self.max_iter - 1:
            self.done = True
        else:
            self.done = False
        self.prev_act = act
        return observation, reward, self.done, self.n_shares

    def reset(self):
        self.iter = 0
        self.done = False
        start_point = int(np.random.rand() * self.start_len)
        self.data = self.big_data[start_point:start_point + self.len, :]
        observation = self.data[self.iter]
        self.prices = self.data[:, 3]
        self.n_shares = 0
        self.cash = 0
        self.prev_equity = 0
        self.equity = 0
        return observation

    def sample(self):
        return np.random.randint(0, 3)
