# Chache

Author: Sunchasing

Version: 0.9.6

## About

A module that stores, in memory, the return values and call keyword arguments of a function that it is applied to.
Can be set to clean stored data at set intervals in a separate thread.
Records usage statistic for each cached item.

## Usage

### Decorator

To use the cache as a function decorator, use the
`sized_func_cache` class method. This method injects a `cache` attribute in the function.

The parameters it takes are:
- `expiry`: The time (in seconds) it would take for the function call to expire. If unset, is persistent.
- `max_size`: Number of function calls to store. If unset, there is no limit.
- `cleaning_frequency_s`: The interval between checking for expired function calls.

### gRPC server/client

The gRPC cache server can be started via `CacheService` and `start_server`.

The parameters it takes are:
- `max_size`: Number of function calls to store. If unset, there is no limit.
- `cleaning_frequency_s`: The interval between checking for expired function calls.

The client can be started via `CacheClient.initialize_client()`, and needs only a `port`.



## Todo

- Finish gRPC (95%)
- Tests (80%)
- Comprehensible examples (30%)