import argparse
import os
import re
import sys
from datetime import timedelta
import json
import subprocess
from pathlib import Path
import asyncio
import logging
from typing import AsyncIterable
from aiohttp import ClientConnectorError

KEY_NAME = "golem-run"


def get_yagna_executable():
    try:
        subprocess.check_call(["yagna", "--version"])
        return "yagna"
    except FileNotFoundError:
        pass

    yagna_executable = str(Path.home() / ".local" / "bin" / "yagna")
    try:
        subprocess.check_call([yagna_executable, "--version"])
        os.environ["PATH"] += f":{str(Path(yagna_executable).parent.absolute())}"
        return yagna_executable
    except:
        pass

    return None


yagna_executable = get_yagna_executable()


def get_run_key():
    global yagna_executable
    out = subprocess.check_output([yagna_executable, "app-key", "list", "--json"])
    app_keys = json.loads(out.decode())
    return next(map(lambda key: {app_keys["headers"][i]: v for i, v in enumerate(key)}, filter(lambda key: key[0] == KEY_NAME, app_keys["values"])), None)


run_key = get_run_key()
if run_key is None:
    subprocess.check_call([yagna_executable, "app-key", "create", KEY_NAME])
    run_key = get_run_key()

gvmi_list = {
    "python:3": "3522a97c07d6442e5b33cb38abf3a5e33e94d5fb7b6c621a2f9f8fb9",
    "node:latest": "1ba672c856aa12d3ee3b7612271eb663f0261352597eee6d4088de39",
}
cache_file = Path.home() / ".cache" / "golem_run_qvmi_list.json"
cache_file.parent.mkdir(exist_ok=True)
if cache_file.exists():
    with cache_file.open() as f:
        gvmi_list.update(json.load(f))

def get_image_hash(img_name):
    global yagna_executable
    if img_name in gvmi_list:
        return gvmi_list[img_name]
    build_exec = str(Path(sys.executable).parent / "gvmkit-build")
    subprocess.check_call(["docker", "build", "-t", "golem-run", "--build-arg", f"IMAGE_NAME={img_name}", str(Path(__file__).parent.absolute())])
    subprocess.check_call([build_exec, "golem-run"])
    print("Uploading image...")
    out = subprocess.check_output([build_exec, "golem-run", "--push"])
    m = re.search('hash link (.+?)\W', out.decode())
    if m:
        new_hash = m.group(1)
        print(f"Uploaded new image, hash: {new_hash}")
        gvmi_list[img_name] = new_hash
        with cache_file.open('w') as f:
            json.dump(gvmi_list, f)
        return new_hash
    else:
        raise RuntimeError("Unable to extract image hash!")


os.environ["YAGNA_APPKEY"] = run_key["key"]
from yapapi import Golem, Task, WorkContext, NoPaymentAccountError
from yapapi.log import enable_default_logger
from yapapi.payload import vm

log = logging.getLogger(__name__)


async def worker(context: WorkContext, tasks: AsyncIterable[Task]):
    async for task in tasks:
        script = context.new_script(timeout=timedelta(minutes=10))
        script.upload_file(task.data["source"], task.data["target"])
        future_result = script.run(task.data["executable"], task.data["target"], *task.data["args"])
        yield script
        task.accept_result(result=await future_result)


def prepare_tasks(args):
    tasks = []
    file_path = Path(args.file).absolute()
    tasks.append(Task(data={
        "source": str(file_path),
        "target": f"/golem/input/{file_path.name}",
        "executable": str(args.executable),
        "args": args.params,
    }))
    return tasks


async def main(args):
    package = await vm.repo(
        image_hash=get_image_hash(args.image),
    )

    tasks = prepare_tasks(args)

    try:
        async with Golem(budget=1.0, subnet_tag="devnet-beta") as golem:
            async for completed in golem.execute_tasks(worker, tasks, payload=package):
                print(completed.result.stdout)
    except NoPaymentAccountError as ex:
        log.error(f"Sender is not initialized!\nPlease run \"yagna payment init --sender\" or consult the docs\nError: {ex}")
    except (ConnectionResetError, ClientConnectorError) as ex:
        log.error(f"Yagna client is not running!\nPlease run \"yagna service run\" or consult the docs\nError: {ex}")


def __run_cli__():
    enable_default_logger(log_file="golem-run.log")
    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=Path, help="Specify script path")
    parser.add_argument("params", nargs="*", default=[], help="Specify script arguments")
    parser.add_argument("-exe", "--executable", type=Path, required=False, help="Specify path inside runtime container to script executable")
    parser.add_argument("-img", "--image", required=False, help="Specify path inside runtime container to script executable")
    args = parser.parse_args()

    if not all([args.executable, args.image]):
        if args.file.suffix == ".js":
            if args.executable is None:
                args.executable = "/usr/local/bin/node"
            if args.image is None:
                args.image = "node:16-latest"
        elif args.file.suffix == ".py":
            if args.executable is None:
                args.executable = "/usr/local/bin/python3"
            if args.image is None:
                args.image = "python:3"
        else:
            raise ValueError("Unable to determine default executable and image, please provide -exe / --executable and -img / --image flags")

    loop = asyncio.get_event_loop()
    task = loop.create_task(main(args))
    try:
        loop.run_until_complete(task)
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    __run_cli__()