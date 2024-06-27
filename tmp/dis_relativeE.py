import matplotlib.pyplot as plt
import numpy as np

barWidth = 0.25
FontSize = 20
Fontfamily = 'times new roman'

a_pro = [78.2281489684941, 4.89057557494785, 0.493662272279925, 0.0488900347875136]
a_rr = [57.5429448038358, 5.63201338296508, 0.564707574162816, 0.0539988279940831]
k_pro = [81.5320551704137, 5.04692523187857, 0.511622414096154, 0.0731157721538022]
k_rr = [90.8115310436241, 8.63214675048731, 0.906923465690934, 0.0856511107282681]
i_pro = [117.745495688143, 7.64410345980691, 0.706746974811328, 0.0736464380558835]
i_rr = [87.8914850682176, 8.79351348688869, 0.887597847237724, 0.0844964541845403]
ec_pro = [22.9599810192462, 1.40339588263263, 0.142383117976473, 0.0163159682981944]
ec_rr = [17.3658532292413, 1.76310284695425, 0.176202596693606, 0.0170616608080439]


# # #############------------e=0.001--------------#################
# bar1 = [k_pro[0], a_pro[0], ec_pro[0], i_pro[0]]  # with shortest path
# bar2 = [k_rr[0], a_rr[0], ec_rr[0], i_rr[0]]
#
# print(bar1)
# print(bar2)
#
# r1 = np.arange(len(bar1))
# r2 = [x + barWidth for x in r1]
# plt.bar(r1, bar1, width=barWidth, align='center', color=[1, 0.2, 0], edgecolor='black', hatch="//", linewidth=1.2,
#         label='JRR')
# plt.bar(r2, bar2, width=barWidth, align='center', color=[0, 0.5, 1], edgecolor='black', linewidth=1.2, label='RR')
#
# plt.xticks([r + barWidth for r in range(len(bar1))], ['Kosarak', 'Amazon', 'EC', 'Census'], fontsize=FontSize)
# plt.yticks([0, 20, 40, 60, 80, 100], ['0', '20', '40', '60', '80', '100'], fontsize=FontSize)
# plt.legend(fontsize=FontSize - 1, frameon=True, edgecolor='black', loc='best')
# plt.ylabel("ARE", fontsize=FontSize)
#
# plt.subplots_adjust(left=0.15)
# plt.savefig('./figure/re_real_e0001.pdf', dpi=300, bbox_inches='tight')
# plt.show()


# # #############------------e=0.01--------------#################
bar1 = [k_pro[1], a_pro[1], ec_pro[1], i_pro[1]]  # with shortest path
bar2 = [k_rr[1], a_rr[1], ec_rr[1], i_rr[1]]

print(bar1)
print(bar2)

r1 = np.arange(len(bar1))
r2 = [x + barWidth for x in r1]
plt.bar(r1, bar1, width=barWidth, align='center', color=[1, 0.2, 0], edgecolor='black', hatch="//", linewidth=1.2, label='JRR')
plt.bar(r2, bar2, width=barWidth, align='center', color=[0, 0.5, 1], edgecolor='black', linewidth=1.2, label='RR')

plt.xticks([r + barWidth for r in range(len(bar1))], ['Kosarak', 'Amazon', 'EC', 'Census'], fontsize=FontSize, fontname=Fontfamily)
plt.yticks([0, 2, 4, 6, 8, 10], ['0', '2', '4', '6', '8', '10'], fontsize=FontSize, fontname=Fontfamily)
plt.legend(fontsize=FontSize - 1, frameon=True, edgecolor='black', loc='best')
plt.ylabel("ARE", fontsize=FontSize, fontname=Fontfamily)

plt.subplots_adjust(left=0.15)
plt.savefig('./ARE_e001.pdf', bbox_inches='tight')
plt.show()


# # #############------------e=0.1--------------#################
bar1 = [k_pro[2], a_pro[2], ec_pro[2], i_pro[2]]  # with shortest path
bar2 = [k_rr[2], a_rr[2], ec_rr[2], i_rr[2]]
#
print(bar1)
print(bar2)

r1 = np.arange(len(bar1))
r2 = [x + barWidth for x in r1]
plt.bar(r1, bar1, width=barWidth, align='center', color=[1, 0.2, 0], edgecolor='black', hatch="//", linewidth=1.2,
        label='JRR')
plt.bar(r2, bar2, width=barWidth, align='center', color=[0, 0.5, 1], edgecolor='black', linewidth=1.2, label='RR')

plt.xticks([r + barWidth for r in range(len(bar1))], ['Kosarak', 'Amazon', 'EC', 'Census'], fontsize=FontSize, fontname=Fontfamily)
plt.yticks([0, 0.2, 0.4, 0.6, 0.8, 1], ['0', '0.2', '0.4', '0.6', '0.8', '1'], fontsize=FontSize, fontname=Fontfamily)
plt.legend(fontsize=FontSize - 1, frameon=True, edgecolor='black', loc='best')
plt.ylabel("ARE", fontsize=FontSize, fontname=Fontfamily)

plt.subplots_adjust(left=0.15)
plt.savefig('./ARE_e01.pdf', bbox_inches='tight')
plt.show()


##############------------e=1--------------#################
bar1 = [k_pro[3], a_pro[3], ec_pro[3], i_pro[3]]  # with shortest path
bar2 = [k_rr[3], a_rr[3], ec_rr[3], i_rr[3]]

print(bar1)
print(bar2)

r1 = np.arange(len(bar1))
r2 = [x + barWidth for x in r1]
plt.bar(r1, bar1, width=barWidth, align='center', color=[1, 0.2, 0], edgecolor='black', hatch="//", linewidth=1.2,
        label='JRR')
plt.bar(r2, bar2, width=barWidth, align='center', color=[0, 0.5, 1], edgecolor='black', linewidth=1.2, label='RR')

plt.xticks([r + barWidth for r in range(len(bar1))], ['Kosarak', 'Amazon', 'EC', 'Census'], fontsize=FontSize, fontname=Fontfamily)
plt.yticks([0, 0.02, 0.04, 0.06, 0.08, 0.1], ['0', '0.02', '0.04', '0.06', '0.08', '0.1'], fontsize=FontSize, fontname=Fontfamily)
plt.legend(fontsize=FontSize - 1, frameon=True, edgecolor='black', loc='best')
plt.ylabel("ARE", fontsize=FontSize, fontname=Fontfamily)

plt.subplots_adjust(left=0.15)
plt.savefig('./ARE_e1.pdf', bbox_inches='tight')
plt.show()


