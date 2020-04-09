# machine_checker.py
# 设备故障判断，对设备上报的数据进行查询、分析
# 如果某个设备一定时间未报告状态，或关键数据超标
# 则插入一笔数据到设备故障表
from db_coffee_dao import *
from db_helper import *
from db_conf import *
import time

def main():
    db_helper = DBHelper()  #实例化一个数据访问对象
    coffeeDao = CoffeeDao(db_helper)

    while True:
        do_check_last_send_time(coffeeDao)  # 检查设备最后发送数据时间
        
        time.sleep(120)

# 检查关键参数有没有超过阈值
def check_key_param():
    ''' 思路：
    1. 读取每个设备最后一笔上报数据的详细内容
       （从mange_eqstate表中读取）
    2. 取出mange_eqstate表一笔记录的关键字段，如：
       锅炉温度、锅炉压力、环境温度、配料数量
    3. 判断第2步取出的参数，有没有超过允许的范围
       （范围：从设备类型表中读取）
       1)根据machine_id找到设备类型编号
       2)根据设备编号找到设备类型信息
       3)从设备类型中取出该类型设备允许的参数范围
    4. 在manage_eqwaring表插入一笔告警信息
    '''

    pass


# 查询所有设备最后发送数据时间到当前时间点的事件间隔，并判断故障
def do_check_last_send_time(coffeeDao):
    result = coffeeDao.query_machine_last_send()
    for i in result:
        machine_id = int(i[0])  # 设备ID
        diff_time = i[1]  # 到当前时间点时间差
        alert_msg = ""
        is_broken = False 

        if not diff_time:
            is_broken = True
            #alert_msg = "编号%d的咖啡机没有上报状态，可能存在故障" % machine_id
            alert_msg = "id:%d err" % machine_id
        elif diff_time >= machine_max_interval:
            is_broken = True
            #alert_msg = "编号%d的咖啡机最后一次上报状态已经%d秒，可能存在故障" % (machine_id, diff_time)
            alert_msg = "id:%d err, last send:%d" % (machine_id, diff_time)

        if is_broken:
            result = coffeeDao.add_machine_warnings(machine_id, alert_msg)
             

if __name__ == "__main__":
    main()

