# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

#class TutorialItem(Item):
    # define the fields for your item here like:
    # name = Field()
#    pass

class DmozItem(Item):
    placename = Field()
    #placename_abbr = Field()
    rank = Field()
    count_likes = Field()
    count_here = Field()
    detail_url = Field()
    phone = Field()
    location = Field()
