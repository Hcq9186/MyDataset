import os

def modify_jpg(path):
    for root,dirs,files in os.walk(path):
       for dir in dirs:
           mulu = root + '/'+ dir     #获取根目目录下每个子文件夹
           os.chdir(mulu)              #改变目录，不改变到文件所在目录的话，无法给文件重新命名
           files = os.listdir(mulu)    #获取当前目录下的所有文件
           for filename in files:
               portion = os.path.splitext(filename)  # 分离文件名与扩展名
               if portion[1] != '.jpg':
                   newname = portion[0] + '.jpg'  # 重新组合文件名和后缀名
                   os.rename(filename, newname)
                   print('jpg modify succsee!')

if __name__ == '__main__':
    modify_jpg(os.path.dirname(os.path.abspath(__file__))+'/'+'标准处理图片')
    print("第五步：图片转换已经完成")