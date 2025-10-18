def color_red(value):
  color = 'red'
  return 'color: %s' % color

def color_green(value):
  color = 'green'
  return 'color: %s' % color

'''
def color_yellow(value): # color string yellow if star in front
  s = str(value).strip()
  color = 'yellow' if str(value)[0] == '*' else 'black'
  return 'color: %s' % color
'''
def highlight_cells(value):
    s = str(value).strip()
    color = 'yellow' if s[0] == '*' else 'white'
    return 'background-color: {}'.format(color)
