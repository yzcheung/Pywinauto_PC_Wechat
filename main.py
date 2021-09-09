# coding='utf-8'

from time import sleep
from pywinauto.application import Application
from pywinauto import mouse
from psutil import process_iter
from pyautogui import hotkey
from pyperclip import copy


class WeiXin(object):

    def __init__(self):
        self.app = Application(backend='uia')
        self.pid = self.__get_pid()
        self.app.connect(process=self.pid)
        self.weixin_pc_window = self.app.window(
            class_name="WeChatMainWndForPC")
        self.weixin_pc_window.set_focus()
        self.weixin_pc_window.draw_outline(colour='green')
        # print(self.weixin_pc_window.dump_tree())

    def __get_pid(self):
        PID = process_iter()
        name = ''
        pid_num = 0
        for pid_temp in PID:
            pid_dic = pid_temp.as_dict(attrs=['pid', 'name'])
            if pid_dic['name'] == 'WeChat.exe':
                name = pid_dic['name']
                pid_num = pid_dic['pid']
                break
        if name == 'WeChat.exe':
            return pid_num
        else:
            return False

    def __get_element_postion(self, element):
        """获取元素的中心点位置"""
        # 元素坐标
        element_position = element.rectangle()
        # 计算中心点位置
        center_position = (int((element_position.left + element_position.right) / 2),
                           int((element_position.top + element_position.bottom) / 2))
        return center_position

    def start_chat(self):
        chat_list_element = self.weixin_pc_window.child_window(
            title="聊天", control_type="Button")
        mouse.click(button='left', coords=self.__get_element_postion(
            chat_list_element))

    def get_users(self):
        user_list = []
        try:
            chat_list = self.weixin_pc_window.child_window(
                control_type='List', title='会话')
            mouse.click(button='left',
                        coords=self.__get_element_postion(chat_list))
            users = chat_list.children()
            for user in users:
                user_list.append(user.window_text())
        except:
            pass
        return user_list

    def find_user(self, user: str):
        user_element = self.weixin_pc_window.child_window(
            title=user, control_type='Text')
        mouse.click(button='left',
                    coords=self.__get_element_postion(user_element))
        sleep(0.3)

    def search_user(self, user_name: str):
        search = self.weixin_pc_window.child_window(
            title="搜索", control_type='Edit')
        mouse.click(button='left', coords=self.__get_element_postion(search))
        sleep(0.1)
        self.weixin_pc_window.type_keys(user_name)
        sleep(0.6)
        self.weixin_pc_window.type_keys('{ENTER}')

    def send_msg(self, texts: str = ""):
        edit_element = self.weixin_pc_window.child_window(
            title=r"输入", control_type="Edit")
        for text in texts.split('\n'):
            if text.isalnum():
                copy(text.strip())
                hotkey('ctrl', 'v')
            else:
                edit_element.type_keys(text)
            sleep(1)
            hotkey('ctrl', 'enter')
        hotkey('enter')

    def teardown(self):
        self.app.kill()


if __name__ == '__main__':
    weixin = WeiXin()
    weixin.start_chat()
    weixin.search_user('文件传输助手')
    weixin.send_msg('测试消息')
