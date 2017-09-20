# -*- coding: utf-8 -*-
import scrapy


class CoinscheduleSpider(scrapy.Spider):
    name = 'coinschedule'
    allowed_domains = ['coinschedule.com']
    start_urls = ['http://coinschedule.com/index.php?live_view=2']

    def parse(self, response):
        print '*'*50
        # There are going to be 3 <tbody/> elements
        # The first one is the Live Token Sales
        # The second one is the header for the Upcoming Sales
        # The third one is hte Upcoming Token Sales
        # ...go figure
        table_bodies = response.css('section div.container div table.table tbody')

        if len(table_bodies) != 3:
            print('Something is weird, update conditions')
            return
                
        live_token_sales = table_bodies[0]
        

        for tr in live_token_sales.css('tr'):
            name = tr.css('td:first-of-type a::text').extract_first()
            href = tr.css('td:first-of-type a::attr(href)').extract_first()

            request = response.follow(href, self.parse_details_page)
            request.meta['name'] = name
            request.meta['href'] = href
            request.meta['kind'] = 'live'
            yield request


        upcoming_token_sales = table_bodies[2]
        for tr in upcoming_token_sales:
            name = tr.css('td:first-of-type a::text').extract_first()
            href = tr.css('td:first-of-type a::attr(href)').extract_first()

            request = response.follow(href, self.parse_details_page)
            request.meta['name'] = name
            request.meta['href'] = href
            request.meta['kind'] = 'upcoming'
            yield request


    def parse_details_page(self, response):

        obj = {}

        name = response.meta.get('name', None)
        href = response.meta.get('href', None)
        kind = response.meta.get('kind', None)

        obj['name'] = name
        obj['href'] = href
        obj['kind'] = kind

        description = response.css('div.page-container > #page-top > div.container div.text-center.well::text').extract_first()
        obj['description'] = description
        
        details_table = response.css('div.page-container > #page-top > div.container > table')
        for tr in details_table.css('tbody > tr'):
            th = tr.css('th::text').extract_first()
            val = ''

            if th == 'Project Type':
                val = tr.css('td::text').extract_first()
                val = val.rstrip() if val is not None else ''
            elif th == 'Platform':
                val = tr.css('td::text').extract_first()
                val = val.rstrip() if val is not None else ''
            elif th == 'Website':
                val = tr.css('td a::attr(href)').extract_first()
                val = val.rstrip() if val is not None else ''
            elif th == 'Category':
                val = tr.css('td::text').extract_first()
                val = val.rstrip() if val is not None else ''
            elif th == 'Total Supply':
                val = tr.css('td::text').extract_first()
                val = val.rstrip() if val is not None else ''
            elif th == 'Location':
                val = tr.css('td::text').extract_first()
                val = val.rstrip() if val is not None else ''
            elif th == 'Whitepaper':
                val = tr.css('td a::attr(href)').extract_first()
                val = val.rstrip() if val is not None else ''
            elif th == 'Bitcoin Talk':
                val = tr.css('td a::attr(href)').extract_first()
                val = val.rstrip() if val is not None else ''
            else:
                pass

            key = th.lower().replace(' ', '_')

            if name and href and kind:
                obj[key] = val
                yield obj