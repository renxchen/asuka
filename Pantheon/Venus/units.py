import os
import sys
import time
import json
from configurations import Configurations


def save_file(folder, filename, content):
    with open(os.path.join(folder, filename)) as f:
        f.read(content)


def create_directory(path):
    if os.path.exists(path) is False:
        os.mkdir(path)
    return path


# /home/apolo/data/task_min5/cli
def save_output_file(params):
    config = Configurations()
    # directory = config.get_configuration('baseDirectory')
    filename_format = config.get_configuration('baseFilenameFormat')
    task_start_time = params['task_start_time']
    # task_start_time = str(time.mktime(time.strptime(task_start_time, "%Y-%m-%d %H:%M:%S"))) #test task
    directory = params['baseDirectory']
    index = params['index']
    status = params['status']
    start_time = params['start_time']
    # hostname = params['hostname']
    ip = params['ip']
    task_id = params['task_id']
    if status == "success":
        output = params['output']
        # dir_str = "C:\\Users\\haonchen\\Desktop\\ppmOutput\\1511227248"
        dir_str = create_directory(os.path.join(directory, task_start_time))
        start_timestamp = str(time.mktime(time.strptime(start_time, "%Y-%m-%d %H:%M:%S")))
        filename = "%s_%s_%s" % (ip, start_timestamp, index)
        with open(os.path.join(dir_str, filename), 'w') as f:
            for each in output:
                f.write(each['output'])
    else:
        output = params['output']
        # dir_str = "C:\\Users\\haonchen\\Desktop\\ppmOutput\\1511227248"
        dir_str = create_directory(os.path.join(directory, task_start_time))
        start_timestamp = str(time.mktime(time.strptime(start_time, "%Y-%m-%d %H:%M:%S")))
        filename = "%s_%s_%s" % (ip, start_timestamp, index)
        with open(os.path.join(dir_str, filename), 'w') as f:
            for each in output:
                f.write(json.dumps(each))


# /home/apolo/data/task_min5/cli
def save_snmp(params):
    config = Configurations()
    # directory = config.get_configuration('baseDirectory')
    filename_format = config.get_configuration('baseFilenameFormat')
    task_start_time = params['task_start_time']
    # task_start_time = str(time.mktime(time.strptime(task_start_time, "%Y-%m-%d %H:%M:%S"))) #test task
    directory = params['baseDirectory']
    index = params['index']
    status = params['status']
    start_time = params['start_time']
    # hostname = params['hostname']
    ip = params['ip']
    task_id = params['task_id']
    if status == "success":
        output = dict()
        output["output"] = params['output']
        output["start_time"] = params['start_time']
        output["end_time"] = params['end_time']
        # dir_str = "C:\\Users\\haonchen\\Desktop\\ppmOutput\\1511227248"
        dir_str = create_directory(os.path.join(directory, task_start_time))
        start_timestamp = str(time.mktime(time.strptime(start_time, "%Y-%m-%d %H:%M:%S")))
        filename = "%s_%s_%s" % (ip, start_timestamp, index)
        with open(os.path.join(dir_str, filename), 'w') as f:
            f.write(json.dumps(output, indent=2))


