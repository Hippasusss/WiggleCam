
from enum import Enum

class Colours:
    black = '30'
    red = '31'
    green = '32'
    yellow = '33'
    blue = '34'
    magenta = '35'
    cyan = '36'
    white = '37'
    _START = '\033['
    _END = '\033[0m'
    _BOLD= '1'
    _UNDERLINE= '4'

def colourFormat(inputString, colour, bold = False, underline = False):
    outputString = None
    boldString = '' 
    underlineString = '' 

    if bold:
        boldString = ';' + Colours._BOLD

    if underline:
        underlineString = ';' + Colours._UNDERLINE

    outputString = Colours._START + colour + boldString + underlineString + 'm' + inputString + Colours._END
    return outputString





