import scrapy

from scrapy.loader import ItemLoader
from ..items import DanskebankltItem
from itemloaders.processors import TakeFirst


class DanskebankltSpider(scrapy.Spider):
	name = 'danskebanklt'
	start_urls = ['https://danskebank.lt/apie-banka/naujienos/naujienos']

	def parse(self, response):
		post_links = response.xpath('//li[@class="overview-item"]/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		title = response.xpath('//h1/text()').get()
		description = response.xpath('//div[@class="row article-body"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//div[@class="meta"]/span/text()').get()

		item = ItemLoader(item=DanskebankltItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
