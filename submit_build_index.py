#!/usr/bin/env python3

import argparse
import asyncio
import pathlib
import time

from ray.job_submission import (
    JobSubmissionClient,
    JobStatus,
)

THIS_DIR = pathlib.Path(__file__).resolve().parent

def execute(args: argparse.Namespace):
    assert isinstance(args.address, str)

    client = JobSubmissionClient(args.address)
    job_id = client.submit_job(
        entrypoint="python build_index_with_ray.py",
        runtime_env={
            "working_dir":
            THIS_DIR,
            "pip": ["requests==2.26.0"],
            'excludes': [
                'data/.faiss_index',
                'data/archive.tar.xz',
            ],
        }
    )

    def wait_until_finish(job_id):
        start = time.time()
        timeout = 600
        while time.time() - start <= timeout:
            status = client.get_job_status(job_id)
            print(f"status: {status}")
            if status in {
                JobStatus.SUCCEEDED, JobStatus.STOPPED, JobStatus.FAILED
            }:
                break
            time.sleep(1)

    wait_until_finish(job_id)



async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--address',
        default='http://localhost:8265',
    )
    args = parser.parse_args()
    execute(args)


if __name__ == '__main__':
    asyncio.run(main())
