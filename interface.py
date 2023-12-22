import flet as ft

async def main(page:ft.Page):
    page.title = 'LAND пароли'
    page.horizontal_alignment=ft.CrossAxisAlignment.CENTER,

    main_col = ft.Column()

    c1 = ft.Checkbox(label="Цифры",value=True)
    c2 = ft.Checkbox(label="Заглавные буквы")
    c3 = ft.Checkbox(label="Строчные буквы")
    c4 = ft.Checkbox(label="Спец. символы ( # @ {] & ^ )")

    col = ft.Column(
        [c1,c2,c3,c4],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        alignment=ft.MainAxisAlignment.START,
    )
    
    tb5 = ft.TextField(label="Диапозон паролей (1, 2, 3, 4 или '2-4')", icon=ft.icons.LOCK,expand=True)

    row = ft.Row([tb5])

    main_col.controls.append(ft.Row([ft.Icon(name=ft.icons.SETTINGS),ft.Text('Настройки',size=20)]))
    main_col.controls.append(col)
    main_col.controls.append(ft.Divider())
    main_col.controls.append(row)
    container_main_col = ft.Container(content=main_col,bgcolor='grey900',width=page.width-20,padding=20,border_radius=20)
    await page.add_async(container_main_col)

async def view():
    await ft.app_async(main)

