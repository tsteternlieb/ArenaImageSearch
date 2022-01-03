"""
script for deploying containers on aws
"""
import boto3
import os
from dotenv import load_dotenv

load_dotenv()
# env variables
SECURITYGROUP = os.getenv("SECURITYGROUP")


# client = boto3.client("ecs", "us-east-1")
# r = client.run_task(
#     taskDefinition="s3ecs",
#     launchType="FARGATE",
#     cluster="scrape-cluster",
#     platformVersion="LATEST",
# )


def _deploy(
    name: str,
    start_slug: str,
    depth: int,
    dic: bool,
    num_threads: str,
    container_name: str,
    task_def: str,
):
    """runs specified task on ecs

    Args:
        name (str): name for the task save locations
        start_slug (str): slug to start crawl at
        depth (int): depth of bfs to go before completing
        dic (bool): whether or not to create adjacency dictionary
        num_threads (str): num of threads, yay multi threading
        container_name (str): name for the container which we override
        task_def (str): task name
    """

    client = boto3.client("ecs")

    r = client.run_task(
        taskDefinition=task_def,
        launchType="FARGATE",
        cluster="scape-cluster",
        platformVersion="LATEST",
        count=1,
        networkConfiguration={
            "awsvpcConfiguration": {
                "subnets": [
                    "subnet-9e7c0fc1",
                ],
                "assignPublicIp": "ENABLED",
                "securityGroups": SECURITYGROUP,
            }
        },
        overrides={
            "containerOverrides": [
                {
                    "name": container_name,
                    "command": [
                        "--slug",
                        start_slug,
                        "--num_threads",
                        num_threads,
                        "--depth",
                        str(depth),
                        "--dic",
                        dic,
                    ],
                }
            ]
        },
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


print(type(SECURITYGROUP), SECURITYGROUP)
