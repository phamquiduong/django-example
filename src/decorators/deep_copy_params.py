from copy import deepcopy


def deep_copy_params(to_call):
    def inner(*args, **kwargs):
        return to_call(*deepcopy(args), **deepcopy(kwargs))
    return inner
