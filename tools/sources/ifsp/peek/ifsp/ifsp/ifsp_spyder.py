# -*- coding: utf-8 -*-
"""
Created on Fri Dec 17 17:28:39 2021

@author: VXhpUS
"""

import scrapy
from scrapy_splash import SplashRequest


class ifspSpider(scrapy.Spider):
    name = "ifsp"
    allowed_domains = ['ifsp.tv']
    start_urls =['https://ifp.tv']
    
    render_script = """
        function main(splash)
            splash.private_mode_enabled = false
            local url = splash.args.url
            assert(splash:go(url))
            assert(splash:wait(5))
            
            local get_divs = splash:jsfunc([[
            function () {
                var body = document.body;
                var divs = body.getElementsByTagName("div");
                return divs
            }
                
                
                ]])
            
            return {
                html = splash:html()
                url = splash:url()
                divs = get_divs()
            }
        end
    """
    def start_requests(self):

        for url in start_urls:
            yield SplashRequest(
                url=url, 
                callback=self.parse_result,
                endpoint=endpoint='execute',
                args={
                    'html': 1,
                    'iframes': 1,
                    'script': 1,
                    'wait': 5,
                    'lua_source': self.render_script,
                }
            )
            
    def parse_result(self, response):
        page = response.url.split("/")[-2]
        filename = f'ifsp-{page}.html'
        ls_titles = response.css('.title-ctn')
        print(ls_titles)
        with open(filename, 'wb') as f:
            f.write(';'.join(ls_titles))
        self.log(f'Saved file {filename}')

#response.xpath('//div[@class="paging"]/p/a[contains(text(),"Next")]/@href')
