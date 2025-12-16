import numpy as np
import os
import sys
import random


class ReversiGame:
    """黑白棋遊戲"""
    
    def __init__(self, board_size=8):
        """初始化遊戲"""
        self.board_size = board_size
        self.reset_game()
        
    def reset_game(self):
        """重置遊戲狀態"""
        # 初始化空棋盤 (0:空, 1:黑棋, 2:白棋)
        self.board = np.zeros((self.board_size, self.board_size), dtype=int)
        
        # 設置初始棋子位置
        mid = self.board_size // 2
        self.board[mid-1][mid-1] = 2  # 白棋
        self.board[mid-1][mid] = 1    # 黑棋
        self.board[mid][mid-1] = 1    # 黑棋
        self.board[mid][mid] = 2      # 白棋
        
        self.current_player = 1  # 黑棋先行 (1:黑棋, 2:白棋)
        self.game_over = False
        self.winner = None
        self.move_count = 0
    
    def print_board(self):
        """列印棋盤到控制台"""
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print("\n" + "=" * 50)
        print("             黑白棋")
        print("=" * 50)
        
        # 列印列號
        print("   ", end="")
        for col in range(self.board_size):
            print(f" {col}  ", end="")
        print()
        
        # 列印分隔線
        print("  +" + "---+" * self.board_size)
        
        # 列印棋盤內容
        for row in range(self.board_size):
            print(f"{row} |", end="")
            for col in range(self.board_size):
                cell = self.board[row][col]
                if cell == 0:
                    print("   |", end="")
                elif cell == 1:
                    print(" ● |", end="")  # 黑棋
                else:
                    print(" ○ |", end="")  # 白棋
            print("\n  +" + "---+" * self.board_size)
        
        # 顯示遊戲信息
        black_count, white_count = self.count_pieces()
        print(f"\n當前玩家: {'黑棋(●)' if self.current_player == 1 else '白棋(○)'}")
        print(f"黑棋(●): {black_count}  白棋(○): {white_count}")
        
        # 遊戲結束時顯示結果
        if self.game_over:
            print("\n" + "=" * 50)
            if self.winner == 1:
                print("            🎉 黑棋(●) 獲勝! 🎉")
            elif self.winner == 2:
                print("            🎉 白棋(○) 獲勝! 🎉")
            else:
                print("                🤝 平局! 🤝")
            print("=" * 50)
    
    def is_valid_move(self, row, col, player):
        """檢查移動是否有效"""
        if not (0 <= row < self.board_size and 0 <= col < self.board_size):
            return False
            
        if self.board[row][col] != 0:  # 該位置已有棋子
            return False
        
        opponent = 3 - player  # 對手的棋子顏色 (1->2, 2->1)
        directions = [(-1, -1), (-1, 0), (-1, 1),
                      (0, -1),           (0, 1),
                      (1, -1),  (1, 0),  (1, 1)]
        
        for dr, dc in directions:
            r, c = row + dr, col + dc
            if 0 <= r < self.board_size and 0 <= c < self.board_size and self.board[r, c] == opponent:
                # 繼續沿這個方向檢查
                r += dr
                c += dc
                while 0 <= r < self.board_size and 0 <= c < self.board_size and self.board[r, c] == opponent:
                    r += dr
                    c += dc
                if 0 <= r < self.board_size and 0 <= c < self.board_size and self.board[r, c] == player:
                    return True
        return False
    
    def get_all_valid_moves(self, player):
        """獲取指定玩家的所有合法移動"""
        valid_moves = []
        for row in range(self.board_size):
            for col in range(self.board_size):
                if self.is_valid_move(row, col, player):
                    valid_moves.append((row, col))
        return valid_moves
    
    def make_move(self, row, col, player):
        """執行移動並翻轉棋子"""
        if not self.is_valid_move(row, col, player):
            return False
        
        # 放置棋子
        self.board[row][col] = player
        opponent = 3 - player
        directions = [(-1, -1), (-1, 0), (-1, 1),
                      (0, -1),           (0, 1),
                      (1, -1),  (1, 0),  (1, 1)]
        
        # 翻轉棋子
        for dr, dc in directions:
            r, c = row + dr, col + dc
            if 0 <= r < self.board_size and 0 <= c < self.board_size and self.board[r, c] == opponent:
                # 繼續沿這個方向檢查
                r += dr
                c += dc
                while 0 <= r < self.board_size and 0 <= c < self.board_size and self.board[r, c] == opponent:
                    r += dr
                    c += dc
                if 0 <= r < self.board_size and 0 <= c < self.board_size and self.board[r, c] == player:
                    # 翻轉棋子
                    r, c = row + dr, col + dc
                    while 0 <= r < self.board_size and 0 <= c < self.board_size and self.board[r, c] == opponent:
                        self.board[r, c] = player
                        r += dr
                        c += dc
        
        self.move_count += 1
        return True
    
    def count_pieces(self):
        """計算雙方棋子數量"""
        black_count = np.sum(self.board == 1)
        white_count = np.sum(self.board == 2)
        return black_count, white_count
    
    def switch_player(self):
        """切換玩家"""
        self.current_player = 3 - self.current_player
        
        # 檢查新玩家是否有合法移動
        if not self.get_all_valid_moves(self.current_player):
            # 跳過回合，切換回原玩家
            self.current_player = 3 - self.current_player
            
            # 如果原玩家也沒有合法移動，遊戲結束
            if not self.get_all_valid_moves(self.current_player):
                self.check_game_over()
                return False
        return True
    
    def check_game_over(self):
        """檢查遊戲是否結束"""
        # 檢查雙方是否都有合法移動
        black_moves = self.get_all_valid_moves(1)
        white_moves = self.get_all_valid_moves(2)
        
        if not black_moves and not white_moves:
            self.game_over = True
            
            # 判斷勝負
            black_count, white_count = self.count_pieces()
            if black_count > white_count:
                self.winner = 1
            elif white_count > black_count:
                self.winner = 2
            else:
                self.winner = 0  # 平局
            return True
        return False


class SimpleComputer:
    """隨機選擇合法移動"""
    
    def get_move(self, game, player):
        """隨機選擇一個合法移動"""
        valid_moves = game.get_all_valid_moves(player)
        
        if not valid_moves:
            return None
        
        # 隨機選擇一個合法移動
        return random.choice(valid_moves)


def print_menu():
    """顯示主選單"""
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\n" + "=" * 50)
    print("             黑白棋主選單")
    print("=" * 50)
    print(" 1. 開始遊戲 (玩家 vs 電腦)")
    print(" 2. 遊戲規則")
    print(" 3. 離開遊戲")
    print("=" * 50)


def print_rules():
    """顯示遊戲規則"""
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\n" + "=" * 50)
    print("             遊戲規則")
    print("=" * 50)
    print("遊戲目標:")
    print("  在遊戲結束時擁有更多己方顏色的棋子")
    print()
    print("基本規則:")
    print("  1. 黑棋(●)先行，玩家控制黑棋")
    print("  2. 白棋(○)由電腦控制")
    print("  3. 棋子必須放在空位上")
    print("  4. 棋子必須夾住對手的棋子")
    print("  5. 被夾住的對手棋子會翻轉成己方顏色")
    print("  6. 如果沒有合法移動，則跳過回合")
    print("  7. 當雙方都沒有合法移動時，遊戲結束")
    print("  8. 遊戲結束時，棋子多的一方獲勝")
    print()
    print("操作方法:")
    print("  輸入座標格式: 行,列 或 行 列")
    print("  例如: 3,4 或 3 4")
    print("=" * 50)
    input("\n按 Enter 鍵返回主選單...")


def play_game():
    """遊戲主循環"""
    game = ReversiGame()
    computer = SimpleComputer()
    
    while not game.game_over:
        game.print_board()
        
        # 檢查當前玩家是否有合法移動
        valid_moves = game.get_all_valid_moves(game.current_player)
        if not valid_moves:
            print(f"\n{'黑棋(●)' if game.current_player == 1 else '白棋(○)'} 沒有合法移動，跳過回合。")
            if not game.switch_player():
                break
            input("\n按 Enter 鍵繼續...")
            continue
        
        # 電腦的回合 (白棋)
        if game.current_player == 2:
            print("\n電腦正在思考中...")
            move = computer.get_move(game, 2)
            if move:
                game.make_move(move[0], move[1], 2)
                print(f"電腦選擇位置: ({move[0]}, {move[1]})")
                game.check_game_over()
                game.switch_player()
            input("\n按 Enter 鍵繼續...")
            continue
        
        # 玩家的回合 (黑棋)
        print("\n輸入格式: 行,列 或 行 列")
        print("例如: 3,4 或 3 4")
        
        while True:
            try:
                command = input(f"\n黑棋(●)的回合，請輸入座標: ").strip()
                
                # 嘗試解析座標
                if ',' in command:
                    row, col = map(int, command.split(','))
                else:
                    row, col = map(int, command.split())
                
                # 執行移動
                if game.make_move(row, col, 1):
                    game.check_game_over()
                    game.switch_player()
                    break
                else:
                    print("無效移動! 請選擇合法位置。")
                    
            except ValueError:
                print("無效輸入! 請使用格式: 行,列 或 行 列")
            except KeyboardInterrupt:
                print("\n遊戲中斷")
                return 'menu'
    
    # 遊戲結束
    game.print_board()
    input("\n按 Enter 鍵返回主選單...")
    return 'menu'


def main():
    """主函數"""
    print("黑白棋遊戲啟動中...")
    input("\n按 Enter 鍵開始遊戲...")
    
    while True:
        print_menu()
        
        try:
            choice = input("\n請選擇選項 (1-3): ").strip()
            
            if choice == '1':  # 開始遊戲
                play_game()
                
            elif choice == '2':  # 遊戲規則
                print_rules()
                
            elif choice == '3':  # 退出遊戲
                print("\n感謝遊玩黑白棋! 再見!")
                sys.exit(0)
                
            else:
                print("請輸入有效的選項 (1-3)")
                input("按 Enter 鍵繼續...")
                
        except KeyboardInterrupt:
            print("\n\n遊戲結束")
            sys.exit(0)
        except Exception as e:
            print(f"發生錯誤: {e}")
            input("按 Enter 鍵繼續...")


if __name__ == "__main__":
    main()