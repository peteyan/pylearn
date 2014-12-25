#coding:utf-8
import MySQLdb
import threading
from Queue import Queue
import time
import urllib2
import random
import os
#import logging  

"""
多线程下载MP3
"""

limit = 17
queue = Queue()
lock = threading.RLock() # 查询锁


class DownloadMusic(threading.Thread):
    def __init__(self, t_name, queue):  
        threading.Thread.__init__(self, name=t_name)
        self.queue = queue
        self.conn = MySQLdb.connect(host="localhost",
                                    user="root",
                                    passwd="",
                                    db="www0402",charset="gbk")
        self.cursor = self.conn.cursor()
        
    def _getLimit(self):
        global limit,lock
        with lock:
            limit += 1
            return (limit-1) * 100
            
    #数据库查询出要下载的MP3 url
    def getRows(self):
        lm = self._getLimit()
        print "________________%s________________" % lm
        sql = "SELECT * from fanwe_music where is_download=0 limit %s, 100 " % lm
        self.cursor.execute(sql)
        return self.cursor.fetchall()
        
    # 获取MP3 文件流
    def get_content_by_proxy(self,url):
        #opener = urllib2.build_opener(urllib2.ProxyHandler({'http':'117.162.44.200:8123'}), urllib2.HTTPHandler(debuglevel=1)) #222.59.244.14:8118
        #urllib2.install_opener(opener)
        try:
            req = urllib2.Request(url, headers=getHeader())
            content =  urllib2.urlopen(req).read()
        except urllib2.HTTPError, e:
            #log(u'%s |%s' % (e,url),'httperror.log')
            content = False
        except urllib2.URLError,e:
            content = False
            #log(u'%s |%s' % (e,url),'urlerror.log')
        except:
            return False
        return content
    
    def download(self,queueRow):
        url = queueRow['mp3']
        urlpath = url.split('/')
        try:
            makeMusicFilePath('music/%s' % urlpath[-2])
            filepath = 'music/%s/%s' % (urlpath[-2],urlpath[-1])
        except:
            filepath = '%s_%s' % (urlpath[-2],urlpath[-1])
        if os.path.isfile(filepath):
            print u"%s 已经存在 " % filepath
            #log(u"%s 已经存在 " % filepath,'exist.log')
        else:
            content = self.get_content_by_proxy(url)
            if content:
                with open(filepath,'wb') as code:
                    code.write(content)
            else:
                self.queue.put(queueRow)
            time.sleep(5)
            
    def run(self):
        while True:
            if self.queue.qsize() < 100:
                data = self.getRows()
                for row in data:
                    self.queue.put({'mp3':row[6],'id':row[0],'thread':self.name})
                    print u"%s : ### %s ### $$$ %s $$$ 添加队列：%s" % (self.name,self.queue.qsize(),row[0],row[6])
                    #time.sleep(2)
            queueRow = self.queue.get()
            print u"%s : ### %s ###  $$$ %s $$$ 下载中 %s " % (self.name,self.queue.qsize(),queueRow['id'],queueRow['mp3'])
            self.download(queueRow)

#请求头部信息
def getHeader():
    user_agent = [
		"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
	]
    return {'Accept':	'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Encoding':	'gzip, deflate',
        'Accept-Language':	'zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3',
        'Connection':	'keep-alive',
        'Host'	:'m2.music.126.net',
        'Referer':	'http://music.163.com/style/swf/CloudMusicPlayer.swf?v=2014060988888',
        'User-Agent':	random.choice(user_agent),
        'x-insight'	:'activate'}

def makeMusicFilePath(folderName):
    #print "make dir %s" % folderName
    if not os.path.isdir(folderName):
        os.makedirs(folderName)
            
if __name__ == '__main__':
    for i in range(10):
        down = DownloadMusic('down%s%s%s%s%s' % (i,i,i,i,i),queue)
        down.setDaemon(True)
        down.start()
    down.join()  