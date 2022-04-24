import numpy as np
from PIL import Image


# 判断是否需要进行图像填充
def judge(img, wi, he):
    width, height = img.size
    # 默认新图像尺寸初始化为原图像
    new_width, new_height = img.size
    if width % wi != 0:
        new_width = (width//wi + 1) * wi
    if height % he != 0:
        new_height = (height//he + 1) * he
    # 新建一张新尺寸的全黑图像
    new_image = Image.new('RGB', (new_width, new_height), (0, 0, 0))
    # 将原图像粘贴在new_image上，默认为左上角坐标对应
    new_image.paste(img, box=None, mask=None)
    new_image.show()
    return new_image

# 按照指定尺寸进行图片裁剪
def crop_image(image, patch_w, patch_h):
    width, height = image.size
    # 补丁计数
    cnt = 0
    for w in range(0, width, patch_w):
        for h in range(0, height, patch_h):
            cnt += 1
            # 指定原图片的左、上、右、下
            img = image.crop((w, h, w+patch_w, h+patch_h))
            img.save("dog-%d.jpg" % cnt)
    print("图片补丁裁剪结束，共有{}张补丁".format(cnt))

def main():
    image_path = "标准处理图片/混凝土桥梁/混凝土桥梁_4.jpg"
    img = Image.open(image_path)
    # 查看图像形状
    print("原始图像形状{}".format(np.array(img).shape))
    size_list = []
    with open('00_img_size.txt', encoding='utf-8') as file:
        size_list = [k.strip() for k in file.readlines()]  # 用 strip()移除末尾的空格

    need_width = int(size_list[0])  # 设置你想缩放的图片宽度的阈值，默认COCO图片格式，不用更改，VOC为500*400
    need_height = int(size_list[1])  # 设置你想缩放的图片宽度的阈值，默认COCO图片格式，不用更改，VOC为500*400
    # 输入指定的补丁宽高
    # print("输入补丁宽高：")
    # wi, he = map(int, input().split(" "))


    # 进行图像填充
    new_image = judge(img, need_width, need_height)
    # 图片补丁裁剪
    crop_image(new_image, need_width, need_height)

if __name__ == '__main__':
    main()
