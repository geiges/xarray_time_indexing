#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 17 22:07:55 2024

@author: and
"""

import xarray as xr
import pandas as pd
from xarray_time_indexing.config import ABS_COORD
from .util_testing import _create_test_dataset




def test_timezone_transformations():
    ds_exp = _create_test_dataset().tix.to_abs_time()

    # convert to CET and back
    ds_obs = ds_exp.tix.tz_localize()
    ds_obs = ds_obs.tix.tz_convert('CET')
    assert str(ds_obs.indexes[ABS_COORD].tzinfo) == 'CET'
    ds_obs = ds_obs.tix.tz_convert('UTC')
    ds_obs = ds_obs.tix.tz_delocalize()

    assert xr.Dataset.equals(ds_obs, ds_exp)

