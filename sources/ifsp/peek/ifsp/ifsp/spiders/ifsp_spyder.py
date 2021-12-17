import scrapy


class ifspSpider(scrapy.Spider):
    name = "ifsp"

    def start_requests(self):
        urls = [
            'https://www.ifsp.tv/list?star=&page=1&pageSize=32&cid=0,1,3,19&year=-1&language=-1&region=-1&status=-1&orderBy=0&desc=true',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = f'ifsp-{page}.html'
        with open(filename, 'wb') as f:
            f.write(response.body) #response.body
        self.log(f'Saved file {filename}')