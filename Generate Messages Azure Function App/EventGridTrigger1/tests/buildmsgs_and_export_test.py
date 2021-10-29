import sys
from unittest.mock import MagicMock, patch, call, Mock
sys.modules['wz_vehpath_lanestat_builder'] = Mock()
sys.modules['wz_map_constructor'] = Mock()
sys.modules['wz_xml_builder'] = Mock()
sys.modules['rsm_2_wzdx_translator'] = Mock()
sys.modules['wz_msg_segmentation'] = Mock()

from .. import buildmsgs_and_export

def test_findNodeByDistance():
    numLanes = 1
    targetDistance = 100
    points = [
        [0, 1, 2, 3, 4, 5, 6, 0],
        [0, 1, 2, 3, 4, 5, 6, 40],
        [0, 1, 2, 3, 4, 5, 6, 80],
        [0, 1, 2, 3, 4, 5, 6, 120],
    ]
    expected = 2
    actual = buildmsgs_and_export.findNodeByDistance(points, numLanes, targetDistance)
    assert expected == actual

def test_getMapPointsBetweenIndexes_2_lanes():
    numLanes = 2
    startIndex = 1
    endIndex = 4
    points = []
    arr = [
        [0, 1, 2, 0, 0, 3, 4, 5],
        [6, 7, 8, 0, 0, 9, 10, 11],
        [12, 13, 14, 0, 0, 15, 16, 17],
        [18, 19, 20, 0, 0, 21, 22, 23],
        [24, 25, 26, 0, 0, 27, 28, 29],
    ]
    expected = [[[6, 7, 8], [9, 10, 11]], [[12, 13, 14], [15, 16, 17]], [[18, 19, 20], [21, 22, 23]]]
    actual = buildmsgs_and_export.getMapPointsBetweenIndexes(arr, numLanes, startIndex, endIndex, points)
    assert actual == expected

def test_getMapPointsBetweenIndexes_append_points():
    numLanes = 1
    startIndex = 1
    endIndex = 4
    points = [1000]
    arr = [
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8],
        [9, 10, 11],
        [12, 13, 14],
    ]
    expected = [1000, [[3, 4, 5]], [[6, 7, 8]], [[9, 10, 11]]]
    actual = buildmsgs_and_export.getMapPointsBetweenIndexes(arr, numLanes, startIndex, endIndex, points)
    assert actual == expected