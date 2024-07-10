import matplotlib.pyplot as plt
import numpy as np
import xarray
from matplotlib.colors import ListedColormap

import bromodels

_link = {
    "lithok": (bromodels.GeoTop.geotop_lithology_class(), "LITHO_CLASS_CD"),
    "strat": (bromodels.GeoTop.geotop_stratigraphic_unit(), "STR_UNIT_CD"),
}

# load GeoTop data
ds = bromodels.GeoTopDomain(
    west=118421, south=484233, east=121256, north=486076, bottom=-20
)
print(ds)

# plot elevation
zgrid, _, _ = xarray.broadcast(ds.z, ds.y, ds.x)
variable = zgrid.where(~np.isnan(ds.lithok)).max("z")
variable.plot()
plt.pause(5)
plt.close()

# plot lithology maps
df, CD = _link["lithok"]
colormap = []
label = []
for i, row in df.loc[df["VOXEL_NR"].isin(ds["lithok"].values.flatten())].iterrows():
    colormap.append(
        np.array([row.RED_DEC / 255, row.GREEN_DEC / 255, row.BLUE_DEC / 255])
    )
    label.append(row[CD])
ds.lithok.plot(x="x", y="y", col="z", col_wrap=4, cmap=ListedColormap(colormap))
plt.pause(5)
plt.close()

# plot lithology cross section
ds.lithok.plot(x="x", y="z", col="y", col_wrap=4, cmap=ListedColormap(colormap))
plt.pause(5)
plt.close()

# load Regis data
ds = bromodels.RegisDomain(
    west=118421, south=484233, east=121256, north=486076, bottom=-500
)
ds = bromodels.Regis.dataset_fill(
    ds, anisotropy=1 / 10, obj={b"HLc": (5, 5), b"DTc": (15, 15)}
)
print(ds)

# plot elevation
variable = ds.top.max("layer")
variable.plot()
plt.pause(5)
plt.close()

# plot horizontal conductivity maps
ds.kh.plot(x="x", y="y", col="layer", col_wrap=4)
plt.pause(5)
plt.close()

# plot horizontal conductivity cross section
ds = ds.assign_coords(index=("layer", range(ds.sizes["layer"])))
ds = ds.swap_dims({"layer": "index"})
ds.kh.plot(x="x", y="index", col="y", col_wrap=4, yincrease=False)
plt.pause(5)
plt.close()
