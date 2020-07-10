import azure.batch._batch_service_client as batch
import azure.batch.batch_auth as batchauth
import azure.batch.models as batchmodels
import time

# Batch account credentials
BATCH_ACCOUNT_NAME = '<insert account name>'
BATCH_ACCOUNT_URL = '<insert account url>'
BATCH_ACCOUNT_KEY = '<insert account key>'

# Create a Batch service client. We'll now be interacting with the Batch
# service in addition to Storage.
credentials = batchauth.SharedKeyCredentials(BATCH_ACCOUNT_NAME,
                                             BATCH_ACCOUNT_KEY)

batch_client = batch.BatchServiceClient(
    credentials,
    batch_url=BATCH_ACCOUNT_URL)

jobSchedulesToDisable = ['jobschedule1', 'jobschedule2']
jobsToMonitor = []
jobsToRemove = []

jobSchedules = batch_client.job_schedule.list()
for jobSchedule in jobSchedules:
    if jobSchedule.id in jobSchedulesToDisable:
        # disable job schedules
        batch_client.job_schedule.disable(jobSchedule.id)
        print('disabling job schedule: ' + jobSchedule.id)
    
        jobs = batch_client.job.list_from_job_schedule(
            job_schedule_id=jobSchedule.id,
            job_list_from_job_schedule_options=batchmodels.JobListFromJobScheduleOptions(
                filter="state eq \'active\'"))

        for job in jobs:
            # disable jobs
            batch_client.job.disable(job.id, 'wait')
            jobsToMonitor.append(job.id)
            print('disabling job: ' + job.id)

while (len(jobsToMonitor) > 0):
    print('Monitoring...')
    for jobToMonitor in jobsToMonitor:
        job = batch_client.job.get(jobToMonitor)
        print('job: ' + job.id + ', state: ' + job.state)
        if job.state == batchmodels.JobState.disabled:
            # terminate disabled job
            batch_client.job.terminate(job.id)
            print('terminating: ' + job.id)
            jobsToRemove.append(jobToMonitor)

    for jobToRemove in jobsToRemove:
        jobsToMonitor.remove(jobToRemove)

    jobsToRemove.clear()

    time.sleep(10)

print('Disabled successfully')
