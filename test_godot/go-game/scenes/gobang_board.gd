extends TextureRect

# 棋盘设置（同之前）
@export var board_size: int = 15
@export var cell_size: int = 40
@export var line_color: Color = Color(0, 0, 0)
@export var star_point_color: Color = Color(0, 0, 0)
@export var star_point_radius: int = 4

# 棋子设置
@export var stone_radius: int = 16  # 棋子半径
var stone_color_black: Color = Color(0, 0, 0)  # 黑子
var stone_color_white: Color = Color(1, 1, 1)  # 白子

var board_margin: int = 40
var current_player: int = 1  # 1=黑子, 2=白子
var board_state: Array = []  # 存储棋盘状态：0=空, 1=黑, 2=白
var move_history: Array = []  # 存储落子历史，元素为 Vector2i(col, row)
var game_over: bool = false  # 游戏是否结束

@onready var win_panel = $"../WinPanel"
@onready var current_player_label = $CurrentPlayerLabel

func _ready():
	# 初始化棋盘状态数组
	_reset_game()
	# 连接 GameControlPanel 的自定义信号
	var control_panel = $"../GameControlPanel"
	control_panel.connect("restart_requested", _on_restart_requested)
	control_panel.connect("undo_requested", _on_undo_requested)
	# 设置结果对话框
	win_panel.connect("restart_requested", _on_restart_requested)
	win_panel.hide()
	#
	_update_player_label()
	
	# 更新玩家标识
func _update_player_label():
	var player_text = "当前玩家: "
	if current_player == 1:
		player_text += "黑子"
	else:
		player_text += "白子"
	current_player_label.text = player_text

#func _input(event: InputEvent) -> void:
	#_on_gui_input(event)
	#if event is InputEventMouseButton:
		#if event.pressed:
			#match event.button_index:
				#MOUSE_BUTTON_LEFT:
					#print("左键点击")
				#MOUSE_BUTTON_RIGHT:
					#print("右键点击")
				#MOUSE_BUTTON_MIDDLE:
					#print("中键点击")
				#MOUSE_BUTTON_WHEEL_UP:
					#print("滚轮向上")
				#MOUSE_BUTTON_WHEEL_DOWN:
					#print("滚轮向下")

# 绘制棋盘和棋子
func _draw():
	# 应用边距偏移
	draw_set_transform_matrix(Transform2D.IDENTITY.translated(Vector2(board_margin, board_margin)))
	# 绘制棋盘网格和星位（同之前）
	var board_width = (board_size - 1) * cell_size
	var board_height = (board_size - 1) * cell_size
	draw_set_transform_matrix(Transform2D(0, Vector2(board_margin, board_margin)))
	# 绘制网格线
	for i in range(board_size):
		draw_line(Vector2(0, i * cell_size), Vector2(board_width, i * cell_size), line_color, 1)
		draw_line(Vector2(i * cell_size, 0), Vector2(i * cell_size, board_height), line_color, 1)
	# 绘制星位
	_draw_star_point(7, 7)  # 天元
	for pos in [[3,3], [3,11], [11,3], [11,11]]:  # 角星位
		_draw_star_point(pos[0], pos[1])
	# 绘制棋子
	for y in range(board_size):
		for x in range(board_size):
			var stone = board_state[y][x]
			if stone != 0:
				var color = stone_color_black if stone == 1 else stone_color_white
				var pos = Vector2(x * cell_size, y * cell_size)
				draw_circle(pos, stone_radius, color)
				# 添加棋子阴影效果
				draw_circle(pos + Vector2(2, 2), stone_radius, Color(0, 0, 0, 0.2))

# 绘制星位
func _draw_star_point(col: int, row: int):
	var center = Vector2(col * cell_size, row * cell_size)
	draw_circle(center, star_point_radius, star_point_color)

# 处理输入相关的事件
func _gui_input(event):
	if game_over:
		return  # 游戏结束后禁止任何操作
	if event is InputEventMouseButton and event.pressed and event.button_index == MOUSE_BUTTON_LEFT:
		var click_pos = event.position
		var grid_pos = get_nearest_point(click_pos)
		var col = grid_pos.x
		var row = grid_pos.y
		#print(row, col)
		# 检查该位置是否已有棋子
		if board_state[row][col] == 0:
			# 放置棋子
			board_state[row][col] = current_player
			# 记录这步棋
			move_history.append(Vector2i(col, row))
			# 检查胜负
			if check_win(col, row, current_player):
				print("Player %s wins!" % current_player)
				game_over = true
				# 这里可以弹出胜利提示框
				_on_game_over(current_player)
			# 切换玩家
			current_player = 3 - current_player  # 1→2, 2→1
			_update_player_label()
			# 重绘棋盘
			queue_redraw()

# 获取点击事件最近的位点
func get_nearest_point(screen_pos: Vector2) -> Vector2i:
	var local_pos = screen_pos - Vector2(board_margin, board_margin)
	var col = round(local_pos.x / cell_size)
	var row = round(local_pos.y / cell_size)
	col = clamp(col, 0, board_size - 1)
	row = clamp(row, 0, board_size - 1)
	return Vector2i(col, row)

# 检查胜负情况
func check_win(col: int, row: int, player: int) -> bool:
	# 检查四个方向：横、竖、正斜、反斜
	var directions = [
		Vector2i(1, 0),   # 横
		Vector2i(0, 1),   # 竖
		Vector2i(1, 1),   # 正斜
		Vector2i(1, -1)   # 反斜
	]
	for dir in directions:
		var count = 1  # 包含当前棋子
		# 正方向计数
		var p = Vector2i(col + dir.x, row + dir.y)
		while p.x >= 0 && p.x < board_size && p.y >= 0 && p.y < board_size && board_state[p.y][p.x] == player:
			count += 1
			p += dir
		# 反方向计数
		p = Vector2i(col - dir.x, row - dir.y)
		while p.x >= 0 && p.x < board_size && p.y >= 0 && p.y < board_size && board_state[p.y][p.x] == player:
			count += 1
			p -= dir
		# 如果连成5子则胜利
		if count >= 5:
			return true
	return false

# 响应游戏结束事件
func _on_game_over(winner: int):
	game_over = true
	win_panel.show_win(winner)  # 显示胜利提示框
	
# 响应重新开始信号
func _on_restart_requested():
	_reset_game()
	win_panel.hide()
	print("GobangBoard: 游戏已重置")

# 响应悔棋信号
func _on_undo_requested():
	if game_over:
		return
	if move_history.size() > 0:
		var last_move = move_history.pop_back()
		var col = last_move.x
		var row = last_move.y
		board_state[row][col] = 0
		current_player = 3 - current_player
		queue_redraw()
		game_over = false  # 悔棋后，游戏状态变为未结束
		print("GobangBoard: 悔棋成功")
		

# 重置游戏的函数
func _reset_game():
	# 重新初始化棋盘状态
	board_state = []
	for y in range(board_size):
		var row = []
		for x in range(board_size):
			row.append(0)
		board_state.append(row)
	# 清空落子历史
	move_history = []
	# 重置当前玩家
	current_player = 1
	# 重置游戏结束标志
	game_over = false
	# 重绘棋盘
	queue_redraw()
