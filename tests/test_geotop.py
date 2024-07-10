import numpy as np

import bromodels


def test_geotop_dis() -> None:
    west = 118246.0
    east = 121601.6
    south = 484755.1
    north = 486597.2

    ds = bromodels.GeoTopDomain(west, south, east, north)
    assert np.all(ds.x.diff("x") == 100)
    assert np.all(ds.y.diff("y") == -100)
    assert np.all(ds.z.diff("z") == -0.5)


def test_stratigraphic() -> None:
    df = bromodels.GTM.GeoTop.geotop_lithology_class()
    assert len(df) == 11
    assert np.all(
        df.columns
        == [
            "LITHO_CLASS_CD",
            "DESCRIPTION",
            "VOXEL_NR",
            "SEQ_NR",
            "RED_DEC",
            "GREEN_DEC",
            "BLUE_DEC",
        ]
    )

    df = bromodels.GTM.GeoTop.geotop_stratigraphic_unit()
    assert len(df) == 98
    assert np.all(
        df.columns
        == [
            "STR_UNIT_CD",
            "DESCRIPTION",
            "VOXEL_NR",
            "SEQ_NR",
            "RED_DEC",
            "GREEN_DEC",
            "BLUE_DEC",
        ]
    )


def test_geotop_point() -> None:
    west = 123659.2
    south = 480710.9
    east = 134996.4
    north = 488079.2

    x = 127418.76
    y = 482854.44
    z = -13

    ds = bromodels.GeoTopDomain(west, south, east, north)
    data = bromodels.GeoTopPoint(x, y, z)

    np.testing.assert_allclose(
        ds.lithok.loc[dict(x=data.x, y=data.y, z=data.z)], data.lithok
    )


def test_geotop_column() -> None:
    west = 123659.2
    south = 480710.9
    east = 134996.4
    north = 488079.2

    x = 127418.76
    y = 482854.44

    ds = bromodels.GeoTopDomain(west, south, east, north, -60)
    data = bromodels.GeoTopColumn(x, y)

    np.testing.assert_allclose(
        ds.lithok.loc[dict(x=data.x, y=data.y)].dropna(dim="z"),
        data.lithok.dropna(dim="z"),
    )
