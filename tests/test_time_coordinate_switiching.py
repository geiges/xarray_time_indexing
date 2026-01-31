#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 17 22:07:55 2024

@author: and
"""

import xarray as xr
import pandas as pd
import xarray_time_indexing
#from xarray_time_indexing.config import ABS_COORD, DLT_COORD, REF_COORD 
#from xarray_time_indexing.config import ABS_COORD
# from . import util_testing
from .util_testing import _create_test_dataset



def test_switch_dataset():
    ds_exp = _create_test_dataset()

    ds_obs = ds_exp.tix.to_abs_time().tix.to_delta_time()

    assert xr.Dataset.equals(ds_obs, ds_exp)


