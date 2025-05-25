# encoding: utf-8

import matplotlib
import matplotlib.pyplot as plt
import flet as ft
from flet.matplotlib_chart import MatplotlibChart

matplotlib.use("svg")


def create_app_bar(page: ft.Page):
    """创建AppBar"""
    # 存储窗口原始位置和大小
    original_size = None
    original_position = None

    # 最大化切换回调函数
    def toggle_maximize(e):
        nonlocal original_size, original_position
        if page.window.maximized:
            # 如果已经是最大化状态，则恢复原始大小
            page.window.maximized = False
            if original_size and original_position:
                page.window.width, page.window.height = original_size
                page.window.left, page.window.top = original_position
        else:
            # 保存当前窗口状态
            original_size = (page.window.width, page.window.height)
            original_position = (page.window.left, page.window.top)
            # 最大化窗口
            page.window.maximized = True
        page.update()

    # 菜单项回调函数
    def on_menu_click(e):
        print(f"点击了: {e.control.text}")

    # 窗口事件回调函数
    def window_event(e):
        if e.data == "close":
            page.open(confirm_dialog)
            page.update()

    page.window.prevent_close = True  # 阻止窗口关闭
    page.window.on_event = window_event

    def yes_click(e):
        page.window.destroy()

    def no_click(e):
        page.close(confirm_dialog)
        page.update()

    # 退出确认对话框
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
    # 菜单选项
    menu_items = [
        ft.PopupMenuItem(text="设置", on_click=on_menu_click),
        ft.PopupMenuItem(text="服务", on_click=on_menu_click),
        ft.PopupMenuItem(),  # 分隔线
        ft.PopupMenuItem(text="退出", on_click=lambda _: page.window.close()),
    ]

    return ft.AppBar(
        title=ft.GestureDetector(  # 检测双击事件
            content=ft.Container(
                content=ft.Text(
                    "我的应用", expand=True, text_align=ft.alignment.center
                ),
                expand=True,
                alignment=ft.alignment.center,
            ),
            on_double_tap=toggle_maximize,
            expand=True,
        ),
        center_title=True,
        actions=[ft.PopupMenuButton(items=menu_items, icon=ft.Icons.SETTINGS)],
    )


def main(page: ft.Page):
    page.title = "macOS 菜单示例"
    page.window.title_bar_hidden = True
    # page.window.borderless = True  # 可选，移除所有窗口边框
    page.window.min_width = 1200  # 最小宽度
    page.window.min_height = 720  # 最小高度
    page.window.width = 1200  # 初始宽度
    page.window.height = 720  # 初始高度
    page.window.center()

    # 设置应用栏
    page.appbar = create_app_bar(page)

    page.add(ft.Text("主内容区域"))

    ctls = []

    # MatplotlibChart
    fig, ax = plt.subplots()
    fruits = ["apple", "blueberry", "cherry", "orange"]
    counts = [40, 100, 30, 55]
    bar_labels = ["red", "blue", "_red", "orange"]
    bar_colors = ["tab:red", "tab:blue", "tab:red", "tab:orange"]
    ax.bar(fruits, counts, label=bar_labels, color=bar_colors)
    ax.set_ylabel("fruit supply")
    ax.set_title("Fruit supply by kind and color")
    ax.legend(title="Fruit color")
    ctls.append(MatplotlibChart(fig, expand=True))
    # page.add()

    fig, ax = plt.subplots()
    x = [0, 1, 2, 3, 4, 5]
    y = [100, 20, 60, 70, 10, 120]
    ax.plot(x, y, "-x")
    ctls.append(MatplotlibChart(fig, expand=True))
    # page.add()
    lv = ft.ListView(spacing=10, padding=20, width=1100, auto_scroll=False)
    lv.controls += ctls
    lvc = ft.Container(content=lv, expand=True, alignment=ft.alignment.center)
    c = ft.Row(
        [lvc],
        expand=True,
        vertical_alignment=ft.CrossAxisAlignment.START,
    )
    page.add(ft.Column(controls=[c], expand=True))


if __name__ == "__main__":
    ft.app(main)
