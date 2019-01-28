# -*- coding: utf-8 -*-
import scrapy


class SpiderSpider(scrapy.Spider):
    name = 'spider'
    allowed_domains = ['naturalia.fr']
    start_urls = [
        'https://naturalia.fr/epicerie-salee?p=1',
        'https://naturalia.fr/epicerie-sucree?p=1',
        'https://naturalia.fr/produits-frais?p=1',
        'https://naturalia.fr/fruits-et-legumes?p=1',
        'https://naturalia.fr/boissons?p=1',
        'https://naturalia.fr/cave-et-boissons-alcoolisees?p=1',
        'https://naturalia.fr/bebe?p=1',
        'https://naturalia.fr/complements-alimentaire?p=1',
        'https://naturalia.fr/hygiene-beaute?p=1',
        'https://naturalia.fr/aromatherapie?p=1',
        'https://naturalia.fr/maison?p=1',
        'https://naturalia.fr/nouveautes?p=1',
        'https://naturalia.fr/promotions?p=1',
        'https://naturalia.fr/vegan?p=1',
        'https://naturalia.fr/biodynamie?p=1',
        'https://naturalia.fr/regime-particulier?p=1',
        'https://naturalia.fr/enfant?p=1'
    ]

    def parse(self, response):
        urls = response.xpath('//a[@class="product-item-link"]/@href').extract()
        for url in urls:
            yield scrapy.Request(url, callback=self.individual_page)

        # Calling next page
        for page in range(2, 10):
            next_page_url = str(response.url.split('=')[0]) + "=" + str(page)
            yield scrapy.Request(url=next_page_url)

    def individual_page(self, response):
        fields = dict()
        fields["base_price"] = response.xpath('//span[@class="price-wrapper "]/@data-price-amount').extract_first()
        fields["discounted_price"] = response.xpath('//span[@class="price-wrapper "]/@data-price-amount').extract_first()
        fields["product_name"] = response.xpath('//h1[@class="page-title"]/span/text()').extract_first()
        fields["category"] = response.xpath('//div[@class="breadcrumbs"]/ul[@class="items"]/li/a/text()').extract()[1].strip()
        fields["brand"] = response.xpath('//div[@class="product-info-main-top-wrapper"]/p[@class="product-attribute brand"]/text()').extract_first()
        fields["description"] = response.xpath('//div[@class="product attribute description"]/div[@class="value"]//text()').extract_first()

        yield fields