from typing import Any

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt

import bromodels

_link = {
    "lithok": (bromodels.GeoTop.geotop_lithology_class(), "LITHO_CLASS_CD"),
    "strat": (bromodels.GeoTop.geotop_stratigraphic_unit(), "STR_UNIT_CD"),
}

soildata = bromodels.GeoTopColumn()

var = "strat"

fig, ax = plt.subplots()
df, CD = _link[var]
for z, nr in zip(soildata.z.values, soildata[var].values):
    ax.fill_between(
        [soildata.x.values, soildata.x.values + 100],
        z + 0.5,
        z,
        color=df.loc[df["VOXEL_NR"] == nr][
            ["RED_DEC", "GREEN_DEC", "BLUE_DEC"]
        ].to_numpy()
        / 255,
    )

patch_list = []
for i, row in df.loc[df["VOXEL_NR"].isin(soildata[var].values)].iterrows():
    data_key = mpatches.Patch(
        color=(row.RED_DEC / 255, row.GREEN_DEC / 255, row.BLUE_DEC / 255),
        label=row[CD],
    )
    patch_list.append(data_key)

plt.legend(handles=patch_list, bbox_to_anchor=(1, 1), loc="upper left")
plt.tight_layout()
plt.pause(5)
plt.close()

var = "lithok"

fig, ax = plt.subplots()
df, CD = _link[var]
for z, nr in zip(soildata.z.values, soildata[var].values):
    ax.fill_between(
        [soildata.x.values, soildata.x.values + 100],
        z + 0.5,
        z,
        color=df.loc[df["VOXEL_NR"] == nr][
            ["RED_DEC", "GREEN_DEC", "BLUE_DEC"]
        ].to_numpy()
        / 255,
    )

patch_list = []
for i, row in df.loc[df["VOXEL_NR"].isin(soildata[var].values)].iterrows():
    data_key = mpatches.Patch(
        color=(row.RED_DEC / 255, row.GREEN_DEC / 255, row.BLUE_DEC / 255),
        label=row[CD],
    )
    patch_list.append(data_key)

plt.legend(handles=patch_list, bbox_to_anchor=(1, 1), loc="upper left")
plt.tight_layout()
plt.pause(5)
plt.close()


def bytes2str(var: Any) -> str:
    return var.tobytes().decode("utf-8").rstrip("\x00")


soildata = bromodels.RegisColumn()

fig, ax = plt.subplots()
df = bromodels.Regis.regis_stratigraphic_unit()
for top, botm, layer in zip(
    soildata.top.values, soildata.bottom.values, soildata.layer.values
):
    ax.fill_between(
        [soildata.x.values, soildata.x.values + 100],
        top,
        botm,
        color=df.loc[df["HYD_UNIT_CD"] == bytes2str(layer)][
            ["RED_DEC", "GREEN_DEC", "BLUE_DEC"]
        ].to_numpy()
        / 255,
    )

patch_list = []
for i, row in df.loc[
    df["HYD_UNIT_CD"].isin([bytes2str(var) for var in soildata.layer.values])
].iterrows():
    data_key = mpatches.Patch(
        color=(row.RED_DEC / 255, row.GREEN_DEC / 255, row.BLUE_DEC / 255),
        label=row.HYD_UNIT_CD,
    )
    patch_list.append(data_key)

plt.legend(handles=patch_list, bbox_to_anchor=(1, 1), loc="upper left")
plt.tight_layout()
plt.pause(5)
plt.close()
