import datetime
import json
import re
from optparse import OptionParser


def main(jsonify=False):
    found = 0
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
    with open('access.log') as logs:
        for log in logs:
            res = pattern.match(log)
            if res:
                found += 1

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

    if jsonify:
        with open('python_results.json', 'w+') as results:
            json.dump({'Total requests': found,
                       'Requests by method': request_type,
                       'Top 10 requests': list(top_urls.items())[:10],
                       'Top 5 4xx requests': top_5_4xx[:5],
                       'Top 5 5xx requests': list(top_5_5xx.items())[:5]}, results)
    else:
        with open('python_results.txt', 'w+') as results:
            results.writelines(
                [str(found), '\n', str(request_type), '\n', str(list(top_urls.items())[:10]), '\n', str(top_5_4xx[:5]),
                 '\n', str(list(top_5_5xx.items())[:5])])


if __name__ == '__main__':
    begin_time = datetime.datetime.now()
    parser = OptionParser()
    parser.add_option('--json', action="store_true", dest='json', default=False, help='Save results in JSON format')
    (options, args) = parser.parse_args()
    main(jsonify=vars(options)['json'])
    print(datetime.datetime.now() - begin_time)
