from starbdp.grid import iter_spatial_windows

def test_sliding_windows():
    ws = list(iter_spatial_windows(5, 5, 3, "sliding"))
    assert len(ws) == 9
    assert all(w.area == 9 for w in ws)

def test_partition_cover():
    ws = list(iter_spatial_windows(5, 5, 3, "partition"))
    assert sum(w.area for w in ws) == 25
