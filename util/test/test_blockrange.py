from enforce_typing import enforce_types
import pytest

from util.blockrange import BlockRange


@enforce_types
def test_failures():
    with pytest.raises(Exception):  # end < start
        BlockRange(st=20, fin=10, num_samples=5)

    with pytest.raises(Exception):  # arg1 negative
        BlockRange(st=-1, fin=10, num_samples=5)

    with pytest.raises(Exception):  # arg2 negative
        BlockRange(st=1, fin=-1, num_samples=5)

    with pytest.raises(Exception):  # arg3 negative
        BlockRange(st=1, fin=10, num_samples=-5)


@enforce_types
def test_startAtZero():
    r = BlockRange(st=0, fin=3, num_samples=10).getBlocks()
    assert r == [0, 1, 2, 3]


@enforce_types
def test_availableN_samples0():
    r = BlockRange(st=10, fin=20, num_samples=0).getBlocks()
    assert r == []


@enforce_types
def test_available1_samples1():
    r = BlockRange(st=10, fin=10, num_samples=1).getBlocks()
    assert r == [10]


@enforce_types
def test_available1_samplesN():
    r = BlockRange(st=10, fin=10, num_samples=10).getBlocks()
    assert r == [10]


@enforce_types
def test_available2_samples1():
    for _ in range(10):
        r = BlockRange(st=10, fin=11, num_samples=1).getBlocks()
        assert r in ([10], [11])


@enforce_types
def test_available2_samplesN():
    r = BlockRange(st=10, fin=11, num_samples=10).getBlocks()
    assert sorted(r) == [10, 11]


@enforce_types
def test_available3_samples1():
    r = BlockRange(st=10, fin=12, num_samples=1).getBlocks()
    assert r in ([10], [11], [12])


@enforce_types
def test_available3_samplesN():
    for _ in range(10):
        r = BlockRange(st=10, fin=12, num_samples=10).getBlocks()
        assert r == [10, 11, 12]  # should always be sorted


@enforce_types
def test_manyRandom():
    for _ in range(100):
        r = BlockRange(st=10, fin=20, num_samples=3).getBlocks()
        assert len(r) == 3
        assert min(r) >= 10
        assert max(r) <= 20
        assert r == sorted(r)


@enforce_types
def test_general():
    br = BlockRange(st=10, fin=20, num_samples=3)
    assert len(br.getBlocks()) == 3
    assert br.numBlocks() == 3
    assert "BlockRange" in str(br)
