extends Control

# 定义两个自定义信号
signal restart_requested  # 当点击“重新开始”按钮时发出
signal undo_requested     # 当点击“悔棋”按钮时发出

@onready var restart_button = $"VBoxContainer/RestartButton"
@onready var undo_button = $"VBoxContainer/UndoButton"

func _ready():
	# 连接按钮的 pressed 信号到本脚本的私有函数
	restart_button.connect("pressed", _on_restart_button_pressed)
	undo_button.connect("pressed", _on_undo_button_pressed)

# “重新开始”按钮被点击
func _on_restart_button_pressed():
	# 发出我们自己的信号
	emit_signal("restart_requested")
	print("GameControlPanel: restart_requested 信号已发出")

# “悔棋”按钮被点击
func _on_undo_button_pressed():
	# 发出我们自己的信号
	emit_signal("undo_requested")
	print("GameControlPanel: undo_requested 信号已发出")
