import base58
from django.http import HttpResponse
import json

def json_view(func):
    """
    A simple function wrapper that decorates API calls and returns JSON.

    """
    def wrap(request, *a, **kw):
        code = 200
        response = func(request, *a, **kw)
        try:
            if isinstance(response, dict):
                response = dict(response)
                if 'result' not in response:
                    response['result'] = 'ok'
        except KeyboardInterrupt:
            # Allow keyboard interrupts through for debugging.
            raise
        except Http404:
            raise Http404
        except Exception, e:
            response = {'result': 'error',
                    'text': unicode(e)}
            code = 500

        return HttpResponse(json.dumps(response), mimetype="application/json", status=code)

    return wrap
