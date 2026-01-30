#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 30 13:37:36 2026

@author: and
"""
import xarray as xr
import pandas as pd

def assert_same_timezone(*datasets):
    timezone_meta = [ds.attrs['tz'] for ds in datasets]
    if len(set(timezone_meta)) > 1:
        raise (Exception('Multiple different timezones found'))

    return timezone_meta[0]


# %% Functions


def switch_to_absolute_time(ds):
    ds = ds.copy()
    # ds.coords['delta'] = pd.Timestamp(ds.ref_time.item()) + pd.TimedeltaIndex(ds.delta)
    if 'ref_time' in ds.indexes:
        ds.coords['delta'] = ds.indexes['ref_time'][0] + pd.TimedeltaIndex(ds.delta)
    elif 'ref_time' in ds.coords:
        ds.coords['delta'] = pd.Timestamp(ds.ref_time.item()) + pd.TimedeltaIndex(
            ds.delta
        )
    else:
        raise (Exception('ref_time not in coordinates or indexes'))

    # ds.attrs['ref_time'] = pd.Timestamp(ds.ref_time.item())

    ds = ds.rename({'delta': 'time'})

    try:
        ds = ds.squeeze('ref_time')
    except Exception:
        pass
    return ds


def add_absolute_time(ds):
    # only possible if there is only one reference time
    if ds.ref_time.size > 1:
        raise (
            Exception('More than one refernce time in data. Absolute time not unique')
        )
    ds = ds.copy()
    ds.coords['time'] = (
        'delta',
        pd.Timestamp(ds.ref_time.item()) + pd.TimedeltaIndex(ds.delta),
    )
    return ds


def switch_to_delta_time(ds, ref_time=None):
    if ref_time is None:
        ref_time = pd.Timestamp(ds.ref_time.item())
    ds = ds.copy()
    ds.coords['time'] = pd.DatetimeIndex(ds.time) - pd.Timestamp(ref_time)
    ds = ds.rename({'time': 'delta'})

    if 'ref_time' not in ds.coords:
        # ds.assign_coords(ref_time = pd.DatetimeIndex([ref_time,]))
        # ds = ds.expand_dims('ref_time')
        if 'ref_time' not in ds.dims:
            ds = ds.expand_dims(dim="ref_time")
        ds.coords['ref_time'] = pd.DatetimeIndex([ref_time])
    else:
        if 'ref_time' not in ds.dims:
            ds = ds.expand_dims(dim="ref_time")

        ds.coords['ref_time'] = pd.DatetimeIndex([ref_time])

    if isinstance(ds, xr.Dataset):
        ds = ds.transpose(*list(ds.dims.keys()))
    elif isinstance(ds, xr.Dataset):
        ds = ds.transpose(*ds.dims)
    return ds
