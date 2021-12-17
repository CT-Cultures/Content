import scrapy


class ifspSpider(scrapy.Spider):
    name = "ifsp"

    def start_requests(self):
        urls = [
            'https://www.ifsp.tv/list?star=&page=1&pageSize=32&cid=0,1,3,19&year=-1&language=-1&region=-1&status=-1&orderBy=0&desc=true',
        ]
        for url in urls:
            yield scrapy.Request(url, self.parse_result, meta={
    'splash': {
        'args': {
            # set rendering arguments here
            'html': 1,
            'png': 1,

            # 'url' is prefilled from request url
            # 'http_method' is set to 'POST' for POST requests
            # 'body' is set to request body for POST requests
        },

        # optional parameters
        #'endpoint': 'render.json',  # optional; default is render.json
        #'splash_url': '<url>',      # optional; overrides SPLASH_URL
        #'slot_policy': scrapy_splash.SlotPolicy.PER_DOMAIN,
        #'splash_headers': {},       # optional; a dict with headers sent to Splash
        #'dont_process_response': True, # optional, default is False
        #'dont_send_headers': True,  # optional, default is False
        #'magic_response': False,    # optional, default is True
    }
})
    def parse_result(self, response):
        page = response.splash['html']
        filename = f'ifsp-{page}.html'
        with open(filename, 'wb') as f:
            f.write(response.body) #response.body
        self.log(f'Saved file {filename}')