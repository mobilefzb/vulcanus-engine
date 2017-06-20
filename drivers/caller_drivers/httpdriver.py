#!/usr/bin/env python
# coding=utf8
import log_conf.logconfig
import logging
import requests
from requests.exceptions import ConnectionError, Timeout, HTTPError

logger = logging.getLogger("httpdriver")


class HTTPClient(object):

    def method_get(self, url, req_params, req_headers, req_timeout):

        """
        :param url: 字符串类型   需要访问的目标URL
        :param req_params:  字典类型  Get方法特有的请求URL参数列表 eg:http://httpbin.org/get?key2=value2&key1=value1
        :param req_headers: 字典类型  每个request都可以使用
        :param req_timeout: Integer  请求的超时时间
        :return:
        """

        try:

            response = requests.get(url, params=req_params, headers=req_headers, timeout=req_timeout)
            print response

        except Timeout as e:

            error_msg = "HTTP Get URL %s timeout. Message: %s " % (url, e)
            logger.error(error_msg)

        except ConnectionError as e:

            error_msg = "HTTP Get URL %s error. Message: %s" % (url, e)
            logger.error(error_msg)

        except Exception as e:

            error_msg = "HTTP Get URL %s Unkown Error. Message: %s" % (url, e)
            logger.error(error_msg)

        finally:
            # print 'final'
            raise e

    def method_post(self, url, req_body, req_headers, req_timeout):

        """
        :param url: 字符串类型   需要访问的目标URL
        :param req_body:  字典类型  POST方法的请求体内内容
        :param req_headers: 字典类型  每个request都可以使用
        :param req_timeout: Integer  请求的超时时间
        :return:
        """
        try:

            response = requests.post(url, data=req_body, headers=req_headers, timeout=req_timeout)
            return response

        except Timeout as e:

            error_msg = "HTTP POST URL %s timeout. Message: %s " % (url, e)

            logger.error(error_msg)

        except ConnectionError as e:

            error_msg = "HTTP POST URL %s error. Message: %s" % (url, e)

            logger.error(error_msg)

        except Exception as e:

            error_msg = "HTTP POST URL %s Unkown Error. Message: %s" % (url, e)

            logger.error(error_msg)

    def method_put(self, url, req_data, req_headers, req_timeout):

        """
        :param url: 字符串类型   需要访问的目标URL
        :param req_data: 字典类型   PUT方法的请求体内容
        :param req_headers: 字典类型   PUT方法的请求头
        :param req_timeout: Integer   请求的超时时间
        :return:
        """

        try:

            response = requests.put(url, data=req_data, headers=req_headers, timeout=req_timeout)
            return response

        except Timeout as e:

            error_msg = "HTTP PUT URL %s timeout. Message: %s " % (url, e)

            logger.error(error_msg)

        except ConnectionError as e:

            error_msg = "HTTP PUT URL %s error. Message: %s" % (url, e)

            logger.error(error_msg)

        except Exception as e:

            error_msg = "HTTP PUT URL %s Unkown Error. Message: %s" % (url, e)

            logger.error(error_msg)

    def method_delete(self, url, req_headers, req_timeout):

        """
        :param url: 字符串类型   需要访问的URL
        :param req_headers: 字典类型    请求的请求头
        :param req_timeout: Integer    请求的超时时间
        :return:
        """

        try:

            response = requests.delete(url, headers=req_headers, timeout=req_timeout)
            return response

        except Timeout as e:

            error_msg = "HTTP DELETE URL %s timeout. Message: %s " % (url, e)

            logger.error(error_msg)

        except ConnectionError as e:

            error_msg = "HTTP DELETE URL %s error. Message: %s" % (url, e)

            logger.error(error_msg)

        except Exception as e:

            error_msg = "HTTP DELETE URL %s Unkown Error. Message: %s" % (url, e)

            logger.error(error_msg)

    def method_option(self, url, req_headers, req_timeout):

        """
        :param url: 字符串类型   需要访问的URL
        :param req_headers: 字典类型    请求的请求头
        :param req_timeout: Integer    请求的超时时间
        :return:
        """

        try:

            response = requests.options(url, headers=req_headers, timeout=req_timeout)
            return response

        except Timeout as e:

            error_msg = "HTTP OPTION URL %s timeout. Message: %s " % (url, e)

            logger.error(error_msg)

        except ConnectionError as e:

            error_msg = "HTTP OPTION URL %s error. Message: %s" % (url, e)

            logger.error(error_msg)

        except Exception as e:

            error_msg = "HTTP OPTION URL %s Unkown Error. Message: %s" % (url, e)

            logger.error(error_msg)

    def get_result(self, response):

        """


        Requests 会自动解码来自服务器的内容。大多数 unicode 字符集都能被无缝地解码。
        请求发出后，Requests 会基于 HTTP 头部对响应的编码作出有根据的推测。当你访问 r.text 之时，Requests 会使用其推测的文本编码。
        你可以找出  Requests 使用了什么编码，并且能够使用 r.encoding 属性来改变它：
        如果你改变了编码，每当你访问 r.text ，Request 都将会使用 r.encoding 的新值。
        你可能希望在使用特殊逻辑计算出文本的编码的情况下来修改编码。比如 HTTP 和 XML 自身可以指定编码。
        这样的话，你应该使用 r.content 来找到编码，然后设置 r.encoding 为相应的编码。这样就能使用正确的编码解析 r.text 了。

        如果 JSON 解码失败， r.json 就会抛出一个异常。例如，相应内容是 401 (Unauthorized)，
        尝试访问 r.json 将会抛出 ValueError: No JSON object could be decoded 异常。

        :param response:
        :return:
        """

        # response = requests.get('https://github.com/timeline.json')
        try:
            if not response.status_code == requests.codes.ok:
                response.raise_for_status()

            return response.json()

        except HTTPError as e:

            error_msg = "Get HTTP Request Result Status Error %s " % e.message
            logger.error(error_msg)

        except ValueError as e:

            error_msg = "HTTP Response Convert to json faild. Message: %s" % e.message
            logger.error(error_msg)

        except Exception as e:

            error_msg = "Get HTTP Request Result  %s Unkown Error. Message: %s" % e

            logger.error(error_msg)


if __name__ == '__main__':

    url = "http://dfcasdwqweqeqwe.com"
    client = HTTPClient()

    client.method_get(url, None, None, 3)


    # POST
    # payload = {'key1': 'value1', 'key2': 'value2'}
    # result = client.method_post("http://httpbin.org/post", payload,{}, 3)
    # content = client.get_result(result)
    # print str(content.get("origin"))

