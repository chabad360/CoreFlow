import sys
from functools import wraps
import copy
import frappe
import json

def _get_memoized_value(func, args, kwargs):
    """Used internally by memoize decorator to get/store function results"""
    key = frappe.generate_hash(json.dumps([func.__name__, repr(args), repr(kwargs)]))

    cache = frappe.cache()
    
    if not key in func._cache_dict:
        ret = func(*args, **kwargs)
        func._cache_dict[key] = ret

    return copy.deepcopy(func._cache_dict[key])

def memoize(func):
    """Decorator that stores function results in a dictionary to be used on the
    next time that the same arguments were informed."""

    func._cache_dict = {}

    def _inner(*args, **kwargs):
        return _get_memoized_value(func, args, kwargs)

    if sys.version.startswith('2.4'):
        return _inner
    else:
        return wraps(func)(_inner)