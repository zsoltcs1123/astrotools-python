
from tools.timeline import Timeline


class TimelinePrinter():
    
    def __init__(self, timeline: Timeline):
        self.timeline = timeline
        
        
    def print_to_console(self):
        str = ""
        
        for group in self.timeline.grouped_events:
            formatted_date = group[0].time.strftime('%A, %b %d %Y')
            str+= f'{formatted_date}:\n'
            str += ''.join([f'{i + 1}. {e.__repr__()} \n------------\n' for i, e in enumerate(group)]) + '\n'
            
        print(str)
        