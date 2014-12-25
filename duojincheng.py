#coding:utf-8

from multiprocessing import Process,Pool
import os,time,random

def long_time_task(name):
    print 'run task %s (%s)...' % (name,os.getpid())
    start = time.time()
    time.sleep(random.random() * 3)
    end = time.time()
    print 'task %s runs %0.2f seconds' % (name,(end-start))

if __name__ == '__main__':
    print 'parent process %s ' % os.getpid()
    p = Pool()
    for i in range(9):
        p.apply_async(long_time_task,args=(i,))
    print "waiting for all subpricesses done..."
    p.close()
    p.join()
    print 'All subpricesses done'


"""
def run_proc(name):
    print 'Run child process %s (%s) ... ' % (name,os.getpid())
    
if __name__ == '__main__':
    print 'parent process %s.' % os.getpid()
    p = Process(target=run_proc,args=('test',))
    p.start()
    p.join()
    print 'Process end'
    
"""