#!/usr/bin/env python3
# Imports
from pathlib import Path

import plotly.express as px
import polars as pl

node_data = pl.scan_parquet(file="/home/jpatterson87/for_classes/gnn_for_diabetes/data/transformed_data_from_vms/with_nodes/most_node_data.parquet",
                            low_memory=True)

node_data_for_plot = (node_data
    .filter((pl.col("node_id") == 0))
    .collect()
)

node_plot = px.scatter(
           x=node_data_for_plot.select(pl.col("POS")).to_series(),
           y=node_data_for_plot.select(pl.col("ALT_GC_ratio")).to_series(),
           color=node_data_for_plot.select(pl.col("population_description")).to_series(),
           opacity=0.5
)

node_plot.show()