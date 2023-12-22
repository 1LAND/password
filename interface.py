import flet as ft

import pyautogui as pg
import pyperclip as pc

class PasswordSetting(ft.UserControl):
    def __init__(self,page):
        super().__init__()
        self.page:ft.Page = page

        self.c1 = ft.Checkbox(label="Цифры",value=True,on_change=self.change_checkbox)
        self.c2 = ft.Checkbox(label="Заглавные буквы",on_change=self.change_checkbox)
        self.c3 = ft.Checkbox(label="Строчные буквы",on_change=self.change_checkbox)
        self.c4 = ft.Checkbox(label="Спец. символы ( # @ {] & ^ )",on_change=self.change_checkbox)

        self.input_password_range = ft.TextField(label="Диапозон паролей (1, 2, 3, 4 или '2-4')", icon=ft.icons.LOCK,expand=True)
    
    def get_setting_value(self):
        return self.input_password_range.value,self.c1.value,self.c2.value,self.c3.value,self.c4.value

    async def change_checkbox(self,e):
        if (self.c1.value + self.c2.value + self.c3.value + self.c4.value) == 1:
            for c in (self.c1,self.c2, self.c3, self.c4):
                if c.value == True:
                    c.disabled = True
        else:
            for c in (self.c1,self.c2,self.c3,self.c4):
                c.disabled = False
        await self.page.update_async()

    def build(self):
        return ft.Container(
            content=ft.Column(
                [
                    ft.Row([ft.Icon(name=ft.icons.SETTINGS),ft.Text('Настройки пароля',size=20)]),
                    ft.Column(
                        [self.c1,self.c2,self.c3,self.c4],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        alignment=ft.MainAxisAlignment.START,
                    ),
                    ft.Divider(),
                    ft.Row([self.input_password_range])
                ]
            ),
            bgcolor='grey900',
            width=self.page.width-20,
            padding=20,
            border_radius=20
        )

class PositonSetting(ft.UserControl):
    def __init__(self,page):
        super().__init__()
        self.page:ft.Page = page

        self.page.fonts = {
            "RobotoSlab": "https://github.com/google/fonts/raw/main/apache/robotoslab/RobotoSlab%5Bwght%5D.ttf"
        }

        self.pos1 = ft.Ref[ft.TextField]()
        self.pos2 = ft.Ref[ft.TextField]()
        self.pos = (0,0)

        self.page.on_keyboard_event = self.on_keyboard

        self.banner = ft.Banner(
            bgcolor="blue400",
            leading=ft.Icon(ft.icons.INFO, color="blue700", size=40),
            content=ft.Text(F"Выбрана точка: {self.pos}"),
            actions=[
                    ft.TextButton("Закрыть", on_click=self.close_banner),
                    ],
                )
        self.page.banner = self.banner
    async def open_banner(self,e):
        self.page.banner.open = True
        await self.page.update_async()            
    async def close_banner(self,e):
        self.page.banner.open = False
        await self.page.update_async()
    async def on_keyboard(self,e: ft.KeyboardEvent):
        if e.ctrl and e.key == 'P':
            x,y = pg.position()
            self.pos = (x,y)
            pc.copy(str(self.pos))
            self.banner.content.value = F"Выбрана точка: {self.pos}"
            await self.banner.update_async()
            await self.open_banner(e)
    def get_positions(self):
        return self.pos1.value,self.pos2.value

    def build(self):
        return ft.Container(
            content=ft.Column(
                [
                    ft.Row([ft.Icon(name=ft.icons.CONTROL_POINT),ft.Text('Настройки точек',size=20)]),
                    ft.Text("   *Нажмите: CTRL + P - что бы выбрать точки",size=15,font_family="RobotoSlab"),
                    ft.Divider(),
                    ft.TextField(ref=self.pos1,label="Текстовое поле для пароля",),
                    ft.TextField(ref=self.pos2,label="Кнопка для провеки",),
                    ]
            ),
            bgcolor='grey900',
            width=self.page.width-20,
            padding=20,
            border_radius=20
        )

async def main(page:ft.Page):
   
    page.window_height = 800
    page.window_width = 500
    page.window_resizable = False
    page.title = 'LAND пароли'
    page.horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    page.scroll = True
    pasword_s = PasswordSetting(page)
    position_s = PositonSetting(page)
    main_btn =  ft.FilledTonalButton(text="Filled tonal button")
    await page.add_async(main_btn)
    await page.add_async(pasword_s,position_s)

async def view():
    await ft.app_async(main)

