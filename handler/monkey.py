#!/usr/bin/python
# -*- coding: utf-8 -*-
import threading
import os
from handler.device import *
import time


def push_maxim(conn):
    maxim_dir = os.getcwd() + '\\maxim'
    conn.push(maxim_dir + '\\monkey.jar', '/sdcard/')
    conn.push(maxim_dir + '\\framework.jar', '/sdcard/')


def push_white_list_file(conn):
    maxim_dir = os.getcwd() + '\\maxim'
    conn.shell('rm /sdcard/awl.strings')
    conn.push(maxim_dir + '\\awl.strings', '/sdcard/')


def start_maxim_simple(conn, package, mode, time):
    conn.service('uiautomator').stop()
    shell_command = 'adb shell CLASSPATH=/sdcard/monkey.jar:/sdcard/framework.jar ' + \
                    'exec app_process /system/bin tv.panda.test.monkey.Monkey ' + \
                    '-p ' + package + ' '\
                    '--' + mode + ' ' + \
                    '--running-minutes ' + time + ' ' + \
                    '-v -v'
    output, exit_code = conn.shell(shell_command, timeout=300)
    print('code:%s' % exit_code)
    conn.service('uiautomator').start()


def start_maxim(conn, package, shell_command, log_mobile_path, log_local_path, timeout):

    # start app
    # conn.app_stop(package)
    # conn.app_start(package)
    # time.sleep(3)
    # stop ui2 server
    conn.service('uiautomator').stop()
    time.sleep(3)
    # task = conn.shell(shell_command, stream=True)
    output, exit_code = conn.shell(shell_command, timeout=timeout)
    # print('code:%s' % exit_code)
    maxim_dir = os.getcwd() + '\\maxim'
    file_name = '%s_%s' % ('monkey_event.log', conn.info['productName'])
    log_file = open('%s\\%s' % (maxim_dir, file_name), 'w')
    log_file.write(output)
    # try:
    #     for line in task.iter_lines():
    #         log_file.write(line.decode("utf-8") + '\n')
    # finally:
    #     task.close()
    print('Done')
    log_file.close()
    pull_log(conn, log_mobile_path, log_local_path)


def pull_log(conn, monkey_log_mobile_path, monkey_log_local_path):
    # pull log to local
    output, exit_code = conn.shell('ls ' + monkey_log_mobile_path)
    output_file_list = output.split('\n')
    print('%s\n%s' % (conn.info['productName'], output))
    for output_file in output_file_list:
        print('pull %s ...' % output_file)
        if (output_file is not None) and output_file != '':
            conn.pull(monkey_log_mobile_path + output_file, monkey_log_local_path + '\\' + output_file)


def logcat_begin(conn, monkey_log_mobile_path):
    # output, exit_code = conn.shell('logcat -f %s%s' % (monkey_log_mobile_path, 'logcat.log'))
    # print(exit_code)
    # time.sleep(5)
    output, exit_code = conn.shell('ps -ef|grep logcat')
    print(output)
    output, exit_code = conn.shell('killall logcat')


def run_monkey_multi_device(device_list, monkey_args):
    # handle config
    package = monkey_args.get('package')
    throttle = monkey_args.get('throttle')
    log_output_customize = monkey_args.get('log_output_customize')
    monkey_log_mobile_path = monkey_args.get('monkey_log_mobile_path')
    monkey_log_local_path = monkey_args.get('monkey_log_local_path')
    log_level = monkey_args.get('log_level')
    is_fs_mode = monkey_args.get('dfs_mode')
    is_mix_mode = monkey_args.get('uiautomatormix')
    mix_percent = monkey_args.get('uiautomatormix_percent')
    is_white_list = monkey_args.get('white_list')
    times = monkey_args.get('running-minutes')
    is_crash_shot = monkey_args.get('crash_shot')

    shell_command = 'CLASSPATH=/sdcard/monkey.jar:/sdcard/framework.jar ' + \
                    'exec app_process /system/bin tv.panda.test.monkey.Monkey ' + \
                    '-p ' + package
    # delay timeout
    timeout = (int(times) + 2) * 60

    if is_mix_mode:
        shell_command = '%s %s %s %s' % (shell_command, '--uiautomatormix', '--pct-uiautomatormix', str(mix_percent))
    if is_fs_mode:
        shell_command = '%s %s' % (shell_command, '--uiautomatordfs')
    if log_output_customize:
        shell_command = '%s %s %s' % (shell_command, ' --output-directory', monkey_log_mobile_path)
    if int(throttle) != 0:
        shell_command = '%s %s %s' % (shell_command, '--throttle', str(throttle))
    if is_crash_shot:
        shell_command = '%s %s' % (shell_command, '--imagepolling')
    if is_white_list:
        shell_command = '%s %s %s' % (shell_command, '--act-whitelist-file', '/sdcard/awl.strings')
    if int(log_level) == 1:
        shell_command = '%s %s' % (shell_command, '-v')
    if int(log_level) == 2:
        shell_command = '%s %s' % (shell_command, '-v -v')
    if int(log_level) == 3:
        shell_command = '%s %s' % (shell_command, '-v -v -v')
    shell_command = '%s %s %s' % (shell_command, '--running-minutes', str(times))
    print(shell_command)

    conn_list = []
    for dev in device_list:
        conn_list.append(dev.conn())

    for conn in conn_list:
        if conn is not None:
            print('device:%s, push monkey.jar framework.jar to mobile...' % conn.info['productName'])
            push_maxim(conn)

    if is_white_list:
        for conn in conn_list:
            if conn is not None:
                print('device:%s, push awl.strings to mobile...' % conn.info['productName'])
                push_white_list_file(conn)

    for conn in conn_list:
        if conn is not None:
            if not log_output_customize:
                monkey_log_mobile_path = '/sdcard/'
            threading.Thread(target=start_maxim,
                             args=(conn,
                                   package,
                                   shell_command,
                                   monkey_log_mobile_path,
                                   monkey_log_local_path,
                                   timeout)).start()

    # for conn in conn_list:
    #     if conn is not None:
    #         logcat_begin(conn, monkey_log_mobile_path)
    #         pull_log(conn, monkey_log_mobile_path, monkey_log_local_path)



