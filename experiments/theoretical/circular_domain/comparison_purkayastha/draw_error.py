import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.ticker import FormatStrFormatter

plt.rcParams['font.size'] = 20
plt.rcParams['font.family'] = 'serif'

# Load data
data = pd.read_csv('comparison_purkayastha_mechanism.csv')
plt.figure(figsize=(5, 4))
plt.plot(data['Epsilon'], data['PurKayastha'], label=r'Pur$(n=2,\kappa)$',linewidth=2, linestyle='-', color=[0, 0, 1], marker='+', markersize=8)
plt.plot(data['Epsilon'], data['OGPM'], label='OGPM', linewidth=2, linestyle='-', color=[1, 0, 0])
plt.xlabel(r'Privacy parameter $\varepsilon$')
plt.xticks(np.arange(1, 9, 1))
plt.yticks(np.arange(0, 1.6, 0.5))
plt.legend(loc='upper right')
plt.gca().xaxis.set_major_formatter(FormatStrFormatter('%g'))
plt.gca().yaxis.set_major_formatter(FormatStrFormatter('%.1f'))

plt.savefig('comparison_purkayastha.pdf', bbox_inches='tight')
plt.show()
