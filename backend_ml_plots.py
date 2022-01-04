
import os, sys
from matplotlib import style
style.use('ggplot')

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../_elements'))

from xpk import *
from xnp import *
from xpd import *

from _study_utils_files import *
from _study_utils_sequences import *
from _study_utils_translations import *
from _study_utils_logs import *

from _study_scopes_ import *


def set_actuals_plots(graphData, figs):

    print('\t. plotting actuals')

    fig = figs[0]
    ax = fig.axes[0]


    # nlines
    color = graphData['colors']['actuals']['base']['nlines']
    lineweight = graphData['lineweights']['actuals']['base']['nlines']
    zorder = graphData['zorders']['actuals']['base']['nlines']
    if ('hlines' in list(graphData['actuals']['base'])):
        for _layer in graphData['actuals']['base']['nlines']:

            ax.plot(
                _layer['x'], _layer['y'],
                linestyle='solid',
                linewidth=lineweight,
                color=color,
                alpha=1,
                zorder=zorder,
            )


    # lines-marks
    color = graphData['colors']['actuals']['base']['nlinesMarks']
    edgecolor = graphData['colors']['actuals']['base']['nlinesMarksEdge']
    lineweight = graphData['lineweights']['actuals']['base']['nlinesMarks']
    markssize = graphData['markssizes']['actuals']['base']['nlinesMarks']
    zorder = graphData['zorders']['actuals']['base']['nlinesMarks']
    if ('marks' in list(graphData['actuals']['base'])):
        for _layer in graphData['actuals']['base']['marks']:

            ax.scatter(
                _layer['x'], _layer['y'],
                marker='.',
                s=markssize,
                linewidth=lineweight,
                color=color,
                edgecolor=edgecolor,
                zorder=zorder,
            )


    # mark y latest
    color = graphData['colors']['actuals']['base']['latestY_nlinesMarkss']
    edgecolor = graphData['colors']['actuals']['base']['latestY_nlinesMarkssEdge']
    lineweight = graphData['lineweights']['actuals']['base']['latestY_nlinesMarks']
    markssize = graphData['markssizes']['actuals']['base']['latestY_nlinesMarks']
    zorder = graphData['zorders']['actuals']['base']['latestY_nlinesMarks']
    if ('latestMark' in list(graphData['actuals']['base'])):
        for _layer in graphData['actuals']['base']['latestMark']:

            ax.scatter(
                _layer['x'], _layer['y'],
                marker='.',
                s=markssize,
                linewidth=lineweight,
                color=color,
                edgecolor=edgecolor,
                zorder=zorder,
            )

    # mark-glow
    glows_color = graphData['colors']['actuals']['base']['latestY_nlinesGlowss']
    glows_edgecolor = graphData['colors']['actuals']['base']['latestY_nlinesGlowssEdge']
    markssize = graphData['markssizes']['actuals']['base']['latestY_nlinesGlows']
    zorder = graphData['zorders']['actuals']['base']['latestY_nlinesGlows']
    if ('latestMark' in list(graphData['actuals']['base'])):
        for _layer in graphData['actuals']['base']['latestMark']:

            ax.scatter(
                _layer['x'], _layer['y'],
                marker='.',
                s=markssize,
                linewidth=14,
                color=glows_color,
                edgecolor=glows_edgecolor,
                zorder=zorder,
            )

    # text y latest
    textcolor = graphData['colors']['general']['texts']
    latesttextBGcolor = graphData['colors']['actuals']['base']['latestY_textsBG']
    lineweight = graphData['lineweights']['actuals']['base']['latestY_text']
    zorder = graphData['zorders']['actuals']['base']['latestY_text']
    if ('latestY' in list(graphData['actuals']['base'])):
        for _layer in graphData['actuals']['base']['latestY']:

            ax.text(
                _layer['x'], _layer['y'], '{}'.format(_layer['text']),
                horizontalAlignment='right',
                verticalAlignment='center',
                transform=ax.transAxes,
                fontdict={
                    'family': 'sans-serif',
                    'size': 8.8,
                    'weight': lineweight,
                    'color': textcolor,
                    'backgroundcolor': latesttextBGcolor,
                },
                zorder=zorder,
            )

    # vlines
    color = graphData['colors']['actuals']['base']['vlines']
    lineweight = graphData['lineweights']['actuals']['base']['vlines']
    zorder = graphData['zorders']['actuals']['base']['vlines']
    if ('vlines' in list(graphData['actuals']['base'])):
        for _layer in graphData['actuals']['base']['vlines']:

            ax.vlines(
                _layer['x'], _layer['y1'], _layer['y2'],
                linewidth=lineweight,
                color=color,
                zorder=zorder,
            )

    # hlines
    _colors = graphData['colors']['actuals']['base']['hlines']
    _lineweights = graphData['lineweights']['actuals']['base']['hlines']
    zorder = graphData['zorders']['actuals']['base']['hlines']
    if ('hlines' in list(graphData['actuals']['apexes'])):
        for _layer in graphData['actuals']['apexes']['hlines']:

            ax.hlines(
                _layer['y'], _layer['x1'], _layer['x2'],
                linewidth=_lineweights[_layer['tf']][_layer['mp']],
                color=_colors[_layer['mp']],
                zorder=zorder,
                clip_on=False,
            )

    return figs
