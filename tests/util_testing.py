#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 31 14:51:33 2026

@author: and
"""
import pandas as pd
import xarray as xr
from xarray_time_indexing.config import ABS_COORD, DLT_COORD, REF_COORD 


def _create_test_dataset():
    new_array = xr.DataArray(
        [range(11)],
        dims=[REF_COORD, DLT_COORD],
        coords=dict(
            ref_time=([REF_COORD], pd.DatetimeIndex(['2024-02-15 22:00:00'],dtype="datetime64[ns]")),
            delta=([DLT_COORD], pd.TimedeltaIndex(pd.timedelta_range('0h', '10h', periods=11),dtype="timedelta64[ns]")),
        ),
    )

    ds = xr.Dataset()
    ds['test'] = new_array
    ds.attrs['tz'] = 'UTC'

    return ds
