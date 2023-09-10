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


def job_exists(cron: CronTab, job_name:str)->bool:
    return any(job.command == job_name for job in cron)


def question_remove_job(cron: CronTab, job_command: str):
    question = [
        inquirer.Confirm("remove", message="Do you want to remove it?"),
    ]
    answer = inquirer.prompt(question)
    answer = answer["remove"]
    if answer:
        remove_all_cron_jobs(cron, job_command)
        print("Cron job was removed.")
    else:
        print("Cron job was not removed.")


def question_add_job(cron: CronTab, job_command: str, schedule: str = '0 * * * *'):
    question = [
        inquirer.Confirm("add", message="Do you want to add this job to the cron?"),
    ]
    answer = inquirer.prompt(question)
    answer = answer["add"]
    if answer:
        add_cron_job(cron, job_command, schedule)
        print("Cron job was added.")
    else:
        print("Cron job was not added.")


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


fetch_data_job_command = f'{virtual_env_path} {cron_script_path}'

if job_exists(cron, fetch_data_job_command):
    print("\n\nThis fetch data cron job already exists.")
    question_remove_job(cron, fetch_data_job_command)
else:
    print("\n\nThis fetch data cron job does not exist.")
    print("It will run every hour @ 0mins.")
    question_add_job(cron, fetch_data_job_command)


db_backup_job_command = f'{virtual_env_path} {os.path.abspath(script_root + "/cron/db_backup.py")}'

if job_exists(cron, db_backup_job_command):
    print(f'\n\nDatabase backup cron job was detected.')
    question_remove_job(cron, db_backup_job_command)
else:
    print("\n\nDatabase backup cron job was not detected.")
    print(f'The cron job will run every hour @ 5mins and will keep last {os.getenv("DB_MAX_BACKUPS")} backups.')
    question_add_job(cron, db_backup_job_command, schedule='5 * * * *')
