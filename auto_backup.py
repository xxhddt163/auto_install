import os
import zipfile
import time
from getpass import getuser

max_file = int(input("输入最多保存的存档数："))
sleep_time = int(input("输入存档备份间隔时间（分钟）："))
username = getuser()  # 当前用户名
print(f"{time.strftime('%Y-%m-%d %H:%M')}", fr"当前用户名为{username},游戏存档目录为C:\Users\{username}\Zomboid\Saves")


def check_dir():  # 目录检查
    print(f"{time.strftime('%Y-%m-%d %H:%M')}", "正在检查存档备份目录......")
    os.chdir(fr'C:\Users\{username}\Zomboid')
    if 'Saves_back' not in os.listdir(os.getcwd()):  # 检查Saves_back文件夹是否创建
        print(f"{time.strftime('%Y-%m-%d %H:%M')}", fr"存档文件夹C:\Users\{username}\Zomboid\Saves_back不存在，将自动创建")
        os.mkdir(os.path.join(os.getcwd(), 'Saves_back'))  # 没有创建就创建该文件夹
    else:
        print(f"{time.strftime('%Y-%m-%d %H:%M')}", fr"存档文件夹C:\Users\{username}\Zomboid\Saves_back已存在")


def zip():
    print(f"{time.strftime('%Y-%m-%d %H:%M')}", "正在备份存档......")
    os.chdir(fr'C:\Users\{username}\Zomboid')
    file_name = time.strftime('%Y%m%d%H%M') + '.zip'
    f = zipfile.ZipFile(os.path.join(fr'C:\Users\{username}\Zomboid', 'Saves_back', file_name), 'w')
    for root_dir, dir_list, file_list in os.walk(os.path.join(os.getcwd(), 'Saves')):
        for name in dir_list:  # 备份所有目录包括空目录
            target_file = os.path.join(root_dir.lstrip(fr'C:\Users\{username}\Zomboid'), name)
            f.write(target_file, target_file, zipfile.ZIP_DEFLATED)
        for name in file_list:  # 备份所有文件
            target_file = os.path.join(root_dir.lstrip(fr'C:\Users\{username}\Zomboid'), name)
            f.write(target_file, target_file, zipfile.ZIP_DEFLATED)

    f.close()
    print(f"{time.strftime('%Y-%m-%d %H:%M')}", f"存档备份完毕，{sleep_time}分钟后将再次备份")


def check_files():  # 文件检查
    print(f"{time.strftime('%Y-%m-%d %H:%M')}", "正在检查存档文件个数......")
    os.chdir(fr'C:\Users\{username}\Zomboid\Saves_back')
    print(f"{time.strftime('%Y-%m-%d %H:%M')}",
          fr"C:\Users\{username}\Zomboid\Saves_back目录下一共有{len(os.listdir(os.getcwd()))}个存档")
    cache = os.listdir(os.getcwd())  # 获取当前目录下的所有存档文件名
    cache.sort(key=lambda x: os.lstat(x).st_ctime)  # 所有存档文件按C-time进行排序
    while True:
        if len(os.listdir(os.getcwd())) < max_file:
            break
        target_file = cache[0]  # 列表中的第一个存档肯定为创建时间最早的存档
        print(f"{time.strftime('%Y-%m-%d %H:%M')}", f"存档文件大于{max_file}个、正在删除存档文件：{target_file}")
        os.remove(os.path.join(fr'C:\Users\{username}\Zomboid\Saves_back', target_file))
        del cache[0]


def main():
    while True:
        check_dir()
        check_files()
        zip()
        time.sleep(sleep_time * 60)


if __name__ == '__main__':
    main()
