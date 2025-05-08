import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.ticker import FormatStrFormatter


plt.rcParams['text.usetex'] = True
plt.rcParams['font.size'] = 20
plt.rcParams['font.family'] = 'serif'


# Load data
data = pd.read_csv('worst-case_L1.csv')
plt.figure(figsize=(5, 4))
plt.plot(data['Epsilon'], data['Staircase'], label='Staircase', linewidth=2, linestyle='--', color=[0, 0, 0])
plt.plot(data['Epsilon'], data['Truncated Laplace'], label='T-Laplace', linewidth=2, linestyle='-', color=[0, 0, 1], marker='+', markersize=8)
plt.plot(data['Epsilon'], data['GPM'], label='OGPM', linewidth=2, linestyle='-', color=[1, 0, 0])
plt.xlabel(r'Privacy parameter $\varepsilon$')
plt.ylabel(r'Worst-case square error')
plt.xticks(np.arange(1, 9, 1))
plt.yticks(np.arange(0, 1, 0.2))
plt.ylim(0, 1)
plt.gca().xaxis.set_major_formatter(FormatStrFormatter('%g'))
plt.gca().yaxis.set_major_formatter(FormatStrFormatter('%g'))
leg = plt.legend(loc='upper right')
# for i, test in enumerate(leg.get_texts()):
#     if i == 3:
#         test.set_fontsize(14)

plt.savefig('worst-case_L1.pdf', bbox_inches='tight')
plt.show()
