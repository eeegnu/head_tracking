
import numpy as np
from constants import screenz, ROOM_WIDTH, ROOM_HEIGHT

def projection(point, camera):
    """
    Returns projection of (x-cx, y-cy, z-cz) to z=screenz plane given the observer at (0, 0, 0)
    """
    x1, y1, z1 = point
    cx, cy, cz = camera
    
    x, y, z = x1 - cx, y1 - cy, z1 - cz
    if z == 0:
        return None
    px = round(x * screenz / z) + ROOM_WIDTH // 2
    py = round(y * screenz / z) + ROOM_HEIGHT // 2

    return (px, py, 0)


def darken(color, shade):
    assert 0 <= shade <= 1
    return (np.array(color) * shade).astype(int).tolist()

