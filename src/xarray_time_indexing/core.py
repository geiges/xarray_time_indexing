#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 30 13:37:36 2026

@author: and
"""
import xarray as xr
import pandas as pd
from .config import ABS_COORD, DLT_COORD, REF_COORD

# %% Functions


def assert_same_timezone(*datasets):
    timezone_meta = [ds.attrs['tz'] for ds in datasets]
    if len(set(timezone_meta)) > 1:
        raise (Exception('Multiple different timezones found'))

    return timezone_meta[0]




def switch_to_absolute_time(ds):
    ds = ds.copy()
    # ds.coords[DLT_COORD] = pd.Timestamp(ds.ref_time.item()) + pd.TimedeltaIndex(ds.delta)
    if REF_COORD in ds.indexes:
        ds.coords[DLT_COORD] = ds.indexes[REF_COORD][0] + pd.TimedeltaIndex(ds.delta)
    elif REF_COORD in ds.coords:
        ds.coords[DLT_COORD] = pd.Timestamp(ds.ref_time.item()) + pd.TimedeltaIndex(
            ds.delta
        )
    else:
        raise (Exception('ref_time not in coordinates or indexes'))

    # ds.attrs[REF_COORD] = pd.Timestamp(ds.ref_time.item())

    ds = ds.rename({DLT_COORD: ABS_COORD})

    try:
        ds = ds.squeeze(REF_COORD)
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
    ds.coords[ABS_COORD] = (
        DLT_COORD,
        pd.Timestamp(ds.ref_time.item()) + pd.TimedeltaIndex(ds.delta),
    )
    return ds


def switch_to_delta_time(ds, ref_time=None):
    if ref_time is None:
        ref_time = pd.Timestamp(ds.ref_time.item())
    ds = ds.copy()
    ds.coords[ABS_COORD] = pd.DatetimeIndex(ds.time) - pd.Timestamp(ref_time)
    ds = ds.rename({ABS_COORD: DLT_COORD})

    if REF_COORD not in ds.coords:
        # ds.assign_coords(ref_time = pd.DatetimeIndex([ref_time,]))
        # ds = ds.expand_dims(REF_COORD)
        if REF_COORD not in ds.dims:
            ds = ds.expand_dims(dim=REF_COORD)
        ds.coords[REF_COORD] = pd.DatetimeIndex([ref_time])
    else:
        if REF_COORD not in ds.dims:
            ds = ds.expand_dims(dim=REF_COORD)

        ds.coords[REF_COORD] = pd.DatetimeIndex([ref_time])

    if isinstance(ds, xr.Dataset):
        ds = ds.transpose(*list(ds.sizes.keys()))
    elif isinstance(ds, xr.Dataset):
        ds = ds.transpose(*ds.sizes)
    return ds
