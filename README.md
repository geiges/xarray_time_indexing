# Xarray Time Indexing
- Additional accessors and functions for xarray for better handling of datetime like indexes

## Intoduction

Xarray Time Indexing requires the use of an time axis compatible to pandas.Dateime index. For managment of many
dataset, swithing to a reference time in combination of a time_delta index can be useful. This small packages 
does facilitate easy switching between both representations. 