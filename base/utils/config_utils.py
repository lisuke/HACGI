import configparser
import os

# 获取config配置文件


def getConfig(file_path):
    config = configparser.ConfigParser()
    config.read(file_path)
    return config
