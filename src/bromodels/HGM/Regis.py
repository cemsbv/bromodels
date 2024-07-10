import logging
from typing import Any, Dict, Tuple, Union

import numpy as np
import pandas as pd
import xarray

from .data import HGM_STR_table

Number = Union[float, int]

url = "http://dinodata.nl/opendap/REGIS/REGIS.nc"


def RegisDomain(
    west: Number = 118421,
    south: Number = 484233,
    east: Number = 121256,
    north: Number = 486076,
    bottom: Number = -500,
) -> xarray.Dataset:
    """
    Extract a Dataset based on a domain (west, south, east, north, bottom) of Regis.

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
    ds = ds.drop_vars(
        ["x_bounds", "y_bounds", "lat_bounds", "lon_bounds", "crs"], errors="ignore"
    )
    ds = ds.sel(x=slice(west, east), y=slice(south, north))
    ds = ds.dropna("layer", how="all", subset=["top", "bottom"])

    if ds.bottom.min() < bottom:
        ds = ds.where(ds.bottom > bottom, drop=True)
    ds = ds.sortby("y", ascending=False)

    for lay in ds.layer:
        if (
            np.isnan(ds.sel(layer=lay).kh).all()
            and np.isnan(ds.sel(layer=lay).kv).all()
        ):
            logging.warning(f"No conductivity in layer: {lay.values}")

    return ds


def RegisColumn(x: Number = 134464, y: Number = 454423) -> xarray.Dataset:
    """
    Extract a Dataset based on a point (x, y, z) location in Regis.

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
    ds = ds.drop_vars(
        ["x_bounds", "y_bounds", "lat_bounds", "lon_bounds", "crs"], errors="ignore"
    )
    ds = ds.sel(x=x, y=y, method="nearest")
    ds = ds.dropna("layer", how="all", subset=["top", "bottom"])

    return ds


def RegisPoint(
    x: Number = 134464, y: Number = 454423, z: Number = -10
) -> xarray.Dataset:
    """
    Extract a Dataset based on a point (x, y, z) location in Regis.

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
    ds = ds.drop_vars(
        ["x_bounds", "y_bounds", "lat_bounds", "lon_bounds", "crs"], errors="ignore"
    )
    ds = ds.sel(x=x, y=y, method="nearest")
    ds = ds.dropna("layer", how="all", subset=["top", "bottom"])
    ds = ds.where((ds.top >= z) & (ds.bottom < z), drop=True)

    return ds


def regis_stratigraphic_unit() -> pd.DataFrame:
    """
    Read lookup DataFrame that relates stratigraphic values to description.
    """
    # Get lookup DataFrame to connect geological units codes to numbers
    return pd.DataFrame(HGM_STR_table)


def dataset_fill(
    ds: xarray.Dataset, anisotropy: Number, obj: Dict[Any, Tuple[Number, Number]]
) -> xarray.Dataset:
    """
    Use anisotropy to fill conductivity values and fill missing values based
    on user input.

    Parameters
    ----------
    ds: xarray.Dataset
    anisotropy : int, float
        Magnitude of difference conductivity in different directions
        (Vertical = Horizontal * anisotropy)
    obj : Dict[Any, Tuple[Number, Number]]
        A dictionary with a key corresponding to the layer name and a tuple
        containing the horizontal and vertical conductivity value
    Returns
    -------
    xarray.Dataset
    """

    assert "REGIS" in ds.title, "This is not a Regis Dataset"

    ds["kv"] = ds.kv.fillna(ds.kh * anisotropy)
    ds["kh"] = ds.kh.fillna(ds.kv * 1 / anisotropy)

    for key, value in obj.items():
        ds["kh"].loc[dict(layer=key)] = value[0]
        ds["kv"].loc[dict(layer=key)] = value[1]

    ds = ds.where(~np.isnan(ds.top))

    for lay in ds.layer:
        if (
            np.isnan(ds.sel(layer=lay).kh).all()
            and np.isnan(ds.sel(layer=lay).kv).all()
        ):
            ValueError(
                f"No conductivity in layer: {lay.values}, please provide the value"
            )

    ds = ds.assign_coords(index=("layer", range(ds.sizes["layer"])))
    ds = ds.swap_dims({"layer": "index"})

    ds["kv"] = ds.kv.bfill("index")
    ds["kh"] = ds.kh.bfill("index")

    ds["top"] = ds.top.interpolate_na("index")
    ds["bottom"] = ds.bottom.interpolate_na("index")

    ds = ds.swap_dims({"index": "layer"})
    ds = ds.drop_vars("index")

    return ds
