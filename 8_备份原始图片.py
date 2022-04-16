from multiprocessing import Manager, Pool
import os


def copyFile(oldFile, newFile, queue=None):
    with open(oldFile, 'rb') as f:
        content = f.read()
    with open(newFile, 'wb') as f:
        f.write(content)
    if queue is not None:
        queue.put(1)


def copyFolder(old, new):
    files = os.listdir(old)
    pool = Pool(8)
    # 待拷贝文件数
    n = files.__len__()
    queue = Manager().Queue(n)
    for file in files:
        pool.apply_async(copyFile, (f'{old}\\{file}', f'{new}\\{file}', queue))
    pool.close()

    # 完成拷贝的文件个数
    finish = 0
    while finish < n:
        finish += queue.get()
        rate = int(finish / n * 100)
        print('\r', '♦' * int(rate / 5), f'{rate}%', end='')

    pool.join()

line_list = []
with open('1_keyword.txt', encoding='utf-8') as file:
    line_list = [k.strip() for k in file.readlines()]  # 用 strip()移除末尾的空格
def main():
    backup_name='未缩放备份图片'
    if not os.path.exists(backup_name):
        os.mkdir(backup_name)
    new = backup_name+'/'+word+'（未缩放）'
    if os.path.exists(old):
        if os.path.isdir(old):
            print('第八步：'+word+'文件夹备份中...')
            print("------------------------------------------------------------")
            copyFolder(old, new)
            print("\n------------------------------------------------------------\n\n")
            return
        copyFile(old, new)
        return
    print('原文件不存在！')
    main()


if __name__ == '__main__':
    for word in line_list:
        old = '标准处理图片/' + word
        main()