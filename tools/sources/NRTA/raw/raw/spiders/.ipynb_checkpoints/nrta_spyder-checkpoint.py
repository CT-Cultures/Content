import scrapy

class NRTASpider(scrapy.Spider):
    
    name = 'nrta'
    
    def start_requests(self):
        urls = [
            'https://dsj.nrta.gov.cn/tims/site/views/applications.shanty?appName=note',
            'https://dsj.nrta.gov.cn/tims/site/views/applications.shanty?appName=importantLixiang',
            'https://dsj.nrta.gov.cn/tims/site/views/applications.shanty?appName=importantShezhi',
            'https://dsj.nrta.gov.cn/tims/site/views/applications.shanty?appName=changing',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
    
    def parse(self, response):
        page = response.url.split('=')[-1]
        filename = f'nrta-{page}.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log(f'Saved file {filename}')