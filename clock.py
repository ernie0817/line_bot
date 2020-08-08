from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()
import urllib

@sched.scheduled_job('cron', day_of_week='mon-fri', minute='*/25')
def scheduled_job():
    url = "https://你-APP-的名字.herokuapp.com/"
    conn = urllib.request.urlopen(url)

    for key, value in conn.getheaders():
        print(key, value)


sched.start()