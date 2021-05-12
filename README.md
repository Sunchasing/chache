# Chache

Author: Sunchasing

Version: 0.2.1

## About

## Usage

### Decorator
To use the cache as a function decorator, use the 
`sized_func_cache` class method.
The parameters it takes are:
 - `expiry`: The time (in seconds) it would take for the function call to expire. If unset, is persistent.
 - `max_size`: Number of function calls to store. If unset, there is no limit.
 - `cleaning_frequency_s`: The interval between checking for expired function calls.
 

## Todo

- Finish README
- Server/client gRPC
- Tests
- Comprehensible examples (10%)