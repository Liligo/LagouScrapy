# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import quote, urlencode
from scrapy.http.cookies import CookieJar


class JobSpider(scrapy.Spider):
    name = 'Job'
    allowed_domains = ['www.lagou.com']
    start_urls = ['https://www.lagou.com/']
    original_job_list_url = 'https://www.lagou.com/jobs/list_{}?'

    def parse(self, response):
        # positions = response.xpath('//*[@id="sidebar"]//a/h3/text()').extract()

        cookiejar = CookieJar()
        params = {'labelWords': '', 'fromSearch': True, 'suginput': ''}
        job_url = self.original_job_list_url.format('PHP') + urlencode(params)
        yield scrapy.Request(
            url=job_url,
            callback=self.parse_position_list,
            meta={
                'cookiejar': cookiejar
            })

    #     job_list_url = [
    #         self.original_job_list_url.format(quote(position_name)) + urlencode(params) for position_name in positions
    #     ]
    #     for job_url in job_list_url:
    #         yield scrapy.Request(url=job_url, callback=self.parse_position)

    def parse_position_list(self, response):
        form_data = {'first': 'false', 'pn': '2', 'kd': 'PHP'}
        json_url = 'https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false'
        yield scrapy.FormRequest(
            url=json_url,
            method='POST',
            formdata=form_data,
            meta={'cookiejar': response.meta['cookiejar']},
            callback=self.parse_position_detail)

    def parse_position_detail(self, response):
        print(response.text)
