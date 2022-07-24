from crontab import CronTab


cron = CronTab(user='root')

job = cron.new(command='python3 manage.py refresh_table')
job.minute.every(1)
cron.write()
