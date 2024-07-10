# conda install -c conda-forge libstdcxx-ng

import numpy as np
import pyvista
from matplotlib.colors import ListedColormap

import bromodels

_link = {
    "lithok": (bromodels.GeoTop.geotop_lithology_class(), "LITHO_CLASS_CD"),
    "strat": (bromodels.GeoTop.geotop_stratigraphic_unit(), "STR_UNIT_CD"),
}

# load GeoTop data
ds = bromodels.GeoTopDomain(
    west=118421, south=484233, east=121256, north=486076, bottom=-50
)
print(ds)

mz, mx, my = np.meshgrid(ds.z.values, ds.x.values, ds.y.values, indexing="ij")
point_cloud = list(zip(mx.flatten(), my.flatten(), mz.flatten() + 0.25))

# create pyvista object
var = "lithok"  # lithok/ strat
pdata = pyvista.PolyData(point_cloud)
pdata[var] = ds[var].values.flatten()

# create many cubes from the point cloud
cube = pyvista.Cube(x_length=100, y_length=100, z_length=0.5)
pc = pdata.glyph(scale=False, geom=cube, orient=False)

# color
df, CD = _link[var]
colormap = []
label = []
for i, row in df.loc[df["VOXEL_NR"].isin(ds[var].values.flatten())].iterrows():
    colormap.append(
        np.array([row.RED_DEC / 255, row.GREEN_DEC / 255, row.BLUE_DEC / 255])
    )
    label.append(row[CD])

pc.plot(scalars=var, cmap=ListedColormap(colormap))
