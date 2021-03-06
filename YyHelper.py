# -*- coding=utf-8 -*-

import os
import time
import re
import getopt
import sys
import random

class YyHelper:

    device = ""
    device_x = 0
    device_y = 0
    # Sumsung s6 2560 * 1440
    # Xiaomi 5 1920 * 1080

    def __init__(self, device=""):
        self.device = device
        self.adb = Adb(device)
        self.initDeviceResolution()

    def initDeviceResolution(self):
        '''
        获取屏幕分辨率
        '''
        resolution = self.adb.getResolution()
        self.device_x = resolution[1]
        self.device_y = resolution[0]

    def startFightForMaterial(self):
        '''
        点击挑战按钮
        :return:
        '''
        challengeBtnPercentage = [0.75, 0.75]
        readyBtnPercentage = [0.90, 0.75]
        finishPercentage = [0.50, 0.50]

        challengeBtnCoordinate = [challengeBtnPercentage[0] * self.device_x, challengeBtnPercentage[1] * self.device_y]
        readyBtnCoordinate = [self.device_x * readyBtnPercentage[0], self.device_y * readyBtnPercentage[1]]
        finishCoordinate = [self.device_x * finishPercentage[0], self.device_y * finishPercentage[1]]

        self.adb.touch(challengeBtnCoordinate)
        self.sleep(20)

        self.adb.touch(readyBtnCoordinate)
        self.sleep(70)  # wait for fighting

        self.adb.touch(finishCoordinate)
        self.sleep(5)  # wait for showing the pangwawa
        self.adb.touch(finishCoordinate)
        self.sleep(5)  # gifts come from the pangwawa
        self.adb.touch(finishCoordinate)
        self.sleep(20)  # quit the fight scenario

    def fightForMaterialEndless(self):
        '''
        无尽模式刷御魂和觉醒材料
        '''
        challengeBtnPercentage = [0.75, 0.75]
        readyBtnPercentage = [0.90, 0.75]
        finishPercentage = [0.50, 0.50]

        while True:
            self.touchByPercent(challengeBtnPercentage)
            self.sleep(1)
            self.touchByPercent(readyBtnPercentage)
            self.sleep(1)
            self.touchByPercent(finishPercentage)
            self.sleep(1)

    def fightWithGroup(self):
        '''
        组队刷御魂和觉醒材料时自动接受好友邀请和准备
        '''
        acceptInviteBtnPercentage = [0.588, 0.602]
        readyBtnPercentage = [0.90, 0.75]

        while True:
            self.touchByPercent(readyBtnPercentage)
            self.sleep(1)
            self.touchByPercent(acceptInviteBtnPercentage)
            self.sleep(1)

    def fightingSkills(self):
        '''
        刷斗技
        '''
        fightBtnPercentage = [0.863, 0.811]
        readyBtnPercentage = [0.90, 0.75]
        quitBtnPercentage = [0.0296, 0.0439]
        quitConfirmBtnPercent = [0.582, 0.592]

        while True:
            self.touchByPercent(fightBtnPercentage)
            self.sleep(16)
#             self.touchByPercent(readyBtnPercentage)
#             self.sleep(20)
            self.touchByPercent(quitBtnPercentage)
            self.sleep(1)
            self.touchByPercent(quitConfirmBtnPercent)
            self.sleep(1)
            self.touchByPercent(quitConfirmBtnPercent)
            self.sleep(5)

    def fightForChapter(self):
        '''
        章节 by @zxjay
        '''
        enterChapter = [0.9, 0.47]
        challengeBtnByPercentage = [0.75, 0.75]
        readyBtnByPercentage = [0.90, 0.75]
        finishByPercentage = [0.50, 0.50]


        enterChapterPos = [enterChapter[0] * self.device_x, enterChapter[1] * self.device_y]
        challengeBtnCoordinate = [challengeBtnByPercentage[0] * self.device_x, challengeBtnByPercentage[1] * self.device_y]
        readyBtnCoordinate = [self.device_x * readyBtnByPercentage[0], self.device_y * readyBtnByPercentage[1]]
        finishCoordinate = [self.device_x * finishByPercentage[0], self.device_y * finishByPercentage[1]]

        #touch chapter
        self.adb.touch(enterChapterPos)
        self.sleep(4)
        #touch challenge btn
        self.adb.touch(challengeBtnCoordinate)
        self.sleep(10)
        for yyp in range(0, 4):
            walkPos = [yyp * 0.25 * self.device_x, 0.757 * self.device_y]
            self.adb.touch(walkPos)
            self.sleep(1)

            for num in range(1, 14):
                itemPos = [num * 0.06611 * self.device_x * random.uniform(0.95, 1.05), 0.558 * self.device_y * random.uniform(0.95, 1.05)]
                self.adb.touch(itemPos)
                #self.sleep(0.2)
                itemPos = [num * 0.06611 * self.device_x * random.uniform(0.95, 1.05), 0.338 * self.device_y * random.uniform(0.95, 1.05)]
                self.adb.touch(itemPos)
                #self.sleep(0.2)
                itemPos = [num * 0.06611 * self.device_x * random.uniform(0.95, 1.05), 0.457 * self.device_y * random.uniform(0.95, 1.05)]
                self.adb.touch(itemPos)
                self.sleep(1)

        self.adb.touch(readyBtnCoordinate)

    def fightForChapterEndless(self):
        while True:
            self.fightForChapter()

    def startFightForEnchantment(self):
        enchantment_start_x = 640
        enchantment_start_y = 300
        enchantment_middle_x = 1280
        enchantment_middle_y = 530
        enchantment_attack_start_x = 790
        enchantment_attack_start_y = 500

        interval_x = enchantment_middle_x - enchantment_start_x
        interval_y = enchantment_middle_y - enchantment_start_y

        enchantment_list = range(0, 9)
        for enchantment_index in enchantment_list:
            # if enchantment_index <= 7:
            #     continue
            index_x = enchantment_index % 3
            index_y = (enchantment_index - enchantment_index % 3) / 3

            print("index x | y is : " + str(index_x) + " | " + str(index_y))

            enchantment_x = enchantment_start_x + index_x * interval_x
            enchantment_y = enchantment_start_y + index_y * interval_y
            self.adb.touch([enchantment_x, enchantment_y])
            # wait for the showing of the challenge btn
            self.sleep(2)

            enchantment_attack_x = enchantment_attack_start_x + interval_x * index_x
            enchantment_attack_y = enchantment_attack_start_y + interval_y * index_y
            self.adb.touch([enchantment_attack_x, enchantment_attack_y])
            # be ready for fighting
            self.sleep(15)

            self.touchReadyBtn()
            self.sleep(100)
            self.endTheFightAndSleep()

            if enchantment_index % 3 == 2:
                self.touchPangwawa()

    def touchByPercent(self, coordinatePercentage):
        coordinate = [self.device_x * coordinatePercentage[0], self.device_y * coordinatePercentage[1]]
        self.adb.touch(coordinate)

    def touchReadyBtn(self):
        ready_btn_coordinate = [2340, 1100]
        self.adb.touch(ready_btn_coordinate)

    def endTheFightAndSleep(self):
        finish_coordinate = [1300, 750]
        self.adb.touch(finish_coordinate)
        self.sleep(10)  # wait for showing the pangwawa
        self.touchPangwawa()

    def touchPangwawa(self):
        finish_coordinate = [1300, 750]
        self.adb.touch(finish_coordinate)
        self.sleep(10)  # gifts come from the pangwawa
        self.adb.touch(finish_coordinate)
        self.sleep(15)  # quit the fight scenario

    def sleep(self, seconds, msg=""):
        if msg is not None and msg != "":
            print("sleep for " + msg)
        print("sleep : " + str(seconds))
        time.sleep(seconds)

class Adb:
    def __init__(self, device=""):
        self.device = device
        if self.device == "" or self.device == None:
            self.cmdPrefix = "adb"
        else:
            self.cmdPrefix = "adb -s %s" % self.device

    def touch(self, coordinate):
        print("adb : touch %d,%d" % (coordinate[0], coordinate[1]))
        cmd = "%s shell input tap %d %d" % (self.cmdPrefix, coordinate[0], coordinate[1])
        os.system(cmd)

    def getResolution(self):
        print("adb : get resolution")
        pattern = re.compile(r'.* (\d+)x(\d+).*')
        cmd = "%s shell wm size" % self.cmdPrefix
        proc = os.popen(cmd)
        output = ''.join(proc.readlines())
        proc.close()
        rematch = pattern.match(output)
        if rematch is not None:
            resolution = [int(rematch.group(1)), int(rematch.group(2))]
            print("adb : resolution is %dx%d" % (resolution[0], resolution[1]))
            return resolution
        else:
            print("adb : get reslution failed!\noutput is %s" % output)
            exit()

def fight_for_material():
    for i in range(0, 100):
        print("------ game : " + str(i + 1) + "------")
        YyHelper().startFightForMaterial()

def fight_for_enchantment():
    YyHelper().startFightForEnchantment()

def usage():
    print("""
          usage: python YyHelper.py [mode]

          Augument `mode` is optional, default is `--material`.

          Available mode:

          -m | --material      Yuhun or Juexing Materials
          -s | --skill         Fighting skills
          -g | --group         Fight for materials with group
          -c | --chapter       Fight for chapters
          """)

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "msgc", ["material", "skill", "group", "chapter"])
    except getopt.GetoptError as err:
        opts = []

    if len(opts) == 0:
        usage()
        opts = [('-m', '')]

    yyhelper = YyHelper()

    for o, a in opts:
        if o in ("-m", "--material"):
            print("start fight for materials endless")
            yyhelper.fightForMaterialEndless()
        elif o in ("-s", "--skill"):
            print("start fighting skills")
            yyhelper.fightingSkills()
        elif o in ("-g", "--group"):
            print("start fight for materials with group")
            yyhelper.fightWithGroup()
        elif o in ("-c", "--chapter"):
            print("start fight for chapters")
            yyhelper.fightForChapterEndless()
        break

if __name__ == '__main__':
    main()
