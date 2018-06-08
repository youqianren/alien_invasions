import pygame.font

class Button():
    """按钮的类"""
    def __init__(self, ai_settings, screen, msg):
        self.screen = screen
        self.screen_rect = self.screen.get_rect()
        # 创建按钮尺寸颜色
        self.width, self.height = 200, 50
        self.button_color = (0, 255, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)
        # 获得rect属性
        self.rect = pygame.Rect(0, 0, self.width, self.height)


        # 给play按钮赋予初始位置
        self.rect.center = self.screen_rect.center

        self.prep_msg(msg)

    def prep_msg(self, msg):
        """将文字渲染成图像，并使其在按钮上居中"""
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()

        self.msg_image_rect.center = self.rect.center

    def draw_buttom(self):
        """绘制一个用颜色填充的按钮，再绘制文本"""
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)


