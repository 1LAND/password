import flet as ft

import pyautogui as pg
import pyperclip as pc

class Frame(ft.UserControl):
    def __init__(self,page:ft.Page,obj:list=None,label_text="",label_icon=ft.icons.CIRCLE_OUTLINED):
        super().__init__()
        self.page = page 
        self.obj = obj
        self.label_text = label_text
        self.label_icon = label_icon
    def build(self):
        return ft.Container(
            content=ft.Column(
                [
                    ft.Row([ft.Icon(name=self.label_icon),ft.Text(self.label_text,size=20)]),
                    *self.obj
                ],
                ),
            bgcolor='grey900',
            width=self.page.width-20,
            padding=20,
            border_radius=20
        )

class PasswordSetting(ft.UserControl):
    def __init__(self,page):
        super().__init__()
        self.page:ft.Page = page

        self.c1 = ft.Checkbox(label="Цифры",value=True,on_change=self.change_checkbox,disabled=True)
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
                    await c.update_async()
        else:
            for c in (self.c1,self.c2,self.c3,self.c4):
                c.disabled = False
                await c.update_async()
        await self.page.update_async()

    def build(self):
        return Frame(self.page,
        [
            ft.Column(
                [self.c1,self.c2,self.c3,self.c4],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.START,
            ),
            ft.Divider(),
            ft.Row([self.input_password_range])
        ],
        label_icon=ft.icons.SETTINGS,
        label_text='Настройки пароля')

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
        return Frame(self.page,
                obj=[
                    ft.Text("   *Нажмите: CTRL + P - чтобы выбрать точки",size=15,font_family="RobotoSlab"),
                    ft.Divider(),
                    ft.TextField(ref=self.pos1,label="Текстовое поле для пароля",),
                    ft.TextField(ref=self.pos2,label="Кнопка для провеки",),
                ],
                label_icon=ft.icons.CONTROL_POINT,
                label_text='Настройки точек'
            )

class SearchPassword(ft.UserControl):
    def __init__(self,page:ft.Page,position_setting:PositonSetting,password_setting:PasswordSetting):
        super().__init__()
        self.page = page
        
        self.status_search = False

        self.position_setting = position_setting
        self.password_setting = password_setting

        self.btn_main = ft.FloatingActionButton(
            content=ft.Row(
                [ft.Text("Поиск")], alignment="center", spacing=5
            ),
            width=500,
            shape=ft.RoundedRectangleBorder(radius=5),
            on_click=self.search_password
        )
        self.text_above_pb = ft.Text('Поиск...')
        self.pb = ft.ProgressBar(width=500)
        self.col_pb = ft.Column([self.pb])
    async def search_password(self,e):
        self.password_setting.input_password_range.error_text = None
        self.position_setting.pos1.current.error_text = None
        self.position_setting.pos2.current.error_text = None
        if self.password_setting.input_password_range.value.strip() == '':
            self.password_setting.input_password_range.error_text = 'Обязательно для заполнения'
            await self.password_setting.input_password_range.update_async()
        elif self.position_setting.pos1.current.value.strip() == '':
            self.position_setting.pos1.current.error_text = 'Обязательно для заполнения'
            await self.position_setting.pos1.current.update_async()
        elif self.position_setting.pos2.current.value.strip() == '':
            self.position_setting.pos2.current.error_text = 'Обязательно для заполнения'
            await self.position_setting.pos2.current.update_async()
        else:
            self.status_search = False if self.status_search else True
            if self.status_search:
                self.pb.value = 0
                self.col_pb.controls.insert(0,self.text_above_pb)
                await self.col_pb.update_async()
                await self.pb.update_async()
            else:
                self.pb.value = None
                self.col_pb.controls.remove(self.text_above_pb)
                await self.col_pb.update_async()
                await self.pb.update_async()

            self.position_setting.pos1.current.disabled = False if self.position_setting.pos1.current.disabled else True
            self.position_setting.pos2.current.disabled = False if self.position_setting.pos2.current.disabled else True

            self.password_setting.c1.disabled = False if self.password_setting.c1.disabled else True 
            self.password_setting.c2.disabled = False if self.password_setting.c2.disabled else True 
            self.password_setting.c3.disabled = False if self.password_setting.c3.disabled else True 
            self.password_setting.c4.disabled = False if self.password_setting.c4.disabled else True 
            await self.password_setting.c1.update_async() 
            await self.password_setting.c2.update_async()
            await self.password_setting.c3.update_async()
            await self.password_setting.c4.update_async()
            self.password_setting.input_password_range.disabled = False if self.password_setting.input_password_range.disabled else True
        
        await self.position_setting.pos1.current.update_async()
        await self.position_setting.pos2.current.update_async()
        await self.password_setting.input_password_range.update_async()
    def build(self):
        return Frame(self.page,
            obj=[
                ft.Column(
                    [self.btn_main,self.col_pb]
                    ),
            ],
            label_text='Поиск пароля',
            label_icon=ft.icons.SEARCH)
async def main(page:ft.Page):
   
    page.window_height = 850
    page.window_width = 500
    page.window_resizable = False
    page.title = 'LAND пароли'
    page.horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    page.scroll = True
    pasword_s = PasswordSetting(page)
    position_s = PositonSetting(page)
    main_btn =  SearchPassword(page,position_s,pasword_s)
    await page.add_async(main_btn)
    await page.add_async(pasword_s,position_s)

async def view():
    await ft.app_async(main)

