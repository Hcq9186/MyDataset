import os
import cv2
import time
import requests
import numpy as np
from selenium import webdriver

# TODO: set parameters
# These two parameters needs to be modified according to your actual situation.
chrome_driver_path = 'chromedriver_win32/chromedriver.exe'
base_url = ''

home_page = 'https://graph.baidu.com/pcpage/index?tpl_from=pc'
seed_imgs_dir = '未缩放备份图片/桥梁损伤（未缩放）'
save_dir = '桥梁损伤相似图片'


def prepare_seed_imgs():
    seed_imgs_url_list = []
    save_dir_list = []
    for file_name in os.listdir(seed_imgs_dir):
        cur_url = base_url + file_name
        seed_imgs_url_list.append(cur_url)

        base_file_name = file_name[:-4]
        cur_save_dir = os.path.join(save_dir, base_file_name)
        if not os.path.exists(cur_save_dir):
            os.mkdir(cur_save_dir)
        save_dir_list.append(cur_save_dir)
    return seed_imgs_url_list, save_dir_list


def search_similar_images(browser, image_url, max_page):
    print("start find similar image of {}".format(image_url))

    search_failed = True
    try_num = 0
    while (search_failed):
        if try_num >= 3:
            break
        try:
            browser.get(home_page)

            # 拖拽图片到此处或粘贴图片网址
            url_upload_textbox = browser.find_element_by_css_selector(
                '#app > div > div.page-banner > div.page-search > div > div > div.graph-search-left > input')
            url_upload_textbox.send_keys(image_url)

            # 识图一下
            search_image_button = browser.find_element_by_css_selector(
                '#app > div > div.page-banner > div.page-search > div > div > div.graph-search-center')
            search_image_button.click()

            # 等待百度识图结果
            time.sleep(15)

            # 切换到当前窗口(好像可有可无)
            browser.current_window_handle

            # 测试是否成功
            graph_similar = browser.find_element_by_class_name('graph-similar-list')

            # 运行到这里说明模拟使用百度识图功能成功，页面已正常加载
            search_failed = False
        except Exception as e:
            # print("ERROR:" + traceback.format_exc())
            print("ERROR: error when request baidu image search.")
        finally:
            try_num += 1

    if search_failed:
        print("give up current image")
        return []

    # 动态加载max_page次页面
    download_page = 0
    print("dynamic loading web page...")
    while download_page < max_page:
        # 模拟向下滑动滚动条动态加载
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # 等待滚动条10s
        time.sleep(10)
        download_page += 1

    # 解析页面中的所有url
    graph_similar = browser.find_element_by_class_name('graph-similar-list')
    left_column = graph_similar.find_element_by_css_selector('div > div:nth-child(1)')
    middle_column = graph_similar.find_element_by_css_selector('div > div:nth-child(2)')
    right_column = graph_similar.find_element_by_css_selector('div > div:nth-child(3)')

    left_column_imgs = left_column.find_elements_by_tag_name('a')
    middle_column_imgs = middle_column.find_elements_by_tag_name('a')
    right_column_imgs = right_column.find_elements_by_tag_name('a')

    url_list = []
    for img_box in left_column_imgs:
        img_url = img_box.find_element_by_tag_name('img').get_attribute('src')
        url_list.append(img_url)
    for img_box in middle_column_imgs:
        img_url = img_box.find_element_by_tag_name('img').get_attribute('src')
        url_list.append(img_url)
    for img_box in right_column_imgs:
        img_url = img_box.find_element_by_tag_name('img').get_attribute('src')
        url_list.append(img_url)

    total_imgs_num = len(left_column_imgs) + len(middle_column_imgs) + len(right_column_imgs)
    print("totally fing {} images.".format(total_imgs_num))
    return url_list


def download_search_images(url_list, cur_save_dir):
    print("start downloading...")
    for img_url in url_list:
        try:
            response = requests.get(img_url, timeout=1)
        except Exception as e:
            print("ERROR: download img timeout.")

        try:
            # imgDataNp = np.fromstring(response.content, dtype='uint8')
            imgDataNp = np.frombuffer(response.content, dtype='uint8')
            img = cv2.imdecode(imgDataNp, cv2.IMREAD_UNCHANGED)

            img_name = img_url.split('/')[-1]
            save_path = os.path.join(cur_save_dir, img_name)
            cv2.imwrite(save_path, img)
        except Exception as e:
            print("ERROR: download img corruption.")


if __name__ == "__main__":
    browser = webdriver.Chrome(executable_path=chrome_driver_path)
    browser.set_page_load_timeout(30)

    seed_imgs_url_list, save_dir_list = prepare_seed_imgs()

    for idx, seed_url in enumerate(seed_imgs_url_list):
        print(idx)

        # 获取百度识图结果
        url_list = search_similar_images(browser, seed_url, max_page=30)

        if len(url_list) == 0:
            continue

        # 下载图片
        cur_save_dir = save_dir_list[idx]
        download_search_images(url_list, cur_save_dir)