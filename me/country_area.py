# -*- coding:utf-8 -*-

import MySQLdb
#import os
#import sys
#ROOT_PATH = os.getcwd()
"""
统计area的数据
"""
#os.path.dirname(os.path.abspath(__file__))
#os.path.join(ROOT_PATH,'ci.txt')


class EmptyPidError(Exception):
    def __init__(self,value):
        self.value = value
    def __str__(self,value):
        return self.value
    

class peici:
    
    pid = 0
    cate_id = 0
    peici = []
    
    def __init__(self):
        self.conn = MySQLdb.connect(host='localhost',user='root',passwd='',db='www0402',charset='utf8')
        self.cursor = self.conn.cursor()
    
    def process_peici(self,filename):
        self._readline(filename)
        
    def _addCate(self,linetxt):
        ''' 添加分类 '''
        self.cate_id = 0
        data = linetxt.replace('#','').strip()
        self.cursor.execute("INSERT INTO fanwe_words_cate (`pid`,`catename`)values(0,'%s')" % data)
        self.pid = self.conn.insert_id()
        self.conn.commit()
    
    def _addChildCate(self,linetxt):
        ''' 添加子分类 '''
        if not self.pid or type(self.pid) not  in (int,long):
           raise EmptyPidError(u"分类pid 不能为空！请查看文本结构")
        data = linetxt.replace('=','').strip()
        self.cursor.execute("INSERT INTO fanwe_words_cate (`pid`,catename)values(%s,'%s')" % (self.pid,data))
        self.cate_id = self.conn.insert_id()
        self.conn.commit()
        
    def showError(self): #测试自定义错误
        self.pid = 'dsf'
        self._addChildCate('dfafa')
    
    def _insertPeici(self):
        #print self.peici
        sql = "INSERT INTO fanwe_words (`pid`,`content`)values(%s,%s)"
        self.cursor.executemany(sql,self.peici)
        self.conn.commit()
        
        
    def _addPeici(self,linetxt):
        ''' 组装配词 '''
        
        if self.cate_id and type(self.cate_id) in (int,long):
            peiciPid = self.cate_id
        elif self.pid and type(self.pid) in (int,long):
            peiciPid = self.pid
        else:
            raise EmptyPidError(u"pid 不能为空！请查看文本结构")
        
        data = linetxt.strip()
        self.peici.append((peiciPid,data))
        #self.cursor.execute("INSERT INTO fanwe_words (`pid`,`content`)values(%s,%s)" % (peiciPid,data))
        #self.conn.commit()
    
    def _readline(self,filename):
        f = open(filename,'r')
        lines = f.readlines()
        f.close()
        for linetxt in lines:
            linetxt = linetxt.strip('\n\t').decode('utf-8')
            if not linetxt:
                continue
            if '#####' in linetxt:
                self._addCate(linetxt)
            elif '=====' in linetxt:
                self._addChildCate(linetxt)
            else:
                self._addPeici(linetxt)
        self._insertPeici()
        
        
    def __del__(self):
        self.cursor.close()
        self.conn.close()
            
"""
替代execute 批量插入
c.executemany(
      "INSERT INTO breakfast (name, spam, eggs, sausage, price)
      VALUES (%s, %s, %s, %s, %s)",
      [
      ("Spam and Sausage Lover's Plate", 5, 1, 8, 7.95 ),
      ("Not So Much Spam Plate", 3, 2, 0, 3.95 ),
      ("Don't Wany ANY SPAM! Plate", 0, 4, 3, 5.95 )
      ] )
"""
        
        
if __name__ == '__main__':
    
    peici().process_peici(sys.argv[1])
    
    
    
    
    
    
    
    
    