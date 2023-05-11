import datetime
import os
import re
import sys
import getopt
import requests
import json
from bs4 import BeautifulSoup


# 输入数字变成前面补0的字符串
def add_zero(num, length=2):
    return str(num).zfill(length)


def main(argv):
    opts, args = getopt.getopt(argv, "", ["openai-api-key=", "api2d-api-key="])
    openai_api_key = None
    api2d_api_key = None
    for opt, arg in opts:
        if opt == '--openai-api-key':
            openai_api_key = arg
        if opt == '--api2d-api-key':
            api2d_api_key = arg

    # 通过读取文件holidays.json获取json文件,并转换为python对象,不存在则返回空json
    try:
        with open('holidays.json', 'r', encoding='utf-8') as f:
            holidays = json.load(f)
    except:
        holidays = {}
    try:
        with open('all_holidays.json', 'r', encoding='utf-8') as f:
            all_holidays = json.load(f)
    except:
        all_holidays = {}
    html = requests.get(
        'http://sousuo.gov.cn/s.htm?'
        't=paper&advance=false&n=100&timetype=timeqb&mintime=&maxtime='
        '&sort=pubtime&q=%E9%83%A8%E5%88%86%E8%8A%82%E5%81%87%E6%97%A5%E5%AE%89%E6%8E%92%E7%9A%84%E9%80%9A%E7%9F%A5')
    html.encoding = 'utf-8'
    soup = BeautifulSoup(html.text, 'html.parser')
    all_notifications = soup.find_all('div', class_='result')[0].find_all('a')
    for notification in all_notifications:
        year_datas = {}
        year = re.findall(r'\d{4}', notification.text)
        if year:
            # 如果年份不在json文件中,则添加
            if year[0] in holidays:
                continue
        notification_html = requests.get(notification.get('href'))
        notification_html.encoding = 'utf-8'
        notification_soup = BeautifulSoup(notification_html.text, 'html.parser')
        content = notification_soup.find('td', class_='b12c').text
        # print(content)
        # 使用正则表达式获取每一行
        messages = re.findall(r'([一二三四五六七八九]、.*?)[\r\n　]', content)
        show_year = year[0]
        last_year = 0
        last_month = 0
        all_datas = {}
        # 带序号遍历每一行
        for index, message in enumerate(messages):
            last_year = show_year
            print(message)
            # 使用正则表达式获取日期 两个日期之间不能出现、
            useful_message = re.findall(r'(([^其]*)(其中.*)?)', message)
            work_messages = []
            if useful_message[0][2] != '':
                work_messages = re.findall(r'.*[，。](.*?上班)', useful_message[0][2])
            useful_message = useful_message[0][1] + (work_messages[0] if len(work_messages) else '')
            dates = re.findall(
                r'((?:\d{4}[年])?(?:\d{1,2}[月])?\d{1,2}[日](?:(?:[(（][^(（)）]*[)）])?[^、，\d](?:\d{4}[年])?(?:\d{1,2}[月])?\d{1,2}[日])*)',
                useful_message)
            for date in dates:
                interval = re.findall(
                    r'((?:\d{4}[年])?(?:\d{1,2}[月])?\d{1,2}[日](?:[(（][^(（)）]*[)）])?[^、，\d](?:\d{4}[年])?(?:\d{1,2}[月])?\d{1,2}[日])',
                    date)
                alone = re.findall(r'((?:\d{4}[年])?(?:\d{1,2}[月])?\d{1,2}[日])', date)
                all_datas[date + str(index)] = {}
                if len(interval) == 0 and len(alone) == 1:
                    day_info = re.findall(r'(?:(\d{4})[年])?(?:(\d{1,2})[月])?(\d{1,2})[日]', alone[0])
                    day_info_y = day_info[0][0] if day_info[0][0] != '' else last_year
                    last_year = day_info_y
                    day_info_m = day_info[0][1] if day_info[0][1] != '' else last_month
                    last_month = day_info_m
                    day_info_d = day_info[0][2]
                    all_datas[date + str(index)]['{}{}{}'.format(
                        str(day_info_y).zfill(4),
                        str(day_info_m).zfill(2),
                        str(day_info_d).zfill(2))] = {}
                    all_holidays['{}{}{}'.format(
                        str(day_info_y).zfill(4),
                        str(day_info_m).zfill(2),
                        str(day_info_d).zfill(2))] = {}
                    year_datas['{}{}{}'.format(
                        str(day_info_y).zfill(4),
                        str(day_info_m).zfill(2),
                        str(day_info_d).zfill(2))] = {}
                if len(interval) == 1 and len(alone) == 2:
                    day_info = re.findall(r'(?:(\d{4})[年])?(?:(\d{1,2})[月])?(\d{1,2})[日]', alone[0])
                    day_info_y = day_info[0][0] if day_info[0][0] != '' else last_year
                    last_year = day_info_y
                    day_info_m = day_info[0][1] if day_info[0][1] != '' else last_month
                    last_month = day_info_m
                    day_info_d = day_info[0][2]
                    all_datas[date + str(index)][
                        '{}{}{}'.format(
                            str(day_info_y).zfill(4),
                            str(day_info_m).zfill(2),
                            str(day_info_d).zfill(2))] = {}
                    all_holidays['{}{}{}'.format(
                        str(day_info_y).zfill(4),
                        str(day_info_m).zfill(2),
                        str(day_info_d).zfill(2))] = {}
                    year_datas['{}{}{}'.format(
                        str(day_info_y).zfill(4),
                        str(day_info_m).zfill(2),
                        str(day_info_d).zfill(2))] = {}
                    day_info_2 = re.findall(r'(?:(\d{4})[年])?(?:(\d{1,2})[月])?(\d{1,2})[日]', alone[1])
                    date_1 = datetime.datetime(int(day_info_y), int(day_info_m), int(day_info_d))
                    while True:
                        date_1 = date_1 + datetime.timedelta(days=1)
                        all_datas[date + str(index)][
                            '{}{}{}'.format(str(date_1.year).zfill(4), str(date_1.month).zfill(2),
                                            str(date_1.day).zfill(2))] = {}
                        all_holidays['{}{}{}'.format(str(date_1.year).zfill(4), str(date_1.month).zfill(2),
                                                  str(date_1.day).zfill(2))] = {}
                        year_datas['{}{}{}'.format(str(date_1.year).zfill(4), str(date_1.month).zfill(2),
                                                  str(date_1.day).zfill(2))] = {}
                        last_year = date_1.year
                        last_month = date_1.month
                        if str(date_1.day).zfill(2) == str(day_info_2[0][2]).zfill(2):
                            if str(date_1.month).zfill(2) == str(day_info_2[0][1]).zfill(2) or day_info_2[0][1] == '':
                                if str(date_1.year).zfill(4) == str(day_info_2[0][0]).zfill(4) or day_info_2[0][
                                    0] == '':
                                    break
            work_messages = re.findall(r'.*[，。](.*?上班)', message)
            if len(work_messages) != 0:
                for work_message in work_messages:
                    work_date = re.findall(
                        r'((?:\d{4}[年])?(?:\d{1,2}[月])?\d{1,2}[日](?:(?:[(（][^(（)）]*[)）])?[^、，\d](?:\d{4}[年])?(?:\d{1,2}[月])?\d{1,2}[日])*)',
                        work_message)
                    for date in work_date:
                        for data1 in all_datas[date + str(index)]:
                            all_datas[date + str(index)][data1]['work'] = True
                            all_holidays[data1]['work'] = True
                            year_datas[data1]['work'] = True
        year_datas = sorted(year_datas.items(), key=lambda x: x[0])
        year_datas = dict(year_datas)
        holidays[year[0]] = year_datas
    all_holidays = sorted(all_holidays.items(), key=lambda x: x[0])
    all_holidays = dict(all_holidays)
    with open('holidays.json', 'w', encoding='utf-8') as f:
        json.dump(holidays, f, ensure_ascii=False, indent=4)
    with open('all_holidays.json', 'w', encoding='utf-8') as f:
        json.dump(all_holidays, f, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    main(sys.argv[1:])
