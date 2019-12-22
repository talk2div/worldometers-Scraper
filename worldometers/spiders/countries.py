# -*- coding: utf-8 -*-
import scrapy
import logging

class CountriesSpider(scrapy.Spider):
    name = 'countries'
    allowed_domains = ['www.worldometers.info']
    start_urls = ['https://www.worldometers.info/world-population/population-by-country/']

    def parse(self, response):
        countries = response.xpath("//td/a")
        for country in countries:
            title = country.xpath(".//text()").get()
            clink = country.xpath(".//@href").get()
            
            # yield{
            #     'title':title,
            #     'country_link':clink
            # }
            # absoulete_url = f"https://www.worldometers.info{clink}"
            # absoulete_url = response.urljoin(clink)
            # yield scrapy.Request(url = absoulete_url)
            yield response.follow(url=clink, callback=self.parse_country,meta={'country_name':title})

    def parse_country(self,response):
        #logging.info(response.url)
        name = response.request.meta['country_name']
        row = response.xpath('(//table[@class="table table-striped table-bordered table-hover table-condensed table-list"])[1]/tbody/tr')
        for count in row:
            year = count.xpath('.//td[1]/text()').get()
            population = count.xpath('.//td[2]/strong/text()').get()

            yield {
                'country_name':name,
                'year':year,
                'population':population
            }
