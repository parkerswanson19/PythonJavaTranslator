from RapAnalyzer.RapCaviar import pull_from_spotify_playlist
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()

scheduler.start()

job = scheduler.add_job(pull_from_spotify_playlist, 'cron', hour=17, minute=49, id='spotify_grabber')

# job.remove()

