# -*- coding: utf-8 -*-
# !/usr/bin/python
import datetime
import sqlite3
import time

from apscheduler.schedulers.blocking import BlockingScheduler


def update():
    now = datetime.datetime.now()
    print(now)
    if now.day == 15:
        conn = sqlite3.connect('../db.sqlite3')
        if conn:
            print "Opened database successfully"
            c = conn.cursor()
            cursor = c.execute("SELECT username,remaining_bytes,uuid  from app_ss_user")
            for row in cursor:
                reardSize = 800 * 1024
                new = row[1] + reardSize
                conn.execute('UPDATE app_ss_user set remaining_bytes = ' + str(new))

                conn.commit()
            conn.close()
        else:
            print "----"

        try:

            print("==奖励完毕========")

            fname=time.strftime("%Y_%m_%d", time.localtime())
            f = open(fname+".log", "a+")
            logcontent = "reward success:" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"\n"
            print(logcontent)

            f.write(logcontent)
            f.close()
        except Exception as e:
            print("-------文件写入隐藏" + e.message)

    else:
        print("今天不是奖励日")


if __name__ == '__main__':
    print "开启定时任务========"

    scheduler = BlockingScheduler()
    scheduler.add_job(update, 'interval', seconds=5)
    scheduler.start()
