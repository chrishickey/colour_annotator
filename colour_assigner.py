import numpy as np
from scipy import spatial
import webcolors
import json
def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb

with open('all_labeled_colors_dict.json') as fh:
    colour_dict = json.load(fh)

HexNameDict = {}
ISBCC_DICT = {}
RGB = []
for key in colour_dict:
    rgb = colour_dict[key]['rgb']
    nbs_iscc = colour_dict[key]['nbs_iscc']
    ISBCC_DICT[key] = nbs_iscc
    val = rgb_to_hex(tuple(rgb)).upper()
    HexNameDict[val] = key
    RGB.append(rgb)
RGB = np.array(RGB)



def get_colour_term(pt):

    # Lookup color name using Hex:ColorName dictionary:
    NearestRGB = (RGB[spatial.KDTree(RGB).query(pt)[1]])
    # TODO: Calculate Hex from pt. (upper case letters)
    # Instead of str(hex(pt[0])[2:]) in Python2, this is Python3 compatible:
    s = '#' \
        + format(NearestRGB[0],'x').zfill(2) \
        + format(NearestRGB[1],'x').zfill(2) \
        + format(NearestRGB[2],'x').zfill(2)
    ColorHex = s.upper() # "#8B7355"  # "#8B7355"
#     ColorDiff = \
#          '('+'{0:+d}'.format(NearestRGB[0]-pt[0]) \
#         +','+'{0:+d}'.format(NearestRGB[1]-pt[1]) \
#         +','+'{0:+d}'.format(NearestRGB[2]-pt[2]) \
#         +')'
    try: ## TODO: try catch block per https://wiki.python.org/moin/HandlingExceptions
        ColorName=HexNameDict[ColorHex]
    except:
        ColorName="not found"
    return ColorName, ISBCC_DICT[ColorName]