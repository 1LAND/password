import flet as ft

async def main(page:ft.Page):
    await page.add_async(ft.Text("Hello, async world!"))


async def view():
    await ft.app_async(main)

