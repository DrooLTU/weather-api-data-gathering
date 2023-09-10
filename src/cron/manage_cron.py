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


if job_exists(cron, job_command_to_check):
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


db_backup_job_command = f'{virtual_env_path} {os.path.abspath(script_root + "/cron/db_backup.py")}'
if job_exists(cron, db_backup_job_command):
    print(f'Database backup cron job was detected. Do you want to remove it?')
    question = [
        inquirer.Confirm("remove", message="Database backup cron job was detected. Do you want to remove it?"),
    ]
    answer = inquirer.prompt(question)
    answer = answer["remove"]
    if answer:
        remove_all_cron_jobs(cron, db_backup_job_command)
        print("Database backup cron job was removed.")
    else:
        print("Database backup cron job was not removed.")
else:
    print("Database backup cron job was not detected.")
    print(f'The cron job will run every hour and will keep last {os.getenv("DB_MAX_BACKUPS")} backups.')
    question = [
        inquirer.Confirm("add", message="Do you want to add this job to the cron?"),
    ]
    answer = inquirer.prompt(question)
    answer = answer["add"]
    if answer:
        add_cron_job(cron, db_backup_job_command)
        print("Database backup cron job was added.")
    else:
        print("Database backup cron job was not added.")
