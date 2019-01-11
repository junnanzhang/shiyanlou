import scrapy

class ShiyanlouGitSpider(scrapy.Spider):
	name = 'shiyanlou-git'

	def start_requests(self):
		url_tmpl = 'https://github.com/shiyanlou?tab=repositories'
		yield scrapy.Request(url=url_tmpl, callback=self.parse)

	def parse(self, response):
		for item in response.css('div#user-repositories-list ul li'):
			yield {
				'name': item.css('div.mb-1.d-inline-block h3 a::text').extract_first().strip(),
				'update_time': item.css('div.f6 relative-time::attr(datetime)').extract_first()
			}
		next_link = response.css('div.pagination a::attr(href)').extract_first()
		if next_link:
			yield scrapy.Request(url=next_link, callback=self.parse)