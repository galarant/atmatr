import binascii
try:
    import simplejson as json
except ImportError:
    import json
#import vcr as vcr_


# TODO: These should go into pytest_config
def get_function_closure(fn):
    """
    Get the given function's closure as a dictionary for ease of access to
    closure objects. Returns None if the given function has no closure
    available.

    :param function fn: The function to get the closure for.

    :rtype dict: The function closure translated to a dictionary.

    """
    if fn.func_closure:
        closure_vars = [c.cell_contents for c in fn.func_closure]
        closure = dict(zip(fn.func_code.co_freevars, closure_vars))
        return closure


def profile(func):
    """
    Decorator that profiles a function with cProfile and produces output
    """
    def wrapper(*args, **kwargs):
        import cProfile
        import pstats
        import StringIO
        pr = cProfile.Profile()
        pr.enable()
        retval = func(*args, **kwargs)
        pr.disable()
        s = StringIO.StringIO()
        sortby = 'cumulative'
        ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
        ps.print_stats()
        print s.getvalue()
        return retval

    return wrapper


class VCRSerializer(object):

    """
    VCR custom serializer to force the cassettes content to stay in 1 line,
    for ease readability on Git diffs.
    """
    # Serializers

    def serialize(self, cassette_dict):
        try:
            return json.dumps(cassette_dict)
        except UnicodeDecodeError:
            return self.serialize_binaries(cassette_dict)

    def serialize_binaries(self, cassette_dict):
        def _serialize_obj(value):
            if isinstance(value, dict):
                value = dict([(k, _serialize_obj(v)) for k, v in value.iteritems()])
            elif isinstance(value, list):
                value = [_serialize_obj(o) for o in value]
            else:
                try:
                    unicode(value)
                except UnicodeDecodeError:  # binary data, encode it to base64
                    value = value.encode('base64')
            return value

        for index, interaction in enumerate(cassette_dict['interactions']):
            # serialize requests
            request_body = _serialize_obj(interaction['request']['body'])
            cassette_dict['interactions'][index]['request']['body'] = request_body
            # serialize responses
            response_body = _serialize_obj(interaction['response']['body'])
            cassette_dict['interactions'][index]['response']['body'] = response_body
        return json.dumps(cassette_dict)

    # Deserializers
    def deserialize(self, cassette_string):
        def _deserialize_obj(value):
            if isinstance(value, dict):
                return dict([(k, _deserialize_obj(v)) for k, v in value.iteritems()])
            elif isinstance(value, list):
                return [_deserialize_obj(o) for o in value]
            else:
                try:
                    try:
                        json.loads(value)  # don't decode matching JSONified strings
                        return value
                    except:
                        return value.decode('base64')
                except (binascii.Error, AttributeError):
                    # many, if not all, non-string objects have no .decode() method
                    return value

        cassette_dict = json.loads(cassette_string)
        for index, interaction in enumerate(cassette_dict['interactions']):
            # deserialize requests
            request_body = _deserialize_obj(interaction['request']['body'])
            cassette_dict['interactions'][index]['request']['body'] = request_body
            # deserialize responses
            response_body = _deserialize_obj(interaction['response']['body'])
            cassette_dict['interactions'][index]['response']['body'] = response_body
        return cassette_dict

"""
vcr = vcr_.VCR(
    cassette_library_dir='tests/cassettes',
    filter_headers=['x-fb-debug', 'Authorization'],
    filter_query_parameters=['fb_exchange_token', 'client_id',
                             'client_secret', 'access_token']
)
vcr.register_serializer('discotech', VCRSerializer())
vcr.serializer = 'discotech'
"""
