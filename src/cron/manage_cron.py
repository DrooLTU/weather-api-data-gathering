import os
import sys
from dotenv import load_dotenv
from crontab import CronTab
load_dotenv()
cron = CronTab(user=os.getenv("CRON_USER"))

def print_cron_jobs(cron: CronTab) -> None:
    for job in cron:
        print(f"Command: {job.command}")
        print(f"Schedule: {job.slices}")
        print(f"User: {cron.user}")
        print("---")

print("Current cron jobs:")
print_cron_jobs(cron)


script_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(script_root)


# PATHS TO THE VIRTUAL ENVIRONMENT AND THE SCRIPT TO BE RUN
virtual_env_path = os.path.abspath((os.path.dirname(script_root) + '/venv/bin/python'))
cron_script_path = os.path.abspath(script_root + '/fetch/fetch_coroutine.py')


# Specify the command of the cron job you want to check
job_command_to_check = f'{virtual_env_path} {cron_script_path}'

# Iterate through the existing cron jobs and check if the command matches
job_exists = any(job.command == job_command_to_check for job in cron)


def add_cron_job(cron: CronTab, command: str, schedule: str) -> None:
    job = cron.new(command=command)
    job.setall(schedule)
    cron.write()
    print("Cron job successfully created!")
    print("Updated cron jobs:")
    print_cron_jobs(cron)


def remove_cron_job(cron: CronTab, command: str) -> None:
    cron.remove_all(command=command)
    cron.write()
    print("Cron job successfully removed!")
    print("Updated cron jobs:")
    print_cron_jobs(cron)


if job_exists:
    print("The cron job already exists.")
else:
    print("The cron job does not exist.")
    add_cron_job(cron, job_command_to_check, '0 * * * *')
