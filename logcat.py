import uiautomator2 as u2
import time
import threading


def ps_logcat(conn):
    output, exit_code = conn.shell('ps |grep logcat')
    print(output)


def run_logcat(conn, monkey_log_mobile_path):
    try:
        r = conn.shell('logcat -f %s%s' % (monkey_log_mobile_path, 'logcat.log'), stream=True)
    # run maxium 600s
    # deadline = time.time() + 600
        # for line in r.iter_lines():
        #     if time.time() > deadline:
        #         break
            # print("Read:", line.decode('utf-8'))
    finally:
        r.close()


def end_logcat(conn):
    output, exit_code = conn.shell('killall logcat')
    print(exit_code)


def ps_actions(conn):
    time.sleep(5)
    ps_logcat(conn)
    time.sleep(5)
    ps_logcat(conn)
    time.sleep(5)
    ps_logcat(conn)

def run_logcat_actions(conn, monkey_log_mobile_path):
    run_logcat(conn, monkey_log_mobile_path)


def logcat_begin(conn, monkey_log_mobile_path):
    threading.Thread(target=ps_actions, args=(conn,)).start()
    threading.Thread(target=run_logcat_actions, args=(conn, monkey_log_mobile_path)).start()
    time.sleep(30)
    threading.Thread(target=end_logcat, args=(conn,)).start()

def main():
    conn = u2.connect('192.168.0.106')
    logcat_begin(conn, '/sdcard/')


if __name__ == '__main__':
    main()