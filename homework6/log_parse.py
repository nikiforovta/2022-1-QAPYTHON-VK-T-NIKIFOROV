def get_top(logs, top_type='method', quantity=10):
    result = dict()
    if top_type == 'method':
        METHODS = ['POST', 'GET', 'HEAD', 'PUT', 'PATCH', 'DELETE', 'CONNECT', 'OPTIONS', 'TRACE']
        for log in logs:
            method = log.group(8)
            if method in METHODS:
                result[method] = result.setdefault(method, 0) + 1
        return dict(sorted(result.items(), key=lambda item: item[1], reverse=True))
    elif top_type == 'frequency':
        for log in logs:
            base_url = log.group(9)
            path = log.group(11)
            url = base_url or ''
            url += path or ''
            result[url] = result.setdefault(url, 0) + 1
        return list(dict(sorted(result.items(), key=lambda item: item[1], reverse=True)).items())[:quantity]
    elif top_type == '4xx':
        result = list()
        for log in logs:
            ip = log.group(1)
            base_url = log.group(9)
            path = log.group(11)
            status_code = log.group(12)
            url = base_url or ''
            url += path or ''
            bytes_size = log.group(13)
            if status_code[0] == "4":
                result.append({"url": url, "status_code": status_code, "headers_byte_size": bytes_size, "ip": ip})
        return list(sorted(result, key=lambda item: item['headers_byte_size'], reverse=True))[:quantity]
    elif top_type == '5xx':
        for log in logs:
            ip = log.group(1)
            status_code = log.group(12)
            if status_code[0] == "5":
                result[ip] = result.setdefault(ip, 0) + 1
        return list(dict(sorted(result.items(), key=lambda item: item[1], reverse=True)).items())[:quantity]
