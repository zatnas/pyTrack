from werkzeug.datastructures import ImmutableMultiDict


def Dict(input):
    if isinstance(input, ImmutableMultiDict):
        return input.to_dict(flat=True)
    else:
        return dict(input)


def Validate(required_params, input_params):
    error_msg = []
    params = Dict(input_params)
    for param_name, required in required_params.items():
        if required and param_name not in params:
            error_msg += [f"{ param_name } is required but not found"]
        if param_name in params:
            del params[param_name]
    for param_name in params.keys():
        error_msg += [f"{ param_name } is not a valid parameter"]
    validity = bool(error_msg)
    return (validity, error_msg)
