#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 30 18:13:35 2026

@author: and
"""

import xarray as xr

import xarray_time_index as tix


def test_integration_dataset():
    
    ds = xr.Dataset()
    
    assert hasattr(ds, 'tix')
    
    
def test_integration_dataarray():
    
    da = xr.DataArray()
    
    assert hasattr(da, 'tix')