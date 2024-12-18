import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.ticker import FormatStrFormatter


plt.rcParams['text.usetex'] = True
plt.rcParams['font.size'] = 20
plt.rcParams['font.family'] = 'serif'

# Load data
data = pd.read_csv('ablation_whole-domain_L2_PM.csv')
plt.figure(figsize=(5, 4))
plt.plot(data['x'], data['PM'], label='PM', linewidth=2, linestyle='-', color=[0, 0, 1], marker='+', markersize=8, markevery=2)
plt.plot(data['x'], data['Optimal'], label='OGPM on [-1,1)', linewidth=2, linestyle='-', color=[1, 0, 0])
plt.xlabel(r'Input $x$')
plt.ylabel(r'Absolute error')
plt.xticks(np.arange(-1, 1.1, 0.5))
plt.yticks(np.arange(0, 0.32, 0.1))
plt.ylim(0.01, 0.32)
plt.gca().xaxis.set_major_formatter(FormatStrFormatter('%g'))
plt.gca().yaxis.set_major_formatter(FormatStrFormatter('%g'))
leg = plt.legend(loc='upper right')
for i, test in enumerate(leg.get_texts()):
    if i == 3:
        test.set_fontsize(14)

plt.savefig('ablation_PM.pdf', bbox_inches='tight')
plt.show()


# Load data
data = pd.read_csv('ablation_whole-domain_l2_SW.csv')
plt.figure(figsize=(5, 4))
plt.plot(data['x'], data['SW'], label='SW', linewidth=2, linestyle='--', color=[0, 0, 0])
plt.plot(data['x'], data['Optimal'], label='OGPM', linewidth=2, linestyle='-', color=[1, 0, 0])
plt.xlabel(r'Input $x$')
plt.ylabel(r'Absolute error')
plt.xticks(np.arange(0, 1.1, 0.2))
plt.yticks(np.arange(0, 0.11, 0.1))
plt.ylim(0.01, 0.11)
plt.gca().xaxis.set_major_formatter(FormatStrFormatter('%g'))
plt.gca().yaxis.set_major_formatter(FormatStrFormatter('%g'))
leg = plt.legend(loc='upper right')
for i, test in enumerate(leg.get_texts()):
    if i == 3:
        test.set_fontsize(14)

plt.savefig('ablation_SW.pdf', bbox_inches='tight')
plt.show()

