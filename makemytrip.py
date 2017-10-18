from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from scrapy.http import Request
import MySQLdb

class MakeMyTrip(BaseSpider):
    name = "MMT"
    start_urls = ['https://www.makemytrip.com/blog/romantic-places']
    def __init__(self, *args, **kwargs):
        self.conn = MySQLdb.connect(host="localhost", user="root", passwd='01491a0237db', db="MMTdb", charset='utf8', use_unicode=True)
        self.cur = self.conn.cursor()
    def parse(self, response):
        sel = Selector(response)
        nodes = sel.xpath('//div[@class="category_info row"]//div[@class="category_part col-sm-4 col-xs-12"]')
        for node in nodes:
            title = "".join(node.xpath('.//div[@class="tile_detail_section append_bottom12"]/p[@class="din-ab text_partinfo search_blog_title append_bottom8"]/a/text()').extract())
            image = "".join(node.xpath('.//p[@class="append_bottom15"]/a/img/@data-src').extract())
           
            link = "".join(node.xpath('.//div[@class="tile_detail_section append_bottom12"]/p[@class="din-ab text_partinfo search_blog_title append_bottom8"]/a/@href').extract())
            publ = "".join(node.xpath('.//div[@class="tile_detail_section append_bottom12"]/p[@class="din-ab text_sub_partinfo"]/text()').extract())
            publish = publ.replace('\n\n', '')
            descr = "".join(node.xpath('.//p[@class="din-regular image_sub_titleone append_bottom16"]/text()').extract())
            qry = 'insert into mmt(title, descr, image, link, publish) values (%s, %s, %s, %s, %s) on duplicate key update title = %s'
            values = (title, descr, image, link, publish, title)
            print qry%values
            self.cur.execute(qry, values)
            self.conn.commit()
      
        next_page_link = "".join(sel.xpath('//div[@class="pagination_section clearfix"]//nav[@class="text-center"]//ul[@class="pagination pagination-lg"]//li[@class="active"]//a/@href').extract())
        next_page_link = 'https://www.makemytrip.com/blog/' + next_page_link
        yield Request(next_page_link, callback=self.parse, meta={}) 
