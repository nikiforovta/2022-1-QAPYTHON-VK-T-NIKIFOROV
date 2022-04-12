import os
import re


def log_parse(top_type='method'):
    request_type = dict()
    top_urls = dict()
    top_5_4xx = list()
    top_5_5xx = dict()
    pattern = re.compile(
        r"((\b25[0-5]|\b2[0-4][0-9]|\b[01]?[0-9][0-9]?)(\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){3})"
        r" - (\w*)- \[(\d{1,2}\/\w+\/\d{4}:\d{2}:\d{2}:\d{2} \+\d{4})\] "
        r"(\"(.+) (https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~=]{1,256}\.[a-zA-Z0-9()]{1,6}\b)?"
        r"([-a-zA-Z0-9()!@:%_\+,;.~#;?$|\*\[\]\{\}\'\\&\/=]*) HTTP\/1.[10]\") (\d{3}) ([\d\-]+)\s?"
        r"(\"(https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~=]{1,256}\.[a-zA-Z0-9()]{1,6}\b)?"
        r"([-a-zA-Z0-9()!@:%_\+,;.~#;?$|\*\[\]\{\}\'&\/=]*)\")?\s?((\".+\")\s?)+")
    with open(os.path.join(os.path.abspath(os.path.join(__file__, os.pardir)), 'access.log')) as logs:
        for log in logs:
            res = pattern.match(log)

            ip = res.group(1)
            method = res.group(8)
            base_url = res.group(9)
            path = res.group(11)
            status_code = res.group(12)
            bytes_size = res.group(13)

            if method in request_type.keys():
                request_type[method] += 1
            else:
                request_type[method] = 1

            url = ''
            if base_url:
                url += base_url
            if path:
                url += path
            if url in top_urls.keys():
                top_urls[url] += 1
            else:
                top_urls[url] = 1

            if status_code[0] == "4":
                top_5_4xx.append(
                    {"url": url, "status_code": status_code, "headers_byte_size": bytes_size, "ip": ip})
            elif status_code[0] == "5":
                if ip in top_5_5xx.keys():
                    top_5_5xx[ip] += 1
                else:
                    top_5_5xx[ip] = 1
    request_type = dict(sorted(request_type.items(), key=lambda item: item[1], reverse=True))
    top_urls = dict(sorted(top_urls.items(), key=lambda item: item[1], reverse=True))
    top_5_4xx = list(sorted(top_5_4xx, key=lambda item: item['headers_byte_size'], reverse=True))
    top_5_5xx = dict(sorted(top_5_5xx.items(), key=lambda item: item[1], reverse=True))

    if top_type == 'method':
        return request_type
    elif top_type == '10':
        return list(top_urls.items())[:10]
    elif top_type == '4xx':
        return top_5_4xx[:5]
    elif top_type == '5xx':
        return list(top_5_5xx.items())[:5]
