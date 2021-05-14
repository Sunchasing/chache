# Chache

Author: Sunchasing

Version: 0.2.1

## About

A module that stores, in memory, the return values and call keyword arguments of a function that it is applied to.
Can be set to clean stored data at set intervals in a separate thread.
Records usage statistic for each cached item.

## Usage

### Decorator

To use the cache as a function decorator, use the 
`sized_func_cache` class method.

The parameters it takes are:
 - `expiry`: The time (in seconds) it would take for the function call to expire. If unset, is persistent.
 - `max_size`: Number of function calls to store. If unset, there is no limit.
 - `cleaning_frequency_s`: The interval between checking for expired function calls.
 
### gRPC server/client
Todo

## Todo

- Finish README
- Server/client gRPC
- Tests
- Comprehensible examples (10%)