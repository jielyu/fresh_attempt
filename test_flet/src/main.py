import flet as ft


def main(page: ft.Page):
    page.title = "macOS 菜单示例"

    # 创建菜单项
    def on_menu_click(e):
        print(f"点击了: {e.control.text}")

    def window_event(e):
        if e.data == "close":
            page.open(confirm_dialog)
            page.update()

    page.window.prevent_close = True
    page.window.on_event = window_event

    def yes_click(e):
        page.window.destroy()

    def no_click(e):
        page.close(confirm_dialog)
        page.update()

    confirm_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("确认"),
        content=ft.Text("你确实想要退出吗?"),
        actions=[
            ft.ElevatedButton("Yes", on_click=yes_click),
            ft.OutlinedButton("No", on_click=no_click),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    menu_items = [
        ft.PopupMenuItem(text="新建", on_click=on_menu_click),
        ft.PopupMenuItem(text="打开", on_click=on_menu_click),
        ft.PopupMenuItem(),  # 分隔线
        ft.PopupMenuItem(text="退出", on_click=lambda _: page.window.close()),
    ]

    # 设置应用栏
    page.appbar = ft.AppBar(
        title=ft.Text("我的应用"), actions=[ft.PopupMenuButton(items=menu_items)]
    )

    page.add(ft.Text("主内容区域"))


ft.app(main)
