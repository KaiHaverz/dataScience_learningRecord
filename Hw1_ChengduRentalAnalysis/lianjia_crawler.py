import requests
from bs4 import BeautifulSoup
import csv
import time

# 设置请求头，模拟浏览器行为
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

# 初始化CSV文件
csv_file = open('chengdu_rent.csv', 'w', newline='', encoding='utf-8')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['标题', '价格', '面积', '区域', '链接'])

# 爬取多页数据
for page in range(1, 100):  # 爬取前10页
    url = f'https://cd.lianjia.com/zufang/pg{page}/'
    print(f'正在爬取第{page}页: {url}')

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # 查找租房信息
    rent_items = soup.find_all('div', class_='content__list--item')

    for item in rent_items:
        try:
            title = item.find('p', class_='content__list--item--title').text.strip()
            price = item.find('span', class_='content__list--item-price').text.strip()
            area = item.find('p', class_='content__list--item--des').text.strip().split('/')[1].strip()
            region = item.find('p', class_='content__list--item--des').text.strip().split('/')[0].strip()
            link = item.find('a', class_='content__list--item--aside')['href']

            csv_writer.writerow([title, price, area, region, link])
        except Exception as e:
            print(f'解析错误: {e}')

    # 每页爬取后暂停一段时间
    time.sleep(2)

# 关闭CSV文件
csv_file.close()
print('爬取完成，数据已保存到chengdu_rent.csv')