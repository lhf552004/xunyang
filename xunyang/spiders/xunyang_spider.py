import scrapy
from .houseItem import HouseItem
import io
import time


class xunyang(scrapy.Spider):  # 需要继承scrapy.Spider类

    temp = HouseItem()
    buildTime = ''
    houseType = ''
    name = "xunyang"  # 定义蜘蛛名
    start_urls = [
        'http://localhost/list.html',
        # 'https://jiujiang.anjuke.com/community/yangqu/p1/',
        # 'https://jiujiang.anjuke.com/community/yangqu/p2/',
        # 'https://jiujiang.anjuke.com/community/yangqu/p3/'
    ]

    # def start_requests(self):  # 由此方法通过下面链接爬取页面
    #
    #     # 定义爬取的链接
    #     urls = [
    #         'http://lab.scrapyd.cn/page/1/',
    #         'http://lab.scrapyd.cn/page/2/',
    #     ]
    #     for url in urls:
    #         yield scrapy.Request(url=url, callback=self.parse)  # 爬取到的页面如何处理？提交给parse方法处理

    def parse(self, response):
        global buildTime
        global houseType
        buildTime = ''
        houseType = ''
        self.log('url response parse begin.')
        xiaoqu = response.css('div.li-itemmod')
        filename = 'res.json'
        with io.open(filename, 'w+', encoding='utf-8') as f:
            str = '浔阳区小区\n'
            f.write(str)

        for x in xiaoqu:
            item = HouseItem()
            li_info = x.css('.li-info')[0]
            item['text'] = li_info.css('a::text').extract_first()
            self.log('name: %s' % item['text'])
            item['addr'] = li_info.css('address::text').extract_first().splitlines()[1].strip()
            url = li_info.css('p.bot-tag a::attr(href)').extract_first()
            self.log('二手房链接: %s' % url)
            yield scrapy.Request(url, callback=self.xiaoqu)

            with io.open(filename, 'a+', encoding='utf-8') as f:
                str = '小区名称: {name}, 地址：{addr}, 建筑年代：{buildTime}, 房屋类型: {houseType}\n'.format(name=item['text'], addr=item['addr'], buildTime=buildTime, houseType=houseType)
                f.write(str)
            self.log('保存文件: %s' % filename)
            # time.sleep(10000)


    def xiaoqu(self, response):
        global buildTime
        global houseType
        fangzi_url = response.css('li.m-rent-house a::attr(href)').extract_first()
        self.log('第一个房子链接: %s' % fangzi_url)
        yield scrapy.Request(fangzi_url, callback=self.house)


    def house(self, response):
        buildTime = response.css('div.houseInfo-detail dl dd::text').extract()[5].splitlines()[1]
        houseType = response.css('div.houseInfo-detail dl dd::text').extract()[6]
        self.log('bulid Time: %s' % buildTime)
        self.log('houseType: %s' % houseType)