# Bokeh libraries
import pandas as pd
from bokeh.io import output_notebook, curdoc, output_file, export_png
from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource, HoverTool, Legend,  CustomJS, Slider
from bokeh.layouts import column
from bokeh.palettes import Spectral11
from bokeh.models import TabPanel, Tabs, Label
from bokeh.themes import Theme

from element import *
from element_truss import *
from element_frame import *
from element_cbush import *

def CharLength(nodes):
    x = []
    y = []
    for node in nodes:
        x.append(node._coord[0])
        y.append(node._coord[1])
    len_x = max(x) - min(x)
    len_y = max(y) - min(y)
    return len_x, len_y
def PlotDisplacement(nodes, elements,U, P):
    len_x, len_y = CharLength(nodes)
    # set the theme
    curdoc().theme = 'dark_minimal'
    color_disp = 'deeppink'


    # create a new plot with a title and axis labels
    p = figure(title="Deformation",
               x_axis_label="x",
               y_axis_label="y",
               match_aspect=True,
               )

    nid = []
    x = []
    y = []
    x_disp = []
    y_disp = []

    ele_id = []
    ele_x = []
    ele_y = []
    ele_x_avg = []
    ele_y_avg = []
    ele_x_disp = []
    ele_y_disp = []
    ele_x_disp_avg = []
    ele_y_disp_avg = []

    for node in nodes:
        nid.append(node._nid)
        x.append(node._coord[0])
        y.append(node._coord[1])

        node.StorePostProcessDisp(U)
        x_disp.append(node._coord_disp[0][0])
        y_disp.append(node._coord_disp[1][0])

    for ele in elements:
        ele.SetCharLength(len_x, len_y)
        ele.PostProcess()
        ele_id.append(ele._eid)
        coords_nodei = ele._nodes[0]._coord
        coords_nodej = ele._nodes[1]._coord
        ele_x.append([coords_nodei[0], coords_nodej[0]])
        ele_y.append([coords_nodei[1], coords_nodej[1]])
        ele_x_avg.append((coords_nodei[0] + coords_nodej[0]) / 2)
        ele_y_avg.append((coords_nodei[1] + coords_nodej[1]) / 2)


        coords_nodei_disp = ele._nodes[0]._coord_disp
        coords_nodej_disp = ele._nodes[1]._coord_disp
        ele_x_disp.append([coords_nodei_disp[0], coords_nodej_disp[0]])
        ele_y_disp.append([coords_nodei_disp[1], coords_nodej_disp[1]])
        ele_x_disp_avg.append((coords_nodei_disp[0] + coords_nodej_disp[0]) / 2)
        ele_y_disp_avg.append((coords_nodei_disp[1] + coords_nodej_disp[1]) / 2)


    data_nodes = pd.DataFrame({'nid' : nid,
                               'x': x,
                               'y': y,
                               'x_disp': x_disp,
                               'y_disp': y_disp,
                                })

    data_ele = pd.DataFrame({'eid' : ele_id,
                             'ele_x': ele_x,
                             'ele_y': ele_y,
                             'ele_x_avg': ele_x_avg,
                             'ele_y_avg': ele_y_avg,
                             'ele_x_disp': ele_x_disp,
                             'ele_y_disp': ele_y_disp,
                             'ele_x_disp_avg': ele_x_disp_avg,
                             'ele_y_disp_avg': ele_y_disp_avg,
                             })

    s1 = ColumnDataSource(data_nodes)
    s2 = ColumnDataSource(data_nodes)
    s3 = ColumnDataSource(data_ele)
    s4 = ColumnDataSource(data_ele)

    # add scatter plot
    r1 = p.circle(x='x', y='y', source=s1, legend_label='undeformed', line_width=8, muted_alpha=0.1)
    r2 = p.circle(x='x_disp', y='y_disp', source=s2, legend_label='deformed', line_width=8, muted_alpha=0.1, color=color_disp)
    r3 = p.circle(x='ele_x_avg', y='ele_y_avg', source=s3, legend_label='undeformed', line_width=8, alpha=0.0, muted_alpha=0.0)
    r4 = p.circle(x='ele_x_disp_avg', y='ele_y_disp_avg', source=s4, legend_label='deformed', line_width=8, alpha=0.0, muted_alpha=0.0, color=color_disp)

    # add hover tool
    # Add tools
    hover = HoverTool(renderers=[r1],
                      tooltips=[('nid', '@nid'),
                                ('x', '@x'),
                                ('y', '@y')])
    hover.point_policy = 'snap_to_data'
    p.add_tools(hover)
    hover = HoverTool(renderers=[r2],
                      tooltips=[('nid', '@nid'),
                                ('x_disp', '@x_disp'),
                                ('y_disp', '@y_disp')])
    hover.point_policy = 'snap_to_data'
    p.add_tools(hover)
    hover = HoverTool(renderers=[r3],
                      tooltips=[('ele id', '@eid'),
                                ])
    hover.point_policy = 'snap_to_data'
    p.add_tools(hover)
    hover = HoverTool(renderers=[r4],
                      tooltips=[('ele id', '@eid'),
                                ])
    hover.point_policy = 'snap_to_data'
    p.add_tools(hover)

    for count, ele in enumerate(ele_id):
        p.multi_line(xs='ele_x', ys='ele_y', source=s3, legend_label='undeformed', line_width=3, muted_alpha=0.1)
        p.multi_line(xs='ele_x_disp', ys='ele_y_disp', source=s4, legend_label='deformed', line_width=3, muted_alpha=0.1, color=color_disp)



    p.legend.click_policy = "mute"
    # show the results
    show(column(p))