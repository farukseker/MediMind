"""
If you ask why it wasn't added as a terminal command to Pycharm,
To answer; Because when the Django server is terminated or needs to be restarted,
the configurations running in the terminal do not adapt to this,
but if you run it as a python command in Pycharm, they work compatible.
We used this solution because we did not want to go too deep.
There may be other solutions, but the solution was quite sufficient to save time.
"""

if __name__ == '__main__':
    from runner import celery_runner
    celery_runner('uv run celery -A config.celery beat --loglevel=info')
    # celery_runner('celery -A config beat -l info')