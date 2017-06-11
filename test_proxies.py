{"url":"http:\/\/proxy.mimvp.com","result":[{"ip:port":"186.225.229.145:1080","http_type":"Socks4"},{"ip:port":"85.174.227.32:8080","http_type":"HTTP"},{"ip:port":"117.143.109.144:80","http_type":"HTTP"},{"ip:port":"188.166.83.34:3128","http_type":"HTTP"},{"ip:port":"62.84.66.39:872","http_type":"HTTP"},{"ip:port":"91.134.138.212:3128","http_type":"HTTP\/HTTPS"},{"ip:port":"160.202.42.210:8080","http_type":"HTTP\/HTTPS"},{"ip:port":"79.130.51.131:3128","http_type":"HTTP\/HTTPS"},{"ip:port":"113.57.97.82:808","http_type":"HTTP\/HTTPS"},{"ip:port":"94.177.234.46:1189","http_type":"HTTP\/HTTPS"},{"ip:port":"175.5.171.149:8998","http_type":"HTTP\/HTTPS"},{"ip:port":"203.142.72.114:808","http_type":"HTTP\/HTTPS"},{"ip:port":"209.66.119.149:8080","http_type":"HTTPS"},{"ip:port":"185.35.67.119:1189","http_type":"HTTP\/HTTPS"},{"ip:port":"171.37.251.84:8998","http_type":"HTTP\/HTTPS"},{"ip:port":"185.35.67.152:1189","http_type":"HTTP\/HTTPS"},{"ip:port":"142.147.117.1:8080","http_type":"HTTP"},{"ip:port":"115.222.23.64:8998","http_type":"HTTP\/HTTPS"},{"ip:port":"190.205.2.66:80","http_type":"HTTP"},{"ip:port":"89.40.112.65:1189","http_type":"HTTP\/HTTPS"}]}

class Client():

    def __init__(self):
        self._session = requests.Session()
        self.proxies = None

    def set_proxy_pool(self, proxies, auth=None, https=True):
        """Randomly choose a proxy for every GET/POST request
        :param proxies: list of proxies, like ["ip1:port1", "ip2:port2"]
        :param auth: if proxy needs auth
        :param https: default is True, pass False if you don't need https proxy
        """
        from random import choice

        if https:
            self.proxies = [{'http': 'http://' + p, 'https': 'https://' + p} for p in proxies]
        else:
            self.proxies = [{'http': 'http://' + p} for p in proxies]

        def get_with_random_proxy(url, **kwargs):
            proxy = choice(self.proxies)
            kwargs['proxies'] = proxy
            if auth:
                kwargs['auth'] = auth
            return self._session.original_get(url, **kwargs)

        def post_with_random_proxy(url, *args, **kwargs):
            proxy = choice(self.proxies)
            kwargs['proxies'] = proxy
            if auth:
                kwargs['auth'] = auth
            return self._session.original_post(url, *args, **kwargs)

        self._session.original_get = self._session.get
        self._session.get = get_with_random_proxy
        self._session.original_post = self._session.post
        self._session.post = post_with_random_proxy

    def remove_proxy_pool(self):
        self.proxies = None
        self._session.get = self._session.original_get
        self._session.post = self._session.original_post
        del self._session.original_get
        del self._session.original_post