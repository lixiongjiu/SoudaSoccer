# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import mysql.connector


class DBError(Exception):
    pass
    
    
class SodasoccerPipeline(object):

    def __init__(self):
        try:
            self.conn=mysql.connector.connect(user='root',password='123',database='soda_data',use_unicode=True)
            self.cursor=None
        
        except:
            print '数据库打开失败...'
        else:
            print '数据库打开成功...' 

    
             
    def process_item(self, item, spider):
        #print '进入数据保存阶段...'
        #print item
        '''
        try:
            self.cursor=self.conn.cursor()
            
            #self.cursor.execute('insert into europe_jifenbang (qiudui,jidu,paiming,changci,sheng,ping,fu,jinqiu,shiqiu,jingshengqiu,jifen,liansai,xingzhi) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',[item['qiudui'],item['jidu'],item['paiming'],item['changci'],item['sheng'],item['ping'],item['fu'],item['jinqiu'],item['shiqiu'],item['jingshengqiu'],item['jifen'],item['liansai'],item['xingzhi']])
            if item['jidu']=='2014/15':
                self.cursor.execute('insert into qiudui (jiancheng,zhuye) values(%s,%s)',(item['qiudui'],item['zhuye']))
            
        except Exception,e:
            self.conn.rollback()
            self.cursor=None
            print e
            print '插入失败，已回滚...'
        else:
            self.conn.commit()
            self.cursor.close()
            print '数据插入成功，已提交...'
        '''
        print item['riqi']
        print item['shijian']
        print item['bisai']
        print item['bifen']
        print item['jieguo']
        return item
        
       
    def __del__(self):
    
        print '数据库已被关闭，相关属性已被清空...'
        self.cursor.close()
        self.conn.close()
        self.cursor=self.conn=None
        
        
