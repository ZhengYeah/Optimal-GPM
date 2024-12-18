import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.ticker import FormatStrFormatter


plt.rcParams['text.usetex'] = True
plt.rcParams['font.size'] = 20
plt.rcParams['font.family'] = 'serif'

# Load data
data = pd.read_csv('whole-domain_circular_L2_epsilon_2.csv')

fig, ax = plt.subplots()
fig.set_size_inches(5, 4)
fig.canvas.draw()

ax.plot(data['x'], data['SW'], label='SW-C', linewidth=2, linestyle='--', color=[0, 0, 0])
ax.plot(data['x'], data['PM'], label='PM-C', linewidth=2, linestyle='-', color=[0, 0, 1], marker='+', markersize=8, markevery=2)
ax.plot(data['x'], data['Optimal'], label='OGPM', linewidth=2, linestyle='-', color=[1, 0, 0])
ax.set_xlabel(r'Input $x$')
ax.set_ylabel(r'Absolute error')
ax.set_xticks([0, 1.57, 3.14, 4.71, 6.28])
ax.set_xticklabels(['$0$', r'$\pi/2$', r'$\pi$', r'$3\pi/2$', r'$2\pi$'])
ax.set_yticks(np.arange(0, 6.1, 2))
ax.set_ylim(0.1, 6.1)
ax.legend(loc='upper right')
fig.gca().yaxis.set_major_formatter(FormatStrFormatter('%.1f'))

plt.savefig('whole-domain_circular_L2_epsilon_2.pdf', bbox_inches='tight')
plt.show()


# Load data
data = pd.read_csv('whole-domain_circular_L2_epsilon_4.csv')

fig, ax = plt.subplots()
fig.set_size_inches(5, 4)
fig.canvas.draw()

ax.plot(data['x'], data['SW'], label='SW-C', linewidth=2, linestyle='--', color=[0, 0, 0])
ax.plot(data['x'], data['PM'], label='PM-C', linewidth=2, linestyle='-', color=[0, 0, 1], marker='+', markersize=8, markevery=2)
ax.plot(data['x'], data['Optimal'], label='OGPM', linewidth=2, linestyle='-', color=[1, 0, 0])
ax.set_xlabel(r'Input $x$')
ax.set_ylabel(r'Absolute error')
ax.set_xticks([0, 1.57, 3.14, 4.71, 6.28])
ax.set_xticklabels(['$0$', r'$\pi/2$', r'$\pi$', r'$3\pi/2$', r'$2\pi$'])
ax.set_yticks(np.arange(0, 4.1, 1))
ax.set_ylim(0.1, 4.1)
ax.legend(loc='upper right')
fig.gca().yaxis.set_major_formatter(FormatStrFormatter('%.1f'))

plt.savefig('whole-domain_circular_L2_epsilon_4.pdf', bbox_inches='tight')
plt.show()



