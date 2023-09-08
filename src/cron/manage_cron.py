import os
import sys
from dotenv import load_dotenv
from crontab import CronTab
import inquirer
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


question = [
        inquirer.List(
            "method",
            message="Select which parallelism you want to use",
            choices=["coroutine", "threads", "processes"],
        ),
    ]
answer = inquirer.prompt(question)
answer = answer["method"]


virtual_env_path = os.path.abspath((os.path.dirname(script_root) + '/venv/bin/python'))
cron_script_path = os.path.abspath(script_root + '/fetch/fetch_coroutine.py')
if answer == "threads":
    cron_script_path = os.path.abspath(script_root + '/fetch/fetch_parallel.py')
elif answer == "processes":
    cron_script_path = os.path.abspath(script_root + '/fetch/fetch_parallel.py -p')

print(f'Chosen: {answer}')


job_command_to_check = f'{virtual_env_path} {cron_script_path}'
job_exists = any(job.command == job_command_to_check for job in cron)


def add_cron_job(cron: CronTab, command: str, schedule: str) -> None:
    job = cron.new(command=command)
    job.setall(schedule)
    cron.write()
    print("Cron job successfully created!")
    print("Updated cron jobs:")
    print_cron_jobs(cron)


def remove_all_cron_jobs(cron: CronTab, command: str) -> None:
    cron.remove_all(command=command)
    cron.write()
    print("Cron job successfully removed!")
    print("Updated cron jobs:")
    print_cron_jobs(cron)


if job_exists:
    print("The cron job already exists.")
    q_clear_old_jobs = input("Do you want to remove the cron jobs? (y/n): ")
    if(q_clear_old_jobs == 'y'):
        remove_all_cron_jobs(cron, job_command_to_check)
        print("Run the script again to add the cron job.")
    else:
        print("No changes made to the cron jobs. This script does not allow creating duplicate cron jobs.")
else:
    print("The cron job does not exist.")
    print("The cron job will run every hour.")
    q_add_new_job = input("Do you want to add the cron job? (y/n): ")
    if(q_add_new_job == 'y'):
        add_cron_job(cron, job_command_to_check, '0 * * * *')
        print("Run the script again to remove the cron job.")
    else:
        print("No changes made to the cron jobs.")