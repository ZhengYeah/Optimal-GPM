import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.ticker import FormatStrFormatter


plt.rcParams['text.usetex'] = True
plt.rcParams['font.size'] = 20
plt.rcParams['font.family'] = 'serif'

# Load data
data = pd.read_csv('epsilon_2.csv')
plt.figure(figsize=(5, 4))
plt.plot(data['x'], data['Staircase'], label='Staircase', linewidth=2, linestyle='--', color=[0, 0, 0])
plt.plot(data['x'], data['Truncated Laplace'], label='T-Laplace', linewidth=2, linestyle='-', color=[0, 0, 1], marker='+', markersize=8, markevery=2)
plt.plot(data['x'], data['GPM'], label='OGPM', linewidth=2, linestyle='-', color=[1, 0, 0])
plt.xlabel(r'Input $x$')
plt.ylabel(r'Absolute error')
plt.xticks(np.arange(0, 1.1, 0.2))
plt.yticks(np.arange(0, 0.45, 0.1))
plt.ylim(0, 0.45)
plt.gca().xaxis.set_major_formatter(FormatStrFormatter('%g'))
plt.gca().yaxis.set_major_formatter(FormatStrFormatter('%g'))
leg = plt.legend(loc='lower right')
# for i, test in enumerate(leg.get_texts()):
#     if i == 3:
#         test.set_fontsize(14)

plt.savefig(f"epsilon_2.pdf", bbox_inches='tight')
plt.show()

# Load data
data = pd.read_csv('epsilon_4.csv')
plt.figure(figsize=(5, 4))
plt.plot(data['x'], data['Staircase'], label='Staircase', linewidth=2, linestyle='--', color=[0, 0, 0])
plt.plot(data['x'], data['Truncated Laplace'], label='T-Laplace', linewidth=2, linestyle='-', color=[0, 0, 1], marker='+', markersize=8, markevery=2)
plt.plot(data['x'], data['GPM'], label='OGPM', linewidth=2, linestyle='-', color=[1, 0, 0])
plt.xlabel(r'Input $x$')
plt.ylabel(r'Absolute error')
plt.xticks(np.arange(0, 1.1, 0.2))
plt.yticks(np.arange(0, 0.25, 0.1))
plt.ylim(0, 0.25)
plt.gca().xaxis.set_major_formatter(FormatStrFormatter('%g'))
plt.gca().yaxis.set_major_formatter(FormatStrFormatter('%g'))
leg = plt.legend(loc='lower right')
# for i, test in enumerate(leg.get_texts()):
#     if i == 3:
#         test.set_fontsize(14)

plt.savefig(f"epsilon_4.pdf", bbox_inches='tight')
plt.show()