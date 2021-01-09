import game_compiler


filename = 'original_data/poker_now_log_4gcAQTnotvBq87RCX1oHXKvhM.csv'
data = game_compiler.Game_Compiler(filename)
print(data.raw_log())
data.read_log()