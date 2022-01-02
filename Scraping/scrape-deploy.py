'''
script for deploying containers on aws
'''
import boto3

client = boto3.client('ecs','us-east-1')
r = client.run_task(
        taskDefinition='s3ecs',
        launchType='FARGATE',
        cluster='scrape-cluster',
        platformVersion='LATEST',
)

def _deploy(start_slug,i: int):
    """starts a scrape task on ecs

    Args:
        start_slug (str): slug to start the crawl from
        i (int): id of process
    """
    client = boto3.client('ecs')
    
    r = client.run_task(
        taskDefinition='s3ecs',
        launchType='FARGATE',
        cluster='scape-cluster',
        platformVersion='LATEST',
        count=1,
        networkConfiguration={
            'awsvpcConfiguration': {
                'subnets': [
                    'subnet-9e7c0fc1',
                ],
                'assignPublicIp': 'ENABLED',
                'securityGroups': ["sg-0bfa5becbde957cd3"]
            }
        }
        )


def wait():
    pass
def write():
    pass
def GetSlug():
    pass
def Deploy(num_workers):
    for i in range(num_workers):
        slug = GetSlug()
        _deploy(slug)
        pass
    wait()

    write()
    
    