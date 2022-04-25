import json, urllib

def paginate(data, params, prefix = ''):
    start = (params['page_num'] - 1) * params['page_size']
    end = start + params['page_size']

    data = data[start:end]
    
    response = {
        'total': data.count(),
        'at_page': min(data.count()-params['page_size']*(params['page_num']-1), params['page_size']),
        'pagination': {},
        'data': json.loads(data.to_json())
    }

    prev = params['page_num'] - 1
    next = params['page_num'] + 1
    params['page_num'] = prev
    url_prev = urllib.parse.urlencode(params)
    params['page_num'] = next
    url_next = urllib.parse.urlencode(params)

    if prev <= 0:
        response['pagination']['previous'] = None
    else:
        response['pagination']['previous'] = prefix + '?' + url_prev

    if end >= response['total']:
        response['pagination']['next'] = None
    else:
        response['pagination']['next'] = prefix + '?' + url_next

    return response