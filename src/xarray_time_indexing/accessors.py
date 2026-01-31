#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 30 13:37:00 2026

@author: and
"""
import xarray as xr

from .core import switch_to_absolute_time, switch_to_delta_time
from .config import ABS_COORD, DLT_COORD, REF_COORD


if not hasattr(xr.Dataset, 'tix'):

    @xr.register_dataset_accessor("tix")
    @xr.register_dataarray_accessor("tix")
    class TimeIndexAccessor:
        def __init__(self, xarray_obj):
            self._obj = xarray_obj

        def to_abs_time(self):
            return switch_to_absolute_time(self._obj)

        def to_delta_time(self, ref_time=None):
            return switch_to_delta_time(self._obj, ref_time)

        def tz_localize(self):
            if ABS_COORD not in self._obj.coords.keys():
                raise (Exception(f'{ABS_COORD} must be in coordinates'))

            ds = self._obj.copy()
            ds.coords[ABS_COORD] = ds.indexes[ABS_COORD].tz_localize(ds.attrs['tz'])
            return ds

        def tz_delocalize(self):
            if ABS_COORD not in self._obj.coords.keys():
                raise (Exception('{ABS_COORD} must be in coordinates'))

            ds = self._obj.copy()
            ds.coords[ABS_COORD] = ds.indexes[ABS_COORD].tz_localize(None)
            return ds

        def tz_convert(self, tz):
            if ABS_COORD not in self._obj.coords.keys():
                raise (Exception('{ABS_COORD} must be in coordinates'))
            ds = self._obj.copy()

            if ds.indexes[ABS_COORD].tzinfo is None:
                ds = ds.tix.tz_localize()
            ds.coords[ABS_COORD] = ds.indexes[ABS_COORD].tz_convert(tz)
            ds.attrs['tz'] = tz
            return ds
