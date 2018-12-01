# -*- coding: utf-8 -*-
import scrapy


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['goodreads.com']
    start_urls = ['http://goodreads.com/quotes']

    def parse(self, response):
        # h1_tag=response.xpath('//h1/text()').extract_first()
        # tags=response.xpath('//*[@class="gr-hyperlink"]/text()').extract()
        #
        # yield{'H1 Tag':h1_tag,'Tags':tags}
        quotes = response.xpath('//*[@class="quoteDetails"]')
        for quote in quotes:
            text=quote.xpath('.//*[@class="quoteText"]/text()').extract_first()
            author=quote.xpath('.//*[@class="authorOrTitle"]/text()').extract_first()
            tags=quote.xpath('.//*[@class="quoteFooter"]/div/a/text()').extract()
            tag=",".join(tags[0:len(tags)-1])

            # print("\n")
            # print(text)
            # print(author)
            # print(tag)
            # print("\n")
            yield {
                'Text':text,
                'Author':author,
                'Tag':tag
            }
        next_page_url=response.xpath('//*[@class="next_page"]/@href').extract_first()
        absolute_url=response.urljoin(next_page_url)
        yield scrapy.Request(absolute_url)
