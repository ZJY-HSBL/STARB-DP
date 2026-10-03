from dataclasses import dataclass
from typing import Iterator

@dataclass(frozen=True)
class SpatialWindow:
    r0: int
    r1: int
    c0: int
    c1: int

    @property
    def area(self) -> int:
        return (self.r1 - self.r0) * (self.c1 - self.c0)

def iter_spatial_windows(height: int, width: int, m: int, mode: str = "sliding") -> Iterator[SpatialWindow]:
    if m <= 0 or height <= 0 or width <= 0:
        raise ValueError("invalid spatial dimensions")
    mh, mw = min(m, height), min(m, width)

    if mode == "partition":
        for r0 in range(0, height, mh):
            for c0 in range(0, width, mw):
                yield SpatialWindow(r0, min(r0 + mh, height), c0, min(c0 + mw, width))
        return

    if mode != "sliding":
        raise ValueError("mode must be sliding or partition")

    for r0 in range(height - mh + 1):
        for c0 in range(width - mw + 1):
            yield SpatialWindow(r0, r0 + mh, c0, c0 + mw)

def build_cell_membership(height, width, windows):
    membership = [[[] for _ in range(width)] for _ in range(height)]
    for k, w in enumerate(windows):
        for i in range(w.r0, w.r1):
            for j in range(w.c0, w.c1):
                membership[i][j].append(k)
    return membership
