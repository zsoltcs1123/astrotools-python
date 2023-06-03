

def generate(timestamps: str) -> str:
    TV_SCRIPT = f'''//@version=5
indicator("Moon change", overlay = true)

moon_date = array.from({timestamps})

for date in moon_date
    line.new(x1=date, y1=low, x2=date, y2=high, xloc=xloc.bar_time, extend=extend.both, color=color.new(#cfdef8, 10), style=line.style_solid, width=2)'''

    return TV_SCRIPT
