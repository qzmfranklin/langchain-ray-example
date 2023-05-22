#!/usr/bin/env python3

import asyncio
import pathlib
import time

from ray.job_submission import (
    JobSubmissionClient,
    JobStatus,
)

THIS_DIR = pathlib.Path(__file__).resolve().parent


async def main() -> None:
    client = JobSubmissionClient("http://127.0.0.1:8266")
    job_id = client.submit_job(
        entrypoint="python build_index_with_ray.py",
        runtime_env={
            "working_dir":
            THIS_DIR,
            "pip": ["requests==2.26.0"],
            'excludes': [
                'data/.faiss_index',
                'data/archive.tar.xz',
                str(THIS_DIR / 'data/.faiss_index'),
                str(THIS_DIR / 'data/archive.tar.xz'),
                '/home/zhongmingqu/code/Dreizack/prod/llm/langchain/ray/search_engine/data/archive.tar.xz',
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


if __name__ == '__main__':
    asyncio.run(main())
