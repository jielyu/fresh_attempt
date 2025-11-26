# WinPanel.gd
extends Control

@onready var label = $VBoxContainer/Label
@onready var button = $VBoxContainer/Button

# 定义信号
signal restart_requested()  # 点击"确定"后发出信号

func _ready() -> void:
	button.connect("pressed", _on_button_pressed)

func show_win(player: int):
	var player_text = "黑子" if player == 1 else "白子"
	label.text = "Player %s Wins!" % player_text
	show()
	button.grab_focus()

func _on_button_pressed():
	hide()
	emit_signal("restart_requested")  # 发出信号通知主节点
