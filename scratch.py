import numpy as np
from bokeh.io import output_file, save
from bokeh.layouts import column
from bokeh.models import ColumnDataSource, CustomJS, Slider
from bokeh.plotting import figure, show

#generate random data
x = np.linspace(0, 10, 500)
y = np.sin(x)

source = ColumnDataSource(data=dict(x=x, y=y))

#create figure
myPlot = figure(y_range=(-10, 10),
              width=660,
              height=380,
              toolbar_location=None,
              background_fill_color='white')

#create line
myPlot.line('x', 'y',
            source=source,
            line_width=3,
            line_alpha=0.6)

#create sliders
amp    = Slider(start=0.1, end=10, value=2, step=.1, title="Amplitude", bar_color='yellow')
freq   = Slider(start=0.1, end=10, value=2, step=.1, title="Frequency", bar_color='purple')
phase  = Slider(start=-6.4, end=6.4, value=0, step=.1, title="Phase" , bar_color='blue')
offset = Slider(start=-9, end=9, value=0, step=.1, title="Offset" , bar_color='green')

#javaScript callback
callback = CustomJS(args=dict(source=source, amp=amp, freq=freq, phase=phase, offset=offset),
                    code="""
    const A = amp.value
    const k = freq.value
    const p = phase.value
    const B = offset.value

    const x = source.data.x
    const y = Array.from(x, (x) => B + A*Math.sin(k*x+p))
    source.data = { x, y }
""")

#call callback when change in slider
amp.js_on_change('value', callback)
freq.js_on_change('value', callback)
phase.js_on_change('value', callback)
offset.js_on_change('value', callback)

#display output
output_file("output.html")
show(column(myPlot,amp, freq, phase, offset))