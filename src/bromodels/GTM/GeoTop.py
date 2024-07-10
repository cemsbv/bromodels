from typing import Union

import pandas as pd
import xarray

from .data import GTM_LITHO_CLASS_table, GTM_STR_UNIT_table

Number = Union[float, int]

url = "http://dinodata.nl/opendap/GeoTOP/geotop.nc"


def GeoTopDomain(
    west: Number = 118421,
    south: Number = 484233,
    east: Number = 121256,
    north: Number = 486076,
    bottom: Number = -20,
) -> xarray.Dataset:
    """
    Extract a Dataset based on a domain (west, south, east, north, bottom) of GeoTop.

    Parameters
    ----------
    west : int, float, optional
        Coordinate in RD new (EPSG:28992)
    south : int, float, optional
        Coordinate in RD new (EPSG:28992)
    east : int, float, optional
        Coordinate in RD new (EPSG:28992)
    north : int, float, optional
        Coordinate in RD new (EPSG:28992)
    bottom : int, float, optional
        Bottom of the domain [m NAP]
    """

    if west > east:
        raise ValueError("west coordinate is larger than east coordinate")

    if south > north:
        raise ValueError("south coordinate is larger than north coordinate")

    ds = xarray.open_dataset(url)
    ds = ds.sortby("z", ascending=False)
    ds = ds.transpose()
    ds = ds.sel(x=slice(west, east), y=slice(south, north), z=slice(None, bottom))
    ds = ds.dropna("z", how="all", subset=["lithok", "strat"])
    ds.load()
    ds = ds.sortby("y", ascending=False)
    return ds


def GeoTopColumn(x: Number = 134464, y: Number = 454423) -> xarray.Dataset:
    """
    Extract a Dataset based on a point (x, y) location in GeoTop.

    Parameters
    ----------
    x : int, float, optional
        Coordinate in RD new (EPSG:28992)
    y : int, float, optional
        Coordinate in RD new (EPSG:28992)

    Returns
    -------
    xarray.Dataset
    """
    ds = xarray.open_dataset(url)
    ds = ds.sel(x=x, y=y, method="nearest")
    ds = ds.dropna("z", how="all", subset=["lithok", "strat"])
    ds = ds.sortby("z", ascending=False)
    return ds


def GeoTopPoint(
    x: Number = 134464, y: Number = 454423, z: Number = -10
) -> xarray.Dataset:
    """
    Extract a Dataset based on a point (x, y, z) location in GeoTop.

    Parameters
    ----------
    x : int, float, optional
        Coordinate in RD new (EPSG:28992)
    y : int, float, optional
        Coordinate in RD new (EPSG:28992)
    z : int, float, optional
        Depth in m NAP

    Returns
    -------
    xarray.Dataset
    """
    ds = xarray.open_dataset(url)
    ds = ds.sel(x=x, y=y, z=z, method="nearest")
    return ds


def geotop_stratigraphic_unit() -> pd.DataFrame:
    """
    Read lookup DataFrame that relates stratigraphic values to description.
    """
    # Get lookup DataFrame to connect geological units codes to numbers
    return pd.DataFrame(GTM_STR_UNIT_table)


def geotop_lithology_class() -> pd.DataFrame:
    """
    Read lookup DataFrame that relates lithology values to description.
    """
    # Get lookup DataFrame to connect geological units codes to numbers
    return pd.DataFrame(GTM_LITHO_CLASS_table)
