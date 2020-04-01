from colour_assigner import get_colour_term
import json
new_dict = {}
with open('all_colors_dict.json') as fh:
    colour_dict = json.load(fh)

for name, rgb in colour_dict.items():
    nbs_iscc = get_colour_term(rgb)
    new_dict[name] = {'rgb': rgb, 'nbs_iscc': nbs_iscc}

with open('all_labeled_colors_dict.json', 'w') as fh:
    json.dump(new_dict, fh)


