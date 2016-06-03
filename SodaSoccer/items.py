# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item
from scrapy.item import Field

class TeamScoreItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
	qiudui=Field()
	jidu=Field()
	paiming=Field()
	zhuye=Field()
	changci=Field()
	sheng=Field()
	ping=Field()
	fu=Field()
	jinqiu=Field()
	shiqiu=Field()
	jingshengqiu=Field()
	jifen=Field()
	liansai=Field()
	xingzhi=Field()
	
class BisaiItem(Item):
    riqi=Field()
    shijian=Field()
    bisai=Field()
    bifen=Field()
    jieguo=Field()
