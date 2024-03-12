import asyncio
import os
from concurrent.futures import ThreadPoolExecutor

import pulumi
import pytest

from mocks import ImmediateExecutor


@pytest.fixture
def pulumi_set_mocks(pulumi_mocks, app_name, stack):
    loop = asyncio.get_event_loop()
    loop.set_default_executor(ImmediateExecutor())
    old_settings = pulumi.runtime.settings.SETTINGS
    try:
        pulumi.runtime.mocks.set_mocks(
            pulumi_mocks,
            project=app_name,
            stack=stack,
            preview=False)
        yield True
    finally:
        pulumi.runtime.settings.configure(old_settings)
        loop.set_default_executor(ThreadPoolExecutor())


@pytest.fixture(autouse=True)
def aws_credentials():
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = 'us-east-1'

    yield os.environ
