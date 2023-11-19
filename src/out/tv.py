

def generate_decans(title: str, timestamps: str) -> str:
    TV_SCRIPT = f'''//@version=5
indicator("{title}", overlay = true)

decans = array.from({timestamps})

for date in decans
    line.new(x1=date, y1=low, x2=date, y2=high, xloc=xloc.bar_time, extend=extend.both, color=color.new(#cfdef8, 10), style=line.style_solid, width=2)'''

    return TV_SCRIPT


def generate_pivot_times(title: str, timestamps: str) -> str:
    TV_SCRIPT = f'''//@version=5
indicator("{title}", overlay = true)

pivots = array.from({timestamps})

for pivot in pivots
    line.new(x1=pivot, y1=low, x2=pivot, y2=high, xloc=xloc.bar_time, extend=extend.both, color=color.new(#48cce3, 10), style=line.style_solid, width=1)'''

    return TV_SCRIPT


def generate_decans_progressions(title: str, decans: str, lines: str) -> str:
    TV_SCRIPT = f'''//@version=5
indicator("{title}", overlay = true)

decans = array.from({decans})
lines = array.from({lines})

for i = 0 to array.size(decans) - 1 
    if array.get(lines, i) == 100
        line.new(x1=array.get(decans, i), y1=low, x2=array.get(decans, i), y2=high, xloc=xloc.bar_time, extend=extend.both, color=color.new(#cfdef8, 10), style=line.style_solid, width=2)
    else if array.get(lines, i) == 50
        line.new(x1=array.get(decans, i), y1=low, x2=array.get(decans, i), y2=high, xloc=xloc.bar_time, extend=extend.both, color=color.new(#cfdef8, 30), style=line.style_dotted, width=1)'''
    return TV_SCRIPT
