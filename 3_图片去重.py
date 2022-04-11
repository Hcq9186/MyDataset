import os
import hashlib

line_list = []
with open('./0_name.txt', encoding='utf-8') as file:
    line_list = [k.strip() for k in file.readlines()]  # 用 strip()移除末尾的空格
filedir = '' # 设置为爬虫后的图片路径，必须自行修改


def filecount(DIR):
    filecount = len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])
    return (filecount)


def md5sum(filename):
    f = open(filedir+'/'+filename, 'rb')
    md5 = hashlib.md5()
    while True:
        fb = f.read(8096)
        if not fb:
            break
        md5.update(fb)
    f.close()
    return (md5.hexdigest())


def delfile():
    all_md5 = {}
    dir =os.walk(filedir)
    for i in dir:
        for tlie in i[2]:

            if md5sum(tlie) in all_md5.values():
                os.remove(filedir+'/'+tlie)
                print(tlie)
            else:
                all_md5[tlie] = md5sum(tlie)


if __name__ == '__main__':
    for word in line_list:
        filedir = word
        oldf = filecount(filedir)
        print(word + '文件夹图片去重中...')
        print("------------------------------------------------------------")
        print('去重前有', oldf, '个文件\n请稍等正在删除重复文件...')
        delfile()
        print('\n去重后剩', filecount(filedir), '个文件')
        print('\n一共删除了', oldf - filecount(filedir), '个文件\n')
        print("------------------------------------------------------------\n\n")
