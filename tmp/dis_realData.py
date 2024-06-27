import matplotlib.pyplot as plt
import numpy as np

barWidth = 0.25
FontSize = 20
Fontfamily = 'times new roman'

# a_pro = [2675132033.30359, 29392128.3724246, 351886.422467621, 6972.33636068702]
# a_rr = [10035841725.1045, 100206595.808765, 940273.899004859, 9706.86253553852]
# k_pro = [2521765354.26053, 27324379.6959456, 427108.199057503, 11454.4006531409]
# k_rr = [18551727771.9693, 193099867.424561, 2112163.53974199, 17463.6265933623]
# i_pro = [1870299287.93583, 18408334.5458859, 253357.966596286, 6306.09500655079]
# i_rr = [9628451139.82335, 98351026.2855308, 1027573.11530725, 9654.45804491267]
# ec_pro = [13372080587.1103, 144333800.628890, 1466627.40491622, 19867.4848573547]
# ec_rr = [23821285359.6625, 219351443.712571, 2269198.88592151, 19513.0527192711]

a_pro = [19573358601.3907, 73152367.7380787, 757893.082303798, 7257.72789067730]
a_rr = [10280131102.5357, 99751004.0705677, 1017996.90792956, 8983.52508049613]
k_pro = [17438109916.4321, 64325434.6187716, 656134.414509742, 13090.0020032263]
k_rr = [21182875363.6019, 189022530.557395, 2060494.02243202, 18251.4422447068]
i_pro = [17818761701.1502, 73539813.2555514, 656683.119792138, 6829.31868848685]
i_rr = [10061970475.6284, 98297777.0814678, 977368.215293171, 9060.90767690803]
ec_pro = [38466718875.7260, 150639799.675067, 1547989.50634270, 19756.2695699713]
ec_rr = [22870085891.8243, 225711866.436592, 2331797.42402949, 21577.4091087713]

# ############------------e=0.001--------------#################
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
# # plt.yscale('log')
# plt.xticks([r + barWidth for r in range(len(bar1))], ['Kosarak', 'Amazon', 'EC', 'Census'], fontsize=FontSize)
# plt.yticks([0, 5e9, 1e10, 1.5e10, 2e10, 2.5e10], ['0', '0.5', '1', '1.5', '2', '2.5'], fontsize=FontSize)
# plt.legend(fontsize=FontSize - 1, frameon=True, edgecolor='black', loc='best')
# plt.ylabel("MSE", fontsize=FontSize)
# plt.text(-0.3, 2.52e10, 'x10$^{10}$', fontsize=FontSize)
# plt.subplots_adjust(left=0.15)
# plt.savefig('./figure/var_real_e0001.pdf', dpi=300, bbox_inches='tight')
# plt.show()

############------------e=0.01--------------#################
bar1 = [k_pro[1], a_pro[1], ec_pro[1], i_pro[1]]  # with shortest path
bar2 = [k_rr[1], a_rr[1], ec_rr[1], i_rr[1]]

print(bar1)
print(bar2)

r1 = np.arange(len(bar1))
r2 = [x + barWidth for x in r1]
plt.bar(r1, bar1, width=barWidth, align='center', color=[1, 0.2, 0], edgecolor='black', hatch="//", linewidth=1.2,
        label='JRR')
plt.bar(r2, bar2, width=barWidth, align='center', color=[0, 0.5, 1], edgecolor='black', linewidth=1.2, label='RR')
# plt.yscale('log')
plt.xticks([r + barWidth for r in range(len(bar1))], ['Kosarak', 'Amazon', 'EC', 'Census'], fontsize=FontSize, fontname=Fontfamily)
plt.yticks([0, 5e7, 1e8, 1.5e8, 2e8, 2.5e8], ['0', '0.5', '1', '1.5', '2', '2.5'], fontsize=FontSize, fontname=Fontfamily)
plt.legend(fontsize=FontSize - 1, frameon=True, edgecolor='black', loc='best')
plt.ylabel("MSE", fontsize=FontSize, fontname=Fontfamily)

plt.text(-0.3, 2.52e8, 'x10$^8$', fontsize=FontSize, fontname=Fontfamily)
plt.subplots_adjust(left=0.15)
plt.savefig('./MSE_e001.eps', bbox_inches='tight')
plt.show()

#############------------e=0.1--------------#################
bar1 = [k_pro[2], a_pro[2], ec_pro[2], i_pro[2]]  # with shortest path
bar2 = [k_rr[2], a_rr[2], ec_rr[2], i_rr[2]]

print(bar1)
print(bar2)

r1 = np.arange(len(bar1))
r2 = [x + barWidth for x in r1]
plt.bar(r1, bar1, width=barWidth, align='center', color=[1, 0.2, 0], edgecolor='black', hatch="//", linewidth=1.2, label='JRR')
plt.bar(r2, bar2, width=barWidth, align='center', color=[0, 0.5, 1], edgecolor='black', linewidth=1.2, label='RR')
plt.xticks([r + barWidth for r in range(len(bar1))], ['Kosarak', 'Amazon', 'EC', 'Census'], fontsize=FontSize, fontname=Fontfamily)
plt.yticks([0, 5e5, 1e6, 1.5e6, 2e6, 2.5e6], ['0', '0.5', '1', '1.5', '2', '2.5'], fontsize=FontSize, fontname=Fontfamily)
plt.legend(fontsize=FontSize - 1, frameon=True, edgecolor='black', loc='best')
plt.ylabel("MSE", fontsize=FontSize, fontname=Fontfamily)
plt.text(-0.3, 2.52e6, 'x10$^{6}$', fontsize=FontSize, fontname=Fontfamily)

plt.subplots_adjust(left=0.15)
plt.savefig('./MSE_e01.eps', dpi=300, bbox_inches='tight')
plt.show()

# ############------------e=1--------------#################
bar1 = [k_pro[3], a_pro[3], ec_pro[3], i_pro[3]]  # with shortest path
bar2 = [k_rr[3], a_rr[3], ec_rr[3], i_rr[3]]

print(bar1)
print(bar2)

r1 = np.arange(len(bar1))
r2 = [x + barWidth for x in r1]
plt.bar(r1, bar1, width=barWidth, align='center', color=[1, 0.2, 0], edgecolor='black', hatch="//", linewidth=1.2,
        label='JRR')
plt.bar(r2, bar2, width=barWidth, align='center', color=[0, 0.5, 1], edgecolor='black', linewidth=1.2, label='RR')
# plt.yscale('log')
plt.xticks([r + barWidth for r in range(len(bar1))], ['Kosarak', 'Amazon', 'EC', 'Census'], fontsize=FontSize, fontname=Fontfamily)
# plt.yticks([1e4,2e4,3e4,4e4,5e4], ['1','2','3','4','5'],fontsize=FontSize)
plt.yticks([0, 5e3, 1e4, 1.5e4, 2e4, 2.5e4], ['0', '0.5', '1', '1.5', '2', '2.5'], fontsize=FontSize, fontname=Fontfamily)
plt.legend(fontsize=FontSize - 1, frameon=True, edgecolor='black', loc='best')
plt.ylabel("MSE", fontsize=FontSize, fontname=Fontfamily)
plt.text(-0.3, 2.52e4, 'x10$^{4}$', fontsize=FontSize, fontname=Fontfamily)

plt.subplots_adjust(left=0.15)
plt.savefig('./MSE_e1.eps', dpi=300, bbox_inches='tight')
plt.show()

