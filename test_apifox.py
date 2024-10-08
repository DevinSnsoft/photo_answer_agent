import json
from PIL import Image

import requests
#
# def crop_image(input_image_path, output_image_path, top_left, bottom_right):
#     """
#     根据给定的坐标截取图片区域并保存。
#
#     :param input_image_path: 输入图片的路径
#     :param output_image_path: 输出图片的路径
#     :param top_left: 左上角坐标 (x1, y1)
#     :param bottom_right: 右下角坐标 (x2, y2)
#     """
#     try:
#         # 打开图片
#         with Image.open(input_image_path) as img:
#             # 截取区域
#             cropped_img = img.crop((top_left[0], top_left[1], bottom_right[0], bottom_right[1]))
#             # 保存截取后的图片
#             cropped_img.save(output_image_path)
#             print(f"图片成功保存为: {output_image_path}")
#     except Exception as e:
#         print(f"处理图片时出错: {e}")

if __name__ == '__main__':
    # url = "https://zhixingyun.yuntim.com/func/cutting_service"
    url = "https://zhixingyun.yuntim.com/func/direction_detection_service"
    picture_url = "https://cdnbj.bookln.cn/correct/v2/20240927/155448417_06d529e0-7cb6-11ef-a24c-899d3bf73cf5.jpg"
    payload = {"data": json.dumps({
        "url": picture_url})}
    headers = {
        'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
        'Accept': '*/*',
        'Host': 'zhixingyun.yuntim.com',
        'Connection': 'keep-alive'
    }
    response_kuangtu = requests.request("POST", url, headers=headers, data=payload)
    print(response_kuangtu.text)
    if json.loads(response_kuangtu.text)['data']['flag'] == 1000:
        url = "https://zhixingyun.yuntim.com/func/cutting_service"
        payload = {"data": json.dumps({
            "url": picture_url})}
        headers = {
            'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
            'Accept': '*/*',
            'Host': 'zhixingyun.yuntim.com',
            'Connection': 'keep-alive'
        }
        response_cut = requests.request("POST", url, headers=headers, data=payload)
        print("输入你想要解答的区域：")
        tmp = json.loads(response_cut.text)['data']['boxs']
        for i in range(len(json.loads(response_cut.text)['data']['boxs'])):
            print("区域{", i+1, "}\n")
        input_region = 1
        # crop_image()
        #
        print(response_cut.text)
        # print(tmp)

# 示例用法
# input_image = 'input.jpg'  # 输入图片路径
# output_image = 'output.jpg'  # 输出图片路径
# top_left_coords = (50, 50)  # 左上角坐标
# bottom_right_coords = (200, 200)  # 右下角坐标
#
# crop_image(input_image, output_image, top_left_coords, bottom_right_coords)
