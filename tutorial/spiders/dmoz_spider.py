from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.http import Request
import time
import random

from tutorial.items import DmozItem

class DmozSpider(Spider):
    name = "dmoz"
    allowed_domains = ["socialbakers.com"]
    start_urls = [
        "http://www.socialbakers.com/places/country/taiwan/page-1/",
        "http://www.socialbakers.com/places/country/taiwan/page-2/",
        "http://www.socialbakers.com/places/country/taiwan/page-3/",
    ]

    def parse(self, response):
        time.sleep(random.random() * 10)
        #filename = response.url.split("/")[-2]
        #open(filename, 'wb').write(response.body)

        #sel = Selector(response)
        #section = sel.xpath('//section[@id="fb-block"]/div[@class="button-facebook"]/div/@data-href').extract()[0]
        #print "fb-url = ", section
        #section = "http://www.socialbakers.com" + section
        return Request(response.url, callback=self.after_login,
            cookies={'current_user': 'uid-bb2294b3-3100-ba76-6e5f-5efc0042817e',
            'fbm_111353382239227': 'base_domain=.socialbakers.com',
            'fbsr_111353382239227': 'b9Spy687KDSUQcO7qDTLH_XVqi1ogOWMG0IipzKNSzI.eyJhbGdvcml0aG0iOiJITUFDLVNIQTI1NiIsImNvZGUiOiJBUUJ3QWxRNWNtZ1FTaGlNT3p2NS1xTDFUMkpSeHFfQjdvcFhxMWRtM19iUVBXVU9UMmhsUFpjUFRxNFdaQkRyM0cteXo1VU1CbjB4bklHTXhDS0JHREpXdGNncEtIWTFTWmpBbGhMLVNjS2txUW9KRnNydWROZVlwRXc5c0VRRllwLU5aQ21LR1F1NHk5UHhfSDZZSnFuZkQzOHEtMmgzblh5NGEzaFMydUhJUEtja2FTcGJmeF9ZcnpLb0ZzWnFmSi1aOVlZSGNzTjZsLXlxSHU4RHJ6RjRXSWV0cGdXOGw4OHBGazl3ZUVmSXJKd1hzQ1RIQUxCR2tYWnI1NTd3a1dobGZfTmhDeWdmWnNyNFB2dHV3cGNWTnJvbU9SdncwUzJBcS1udWVTNHhNYzNOY3E1UEVYb2tIZUVJdzRmbUNYTSIsImlzc3VlZF9hdCI6MTQwMzE0NjgzOCwidXNlcl9pZCI6IjE4MTM3NTg3MTkifQ',
            'nette-browser': 'umyhz726zs',
            'primary_user': 'acl-217152',
            'sbks:sso': '6475d053-8c66-403a-b593-33c93e89e9f1',
            'sbkswww': 'bb4cq0ngl7e08mvvbsgj502k25',
            'userhash': 'bb2294b3-3100-ba76-6e5f-5efc0042817e',
            'wp3396': 'WWCZDDDDDDSSX-THLZXIDSSX-TMXZMHDlhJpHsIHrLkl_Jht'})



    def after_login(self, response):
        #filename = response.url.split("/")[-2] + "_after"
        #open(filename, 'wb').write(response.body)
        items = []
        sel = Selector(response)
        section = sel.xpath('//table[@class="common-table"]/tbody/tr')
        for sub_tr in section:
            item = DmozItem()
            placename = sub_tr.xpath('td[@class="name"]/a')
            item['placename'] = placename.xpath('text()').extract()[0].replace("\n", "").replace("\t", "")
            if (item['placename'] == "") : item['placename'] = placename.xpath('//abbr/@title').extract()[0].replace("\n", "").replace("\t", "")
            item['rank'] = sub_tr.xpath('td[@class="rank"]/span[@class="rank"]/text()').extract()[0].replace("\n", "").replace("\t", "")[:-1]
            #item['count_likes'] = sub_tr.xpath('td[@class="count"]/text()').extract()
            #item['count_here'] = sub_tr.xpath('td[@class="count"]/text()').extract()[1].replace("\n", "").replace("\t", "")

            item['detail_url'] = placename.xpath('@href').extract()[0]
            yield Request(item['detail_url'], callback=self.detail_parse,
                cookies={'current_user': 'uid-bb2294b3-3100-ba76-6e5f-5efc0042817e',
                'fbm_111353382239227': 'base_domain=.socialbakers.com',
                'fbsr_111353382239227': 'b9Spy687KDSUQcO7qDTLH_XVqi1ogOWMG0IipzKNSzI.eyJhbGdvcml0aG0iOiJITUFDLVNIQTI1NiIsImNvZGUiOiJBUUJ3QWxRNWNtZ1FTaGlNT3p2NS1xTDFUMkpSeHFfQjdvcFhxMWRtM19iUVBXVU9UMmhsUFpjUFRxNFdaQkRyM0cteXo1VU1CbjB4bklHTXhDS0JHREpXdGNncEtIWTFTWmpBbGhMLVNjS2txUW9KRnNydWROZVlwRXc5c0VRRllwLU5aQ21LR1F1NHk5UHhfSDZZSnFuZkQzOHEtMmgzblh5NGEzaFMydUhJUEtja2FTcGJmeF9ZcnpLb0ZzWnFmSi1aOVlZSGNzTjZsLXlxSHU4RHJ6RjRXSWV0cGdXOGw4OHBGazl3ZUVmSXJKd1hzQ1RIQUxCR2tYWnI1NTd3a1dobGZfTmhDeWdmWnNyNFB2dHV3cGNWTnJvbU9SdncwUzJBcS1udWVTNHhNYzNOY3E1UEVYb2tIZUVJdzRmbUNYTSIsImlzc3VlZF9hdCI6MTQwMzE0NjgzOCwidXNlcl9pZCI6IjE4MTM3NTg3MTkifQ',
                'nette-browser': 'umyhz726zs',
                'primary_user': 'acl-217152',
                'sbks:sso': '6475d053-8c66-403a-b593-33c93e89e9f1',
                'sbkswww': 'bb4cq0ngl7e08mvvbsgj502k25',
                'userhash': 'bb2294b3-3100-ba76-6e5f-5efc0042817e',
                'wp3396': 'WWCZDDDDDDSSX-THLZXIDSSX-TMXZMHDlhJpHsIHrLkl_Jht'},
                meta={'item': item})
            #break

            items.append(item)
        #return items

    def detail_parse(self, response):
        time.sleep(random.random() * 5)
        #filename = response.url.split("/")[-1] + "_detail"
        #open(filename, 'wb').write(response.body)
        item = response.request.meta['item']
        sel = Selector(response)
        detail = sel.xpath('//section[@class="profile-detail facebook-place"]/ul[@class="stats"]')
        item['count_likes'] = "".join(detail.xpath('li')[0].xpath('strong/text()').extract())
        item['count_here'] = "".join(detail.xpath('li')[1].xpath('strong/text()').extract())
        phones = detail.xpath('li').re(r'Phone: ([^<]*)')
        if (len(phones) > 0) : item['phone'] = phones[0]
        location = sel.xpath('//div[@class="places-map"]/script[@type="text/javascript"]')
        item['location'] = location.xpath('text()').re(r'LatLng\(([0-9\.]+, [0-9\.]+)\)')[0]
        return item


