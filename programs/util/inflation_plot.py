#!/usr/bin/env python3

import datetime
import json
import sys

import numpy
import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator

x = []
y = []
y2 = []
y3 = []
y4 = []
y5 = []
y6 = []
y7 = []
y8 = []
y9 = []
y10 = []
y11 = []

names = ["Curator", "Content", "Producer", "Liquidity", "PoW"]
inflections = {}
markers = []

colors = iter("mgbr")
shapes = iter("ovx+")

ax = plt.gca()

plt.axis([0, 1, 10e6, 5e9])
ax.set_xticks(range(13))
ax.set_yscale("log")
ax.tick_params(axis="y", which="minor", left="off", right="off")
ax.tick_params(axis="y2", which="minor", left="off", right="off")
ax.tick_params(axis="y3", which="minor", left="off", right="off")
ax.tick_params(axis="y4", which="minor", left="off", right="off")
ax.tick_params(axis="y5", which="minor", left="off", right="off")
ax.tick_params(axis="y6", which="minor", left="off", right="off")
ax.tick_params(axis="y7", which="minor", left="off", right="off")
ax.tick_params(axis="y8", which="minor", left="off", right="off")
ax.tick_params(axis="y9", which="minor", left="off", right="off")
ax.tick_params(axis="y10", which="minor", left="off", right="off")
ax.tick_params(axis="y11", which="minor", left="off", right="off")
ax.set_yticks([1e6, 10e6, 20e6, 30e6, 40e6, 50e6, 60e6, 70e6, 80e6])
ax.set_yticklabels(["1M", "10M", "20M", "30M", "40M", "50M", "60M", "70M"])
ax.set_ylabel("Supply [GOLOS]")
ax.set_xlabel("Time [Months]")
plt.grid(True, which="major", linestyle="-")

BLOCKS_PER_YEAR = 20*60*24*365
BLOCKS_PER_MONTH = BLOCKS_PER_YEAR / 12.0

with open(sys.argv[1], "r") as f:
    n = 0
    for line in f:
        n += 1
        d = json.loads(line)
        block = int(d["b"])
        total_supply = int(d["s"])

        curation_rewards = int(d['rvec'][0])/1000.0
        vesting_rewards_balancing_curation_rewards = int(d['rvec'][1])/1000.0
        content_rewards = int(d['rvec'][2])/1000.0
        vesting_rewards_balancing_content_rewards = int(d['rvec'][3])/1000.0
        producer_rewards = int(d['rvec'][4])/1000.0
        vesting_rewards_balancing_producer_rewards = int(d['rvec'][5])/1000.0
        liquidity_rewards = int(d['rvec'][6])/1000.0
        vesting_rewards_balancing_liquidity_rewards = int(d['rvec'][7])/1000.0
        pow_rewards = int(d['rvec'][8])/1000.0
        vesting_rewards_balancing_pow_rewards = int(d['rvec'][9])/1000.0

        px = block / float(BLOCKS_PER_MONTH)
        py = total_supply / 1000.0
        x.append(px)
        y.append(py)
        y2.append(curation_rewards)
        y3.append(vesting_rewards_balancing_curation_rewards)
        y4.append(content_rewards)
        y5.append(vesting_rewards_balancing_content_rewards)
        y6.append(producer_rewards)
        y7.append(vesting_rewards_balancing_producer_rewards)
        y8.append(liquidity_rewards)
        y9.append(vesting_rewards_balancing_liquidity_rewards)
        y10.append(pow_rewards)
        y11.append(vesting_rewards_balancing_pow_rewards)

        for i in range(len(names)):
            if i == 1:
                continue
            if names[i] in inflections:
                continue
            if (int(d["rvec"][i*2]) % 1000) == 0:
                continue
            inflections[names[i]] = d["b"]
            markers.append([[[px], [py], next(colors)+next(shapes)], {"label": "Starting of "+names[i]}])

        if block > BLOCKS_PER_YEAR:
            break

plt.plot(x, y, label='Total Supply')
plt.plot(x, y2, label='Curation rewards')
plt.plot(x, y3, label='Vesting rewards balancing curation rewards')
plt.plot(x, y4, linestyle=":", label='Content rewards')
plt.plot(x, y5, linestyle=":", label='Vesting rewards balancing content rewards')
plt.plot(x, y6, label='Producer rewards')
plt.plot(x, y7, label='Vesting rewards balancing producer rewards')
plt.plot(x, y8, linestyle=":", label='Liquidity rewards')
plt.plot(x, y9, linestyle=":", label='Vesting rewards balancing liquidity rewards')
plt.plot(x, y10, linestyle=":", label='PoW rewards')
plt.plot(x, y11, linestyle=":", label='Vesting rewards balancing PoW rewards')
for m in markers:
    print(m)
    plt.plot(*m[0], **m[1])
lgd = plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
plt.title("First year GOLOS supply projection from inflation model")
plt.savefig('supply.png', dpi=150, format='png', bbox_extra_artists=(lgd,), bbox_inches='tight')
