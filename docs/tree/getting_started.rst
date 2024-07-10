.. _getting_started:

Getting started
===============

The easiest way to get started with BROmodels is in the **Nuclei Notebooks**.


Installation
------------
To install this package, including the `map` and `gef` reading functionality, run:

.. code-block::

    pip install bromodels


Than you can import BROmodels as follows:

.. ipython:: python

   import bromodels

or any equivalent :code:`import` statement.

How to use BROmodels repo?
---------------------------

How to plot a GeoTop column?:

.. ipython:: python

    import bromodels
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches

    _link = {
        "lithok": (bromodels.GeoTop.geotop_lithology_class(), "LITHO_CLASS_CD"),
        "strat": (bromodels.GeoTop.geotop_stratigraphic_unit(), "STR_UNIT_CD"),
    }

    # get data
    soildata = bromodels.GeoTopColumn()

    soildata

.. ipython:: python

    # set variable
    var = "strat"

    # create plot
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
    @savefig GEOTOP.png
    plt.tight_layout()

More information about other user cases following soon!
