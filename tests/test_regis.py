import numpy as np

import bromodels


def test_regis_dis() -> None:
    west = 118246.0
    east = 121601.6
    south = 484755.1
    north = 486597.2

    ds = bromodels.RegisDomain(west, south, east, north)
    assert np.all(ds.x.diff("x") == 100)
    assert np.all(ds.y.diff("y") == -100)


def test_stratigraphic() -> None:
    df = bromodels.HGM.Regis.regis_stratigraphic_unit()
    assert len(df) == 155
    assert np.all(
        df.columns
        == ["HYD_UNIT_CD", "DESCRIPTION", "SEQ_NR", "RED_DEC", "GREEN_DEC", "BLUE_DEC"]
    )


def test_regis_fill() -> None:
    west = 118246.0
    east = 121601.6
    south = 484755.1
    north = 486597.2

    ds1 = bromodels.RegisDomain(west, south, east, north)
    np.testing.assert_array_equal(ds1.kv.loc[dict(layer=b"HLc")], np.nan)

    ds2 = bromodels.Regis.dataset_fill(
        ds1, anisotropy=1 / 10, obj={b"HLc": (5, 5), b"DTc": (15, 15)}
    )
    np.testing.assert_array_less(ds2.bottom.diff("layer"), 0)
    np.testing.assert_allclose(ds2.kv.loc[dict(layer=b"HLc")], 5)


def test_regis_point() -> None:
    west = 123659.2
    south = 480710.9
    east = 134996.4
    north = 488079.2

    x = 127418.76
    y = 482854.44
    z = -150

    ds = bromodels.RegisDomain(west, south, east, north)
    data = bromodels.RegisPoint(x, y, z)

    np.testing.assert_allclose(
        ds.kh.loc[dict(x=data.x, y=data.y, layer=data.layer)], data.kh
    )


def test_regis_column() -> None:
    west = 123659.2
    south = 480710.9
    east = 134996.4
    north = 488079.2

    x = 127418.76
    y = 482854.44

    ds = bromodels.RegisDomain(west, south, east, north, -1000)
    data = bromodels.RegisColumn(x, y)

    np.testing.assert_allclose(
        ds.top.loc[dict(x=data.x, y=data.y)].dropna(dim="layer"),
        data.top.dropna(dim="layer"),
    )
