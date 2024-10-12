from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import time

# 初始化CSV文件
csv_file = open('chengdu_new_homes.csv', 'w', newline='', encoding='utf-8')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['楼盘名称', '价格', '区域', '链接'])

# 初始化Selenium WebDriver
driver = webdriver.Chrome()

# 爬取多页数据
for page in range(1, 101):  # 假设爬取前100页
    url = f'https://cd.fang.lianjia.com/loupan/pg{page}/'
    print(f'正在爬取第{page}页: {url}')

    driver.get(url)
    time.sleep(3)  # 增加等待时间，确保页面加载

    # 等待页面元素加载
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'li.resblock-list'))
        )
    except Exception as e:
        print(f'页面加载超时: {e}')
        continue

    # 查找新房信息
    new_home_items = driver.find_elements(By.CSS_SELECTOR, 'li.resblock-list')

    for item in new_home_items:
        try:
            title = item.find_element(By.CSS_SELECTOR, 'a.name').text.strip()
            price = item.find_element(By.CSS_SELECTOR, 'span.number').text.strip()
            region = item.find_element(By.CSS_SELECTOR, 'span.resblock-location').text.strip()
            link = item.find_element(By.CSS_SELECTOR, 'a.name').get_attribute('href')

            csv_writer.writerow([title, price, region, link])
        except Exception as e:
            print(f'解析错误: {e}')

    # 每页爬取后暂停一段时间
    time.sleep(2)

# 关闭CSV文件
csv_file.close()

# 关闭WebDriver
driver.quit()
print('爬取完成，数据已保存到chengdu_new_homes.csv')