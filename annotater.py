import json
import numpy as np
from colour_assigner import get_colour_term
from collections import defaultdict
import random
import sys, os
import operator

from pycocotools.coco import COCO
try:
    import Image
except ImportError:
    from PIL import Image

REVERSE = False


def run_annotater(annotations_file, image_dir, results_dir):
    # Load COCO annotations and annotations file
    coco = COCO(annotations_file)
    with open(annotations_file, 'r') as fh:
        annotations = json.load(fh)

    annotations = sorted(annotations['annotations'], key=lambda ann: ann['image_id'], reverse=REVERSE)

    while len(annotations):
        image_id = annotations[0]['image_id']
        image_file = "{}{}".format("000000", str(image_id))[-7:]
        image = os.path.join(image_dir, '{}.jpg'.format(image_file))
        segments = []
        while annotations[0]['image_id'] == image_id:
            segments.append(annotations.pop(0))

        masks = []
        for seg in segments:
            masks.append(coco.annToMask(seg))

        polygons = []
        for mask in masks:
            polygon = np.where(mask==True)
            polygons.append(polygon)

        iis = []
        for polygon in polygons:
            ii = np.array(zip(polygon[1], polygon[0]))
            iis.append(ii)

        img = Image.open(image)
        red_image_rgb = img.convert("RGB")

        for index in range(len(iis)):
            num_pixels = iis[index].shape[0]
            max_pixels = 500
            description_dict = defaultdict(int)
            colour_dict = defaultdict(int)
            k = max_pixels if num_pixels > max_pixels else num_pixels
            for x, y in random.sample(np.array(iis[index]), k=k):
                r, g, b = red_image_rgb.getpixel((int(x), int(y)))
                name, color = get_colour_term([r, g, b])
                colour_dict[name] += 1
                description_dict[color] += 1

            max_description, description_value = max(description_dict.iteritems(), key=operator.itemgetter(1))
            max_colour, colour_value = max(colour_dict.iteritems(), key=operator.itemgetter(1))
            colour_value = float(colour_value) / k
            description_value = float(description_value) / k
            segments[index]['colour_name'] = {max_colour: colour_value}
            segments[index]['colour_description'] = {max_description: description_value}

        output_file = os.path.join(results_dir, '{}.json'.format(image_id))
        with open(output_file, 'w') as fh:
            json.dump(segments, fh)


if __name__ == '__main__':
    annotations_file, image_dir, results_dir = sys.argv[-3], sys.argv[-2], sys.argv[-1]
    run_annotater(annotations_file, image_dir, results_dir)
