import scrapy
from scrapy_splash import SplashRequest

script = """
function main(splash)
  splash:init_cookies(splash.args.cookies)
  assert(splash:go{
    splash.args.url,
    headers=splash.args.headers,
    http_method=splash.args.http_method,
    body=splash.args.body,
    })
  assert(splash:wait(0.5))

  local entries = splash:history()
  local last_response = entries[#entries].response
  return {
    url = splash:url(),
    headers = last_response.headers,
    http_status = last_response.status,
    cookies = splash:get_cookies(),
    html = splash:html(),
  }
end
"""

class ifspSpider(scrapy.Spider):
    name = "ifsp"

    def start_requests(self):
        urls = [
            'https://www.ifsp.tv/movie',
        ]

        for url in urls:
            yield SplashRequest(url, self.parse_result,
                endpoint='execute',
                cache_args=['lua_source'],
                args={'lua_source': script},
                headers={'X-My-Header': 'value'},
            )
            
    def parse_result(self, response):
        page = response.url.split("/")[-2]
        filename = f'ifsp-{page}.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log(f'Saved file {filename}')