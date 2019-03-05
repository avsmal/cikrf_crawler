import scrapy

class UIKSpider(scrapy.Spider):
    name = "UIK"

    def start_requests(self):
        f = open('spb-2014.list', 'r')
        urls = [x.strip() for x in f.readlines()]
       
        elections = "gub"
        if elections == "gub":
            # parsing gubernator elections
            self.prefix="gub"
            yield scrapy.Request(url=urls[0], callback=self.LocalElectionsParse)
        else:
            # parsing MO elections
            self.prefix="mo"
            for url in urls[1:]:
                yield scrapy.Request(url=url, callback=self.LocalElectionsParse)

    def LocalElectionsParse(self, response):
        oik_urls = response.css('option::attr(value)').getall()
        for url in oik_urls:
            yield scrapy.Request(url=url, callback=self.TIKParse1)

    def TIKParse1(self, response):
        url = response.css('td[height="20px"] > a::attr(href)').getall()[2]
        yield scrapy.Request(url=url, callback=self.TIKParse2)
 
    def TIKParse2(self, response):
        uik_urls = response.css('option::attr(value)').getall()
        for url in uik_urls:
            yield scrapy.Request(url=url, callback=self.UIKParse1)

    def UIKParse1(self, response):
        url = response.css('a::attr(href)').getall()[-1]
        yield scrapy.Request(url=url, callback=self.UIKParse2)

    def UIKParse2(self, response):
        uik = response.css('tr[bgcolor="eeeeee"] > td::text').getall()[0]
        uikn = uik.split()[-1][1:]
        results = response.css('table[bgcolor="#ffffff"] > tr > td[align="right"] > b::text').getall()

        results = [uikn, response.url] + results
        
        filename = '%s/uik-%s.dat' % (self.prefix, uikn)
        with open(filename, 'w') as f:
            f.write(",".join(results))
        self.log('Saved file %s' % filename)

