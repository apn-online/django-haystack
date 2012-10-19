"""
Mock out the required spatial classes.
ElasticSearch doesn't need the extra complexity of having geos installed.

"""


class Distance(object):
    def __init__(self, km):
        self.km = km


class Point(object):

    geom_type = 'Point'

    def __init__(self, x, y=None):
        """Requires (lng, lat)"""

        if isinstance(x, (tuple, list)):
            # Here a tuple or list was passed in under the `x` parameter.
            coords = x
        elif isinstance(x, (int, float, long)) and isinstance(y, (int, float, long)):
            # Here X and Y were passed in individually, as parameters.
            coords = (x, y)
        else:
            raise TypeError('Invalid parameters given for Point initialization. %r, %r' % (x, y))

        self.x = self.lng = float(coords[0])
        self.y = self.lat = float(coords[1])

    def get_coords(self):
        "Returns a tuple of (lng, lat)."
        return (self.lng, self.lat)
