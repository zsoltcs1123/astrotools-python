
from tools.timeline import Timeline
from out.file import to_text_file


class TimelinePrinter():
    
    def __init__(self, timeline: Timeline):
        self.timeline = timeline
        self.str = self._generate_str()
        
    def _generate_str(self) -> str:
        str = ""
        
        for group in self.timeline.grouped_events:
            formatted_date = group[0].time.strftime('%A, %b %d %Y')
            str+= f'{formatted_date}:\n'
            str += ''.join([f'{i + 1}. {e.__repr__()} \n------------\n' for i, e in enumerate(group)]) + '\n'
        
        return str
        
    def print_to_console(self):
        print(self.str)
        
    def print_to_file(self, filename:str):
        to_text_file(filename, self.str)
        
    
        
    