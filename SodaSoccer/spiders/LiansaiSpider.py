#coding=utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

#print sys.getdefaultencoding()
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.selector import Selector
from scrapy.http import Request
from SodaSoccer.items import TeamScoreItem,BisaiItem

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def printJieguo(bifen):
    a=int(bifen[0])
    b=int(bifen[2])
    if a>b:
        return '胜'
    elif a==b:
        return '平'
    else:
        return '负'
        
class SodaLiansaiSpider(BaseSpider):
    name='liansai'
    allow_domains=['http://www.sodasoccer.com']
    start_urls=['http://www.sodasoccer.com/dasai/league/133.html']
    
    def __init__(self):
    
        #用于存储比赛信息
        self.bisai_infos=[]
        #用于存储积分榜信息
        self.teams_jifenbang=[]
        self.liansai=None
        self.driver=None
        
    #解析联盟主页，获取历史记录的主页
    def parse(self,response):
        hxs=HtmlXPathSelector(response)
        history_url_list=hxs.select('//*[@class="main"]/div/div[1]/div[2]/ul/li/a/@href').extract()
        
        self.liansai=hxs.select('//*[@class="head"]/div[@class="main"]/div[@class="league_new"]/div[@class="l_left"]/div[@class="l_o"]/h1/text()').extract()[0]
        print self.liansai
        
        #打开浏览器
        self.driver=webdriver.Firefox()
        for history_url in history_url_list:
            url_head='http://www.sodasoccer.com'
            #yield Request(url_head+history_url,callback=self.parse_history)
            self.bisai(url_head+history_url)
        
        self.driver.close()
        return self.bisai_infos
   
    #获取每只球队的比赛数据
    def bisai(self,url):
        #清空上次信息
        #self.bisai_infos=[]
        
        self.driver.get(url)
        index=1
        flag=1
        while flag==1:
            try:
                elem=self.driver.find_element_by_id('rd_sel_%d' % index)
            except:
                return None
            else:
                elem.click()
                #elem.clear()
                hxs=Selector(text=self.driver.page_source)
                lines=hxs.xpath('/html/body/div/div[3]/div/div[2]/div[1]/table[2]/tbody/tr')
                if len(lines)==1:
                    return None
                for line in lines[1:]:
                    
                    item=BisaiItem()
                    shijian=line.xpath('.//td[2]/text()').extract()[0]
                    if shijian is None:
                        flag=0
                        break
                        
                    item['shijian']=shijian
                    item['riqi']=line.xpath('.//td[1]/text()').extract()[0]
                    list=line.xpath('.//td[3]/a')
                    item['bisai']=list.xpath('.//text()').extract()
                    item['bifen']=line.xpath('.//td[4]/font/text()').extract()[0]
                    item['jieguo']=printJieguo(item['bifen'])  
                    #print item
                    self.bisai_infos.append(item)
                
                index+=1
        return None
        
    #获取每只球队的积分信息        
    def jifenbang(self,hxs):
        #先清空上次信息
        self.teams_jifenbang=[]
        #获取比赛时间
        time=hxs.select('//*[@class="main"]/div[@class="league_new"]/div[@class="l_left"]/div[@class="l_o"]/h3[@class="lh3"]/text()').extract()[0]
        
        changcis=hxs.select('//*[@class="main"]/div/div[2]/div[@class="l_j"]/table')
       
        #teams_jifenbang=[]
        if changcis is None:
            return
            
        index=0
        changci_dict=dict(zip([0,1,2],['总积分','主场','客场']))
        for changci in changcis:
            teams=None
            teams=changci.select('./tr')
            for team in teams[1:]:
                team_info=TeamScoreItem()
            
                #attr=['排名','场次','胜','平','负','进球','失球','净胜率','积分']
                team_name=team.select('.//td[2]/a/text()').extract()
                team_url=team.select('.//td[2]/a/@href').extract()
                other_info=team.select('.//td/text()').extract()
                team_info['xingzhi']=changci_dict[index]
                #team_info=dict(zip(attr,other_info))
                team_info['jidu']=time
                team_info['qiudui']=team_name[0]
                team_info['zhuye']=team_url[0]
                team_info['paiming']=other_info[0]
                team_info['changci']=other_info[1]
                team_info['sheng']=other_info[2]
                team_info['ping']=other_info[3]
                team_info['fu']=other_info[4]
                team_info['jinqiu']=other_info[5]
                team_info['shiqiu']=other_info[6]
                team_info['jingshengqiu']=other_info[7]
                team_info['jifen']=other_info[8]
                team_info['liansai']=self.liansai
            
            #for k,v in team_info.iteritems():
                #print k,v
                self.teams_jifenbang.append(team_info)
                
            index+=1
            
        
    
    def parse_history(self,response):
        hxs=HtmlXPathSelector(response)
        self.jifenbang(hxs)
        return self.teams_jifenbang
        
