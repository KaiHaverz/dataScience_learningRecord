from selenium import webdriver
from selenium.webdriver.common.by import By
import csv
import time

# 初始化CSV文件
csv_file = open('shanghai_rent.csv', 'w', newline='', encoding='utf-8')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['标题', '价格', '面积', '区域', '链接'])

# 初始化Selenium WebDriver
driver = webdriver.Chrome()

# 爬取多页数据
for page in range(1, 101):  # 假设爬取前100页
    url = f'https://sh.lianjia.com/zufang/pg{page}/'
    print(f'正在爬取第{page}页: {url}')

    driver.get(url)
    time.sleep(2)  # 等待页面加载

    # 查找租房信息
    rent_items = driver.find_elements(By.CSS_SELECTOR, 'div.content__list--item')

    for item in rent_items:
        try:
            title = item.find_element(By.CSS_SELECTOR, 'p.content__list--item--title').text.strip()
            price = item.find_element(By.CSS_SELECTOR, 'span.content__list--item-price').text.strip()
            area = item.find_element(By.CSS_SELECTOR, 'p.content__list--item--des').text.strip().split('/')[1].strip()
            region = item.find_element(By.CSS_SELECTOR, 'p.content__list--item--des').text.strip().split('/')[0].strip()
            link = item.find_element(By.CSS_SELECTOR, 'a.content__list--item--aside').get_attribute('href')

            csv_writer.writerow([title, price, area, region, link])
        except Exception as e:
            print(f'解析错误: {e}')

    # 每页爬取后暂停一段时间
    time.sleep(2)

# 关闭CSV文件
csv_file.close()

# 关闭WebDriver
driver.quit()
print('爬取完成，数据已保存到shanghai_rent.csv')