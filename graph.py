#!/usr/bin/env python
import matplotlib.pyplot as plt

def create_graph_image(t):
    x, y = [], []
    x_tick = []
    for i in t:
        x_tick.append(i[0].split(' ')[1][:-3])
        x.append(i[0])
        y.append(i[1])

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(x, y, 'k-', lw=1.5, alpha=0.6, label='generation')
    ax.plot(x, y, 'o', color='none', markersize=7, markeredgewidth=3, markeredgecolor='blue', alpha=0.8, label='generation_dot')

    ax.set_xlim(x[0], x[-1])
    ax.set_xticklabels(x_tick, fontsize=7, color="black")
    ax.set_xlabel('Time (h)', fontsize=14, color='black')

    ax.set_ylim(0, 50)
    ax.set_yticks([0,20,40])
    ax.set_yticklabels([0,20,40], fontsize=14, color='black')
    ax.set_ylabel('Generation (kWh)')

    ax.spines['top'].set_linewidth(0)
    ax.spines['right'].set_linewidth(0)
    ax.spines['left'].set_linewidth(2)
    ax.spines['left'].set_color('gray')
    ax.spines['bottom'].set_linewidth(2)
    ax.spines['bottom'].set_color('gray')
    ax.tick_params(direction='in', length=6, width=2, color='gray')

    ax.yaxis.grid(linestyle='--', lw=1, alpha=0.4, color='lightgray')
    ax.set_title('Electric power generation')

    plt.setp(ax.get_xticklabels(), rotation=45)
    plt.savefig('figure.png', bbox_inches='tight')