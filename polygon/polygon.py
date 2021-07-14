"""
Take OPEN, HIGH, LOW, CLOSE, VOLUME and turn into a polygon image, 300x300

HIGH and LOW will be the left and right vertices on the polygon
 - the distance between them will be a logarithmically altered representation of the percent difference

OPEN and CLOSE will be the top and bottom vertices on the polygon
 - the distance between them will be represented in the same way

VOLUME will be represented by the shading within the polygon, higher volume indicated with more white pixels and vice versa.

Feed this through a CNN and implement temporal difference learning.
Polygons will be fed in batches of 5, each representing the result of a 5 minute interval.
"""

from PIL import Image, ImageDraw
import numpy as np


class Polygon:
    def __init__(self, size):
        self.size = size
        self.image = None
        self.records = []

    def prepare(self, inputs):
        """
        param inputs:
            [{high: int, low: int, open: int, close: int, volume: int}]
        """
        for i in inputs:
            self.records.append([i[0], i[1], i[2], i[3]])

        return self

    def split_batch(self, batch_size):
        small_batch_polygons = []
        for i in range(0, len(self.records), batch_size):
            batch = self.records[i : i + batch_size]
            small_batch_polygons.append(Polygon(self.size).prepare(batch))
        return small_batch_polygons

    def price_delta(self):
        start = self.records[0][3]
        end = self.records[len(self.records) - 1][3]
        print("$%s to $%s" % (start, end))
        return end - start

    def gain(self):
        return True if self.price_delta() > 0 else False

    def gen_polygon_flexible(self):
        self.image = Image.new("RGB", self.size)
        draw = ImageDraw.Draw(self.image)
        segments = len(self.records)
        # vertical spacing of the N polygon centers
        spacing = self.size[1] / (segments + 1)
        centers = [(i + 1) * spacing for i in range(0, segments)]
        # find the average, min, max open/close difference
        open_close_diffs = [abs(i[2] - i[3]) for i in self.records]
        open_close_diff_average = np.mean(open_close_diffs)
        open_close_diff_max = np.max(open_close_diffs)
        open_close_diff_min = np.min(open_close_diffs)
        # find the average, min, max high/low difference
        high_low_diffs = [abs(i[0] - i[1]) for i in self.records]
        high_low_diff_average = np.mean(high_low_diffs)
        high_low_diff_max = np.max(high_low_diffs)
        high_low_diff_min = np.min(high_low_diffs)

        for i in range(len(self.records)):
            r = self.records[i]
            c = centers[i]

            high_low_diff = abs(r[0] - r[1])
            high_low_ratio = high_low_diff / high_low_diff_average
            high_low_span = high_low_ratio * self.size[0] / 4

            open_close_diff = abs(r[2] - r[3])
            open_close_ratio = open_close_diff / open_close_diff_average
            open_close_span = open_close_ratio * spacing

            xy = [
                ((self.size[0] / 2) - high_low_span, c),
                (self.size[0] / 2, c + open_close_span),
                ((self.size[0] / 2) + high_low_span, c),
                (self.size[0] / 2, c - open_close_span),
            ]

            draw.polygon(xy)

        # self.image.show()
        return self

    def gen_polygon_rigid(self, high, low):
        """
        Draws the corners of each polygon in place based
        on of a pre-set group of values. (Instead of each corner render being
        from the average of the group)
        """
        self.image = Image.new("RGB", self.size)
        draw = ImageDraw.Draw(self.image)
        segments = len(self.records)
        # vertical spacing of the N polygon centers
        spacing = self.size[1] / (segments + 1)
        centers = [(i + 1) * spacing for i in range(0, segments)]
        # horizontal reference for centers
        mid = (high + low) / 2

        for i in range(len(self.records)):
            r = self.records[i]
            c = centers[i]

            high_val = (r[0] / (high - mid)) * -(self.size[0] / 4)
            low_val = (r[1] / (mid - low)) * (self.size[0] / 4)

            open_val = r[2] / (high - mid) * -spacing
            close_val = r[2] / (mid - low) * spacing

            xy = [
                ((self.size[0] / 2) + high_val, c),
                (self.size[0] / 2, c + open_val),
                ((self.size[0] / 2) + low_val, c),
                (self.size[0] / 2, c + close_val),
            ]

            draw.polygon(xy)

        return self

    def show_image(self):
        self.image.show()
        return self

    def records(self):
        return self.records

    def gen_image(self):
        return self.image

    def gen_ndarray(self):
        return np.array(self.image)
