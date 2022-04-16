import os

def rename():
    path = ''
    line_list = []
    with open('1_keyword.txt', encoding='utf-8') as file:
        line_list = [k.strip() for k in file.readlines()]  # 用 strip()移除末尾的空格

    # TODO: set parameters
    # 可更改内容
    # -----------------------------------------------------------------#
    startNumber = 1        # 从第几张图片开始，看情况自行修改,保证各文件夹中图片序号连续
    fileType = ".jpg"      # 图片格式，这项一般不该
    # -----------------------------------------------------------------#\

    seq = "0"
    name1 = seq*5
    name2 = seq*4
    name3 = seq*3
    name4 = seq*2
    name5 = seq
    for word in line_list:
        path = '标准处理图片/'+ word
        filelist=os.listdir(path)
        num = 1
        count = 0
        for files in filelist:
            Olddir=os.path.join(path,files)
            if os.path.isdir(Olddir):
                continue
            if num in range(0, 10):
                Newdir=os.path.join(path, name1 + str(count + int(startNumber)) + fileType)
            if num in range(10, 100):
                Newdir=os.path.join(path, name2 + str(count + int(startNumber)) + fileType)
            if num in range(100, 1000):
                Newdir=os.path.join(path, name3 + str(count + int(startNumber)) + fileType)
            if num in range(1000, 10000):
                Newdir=os.path.join(path, name4 + str(count + int(startNumber)) + fileType)
            if num in range(10000, 100000):
                Newdir=os.path.join(path, name5 + str(count + int(startNumber)) + fileType)
            os.rename(Olddir,Newdir)
            count+=1
            num=startNumber+num
        print('第七步：'+word + '文件夹图片重命名中...')
        print("------------------------------------------------------------")
        print("一共修改了"+str(count)+"个文件")
        print("------------------------------------------------------------\n\n")

if __name__ == '__main__':
    rename()
