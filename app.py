import random

class Player:
    def __init__(self, name, role):
        self.name = name
        self.role = role
        self.is_alive = True
        self.is_protected = False

class Game:
    def __init__(self, num_players):
        self.num_players = num_players
        self.players = []
        self.num_players_alive = num_players

    def start(self):
        self.setup_game()
        self.run_game()

    def setup_game(self):
        roles = ['人狼', '市民', '占い', '騎士','狂人']
        selected_roles = self.select_roles(roles)
        self.assign_roles_to_players(selected_roles)
        self.display_assigned_roles()

    def select_roles(self, roles):
        selected_roles = []
        print("利用可能な役職:", roles)
        while len(selected_roles) < self.num_players:
            role = input("追加したい役職を入力してください: ")
            if role in roles:
                selected_roles.append(role)
            else:
                print("有効な役職を入力してください。")
        random.shuffle(selected_roles)
        return selected_roles

    def assign_roles_to_players(self, selected_roles):
        for i in range(self.num_players):
            player_name = input(f"プレイヤー{i + 1}の名前を入力してください: ")
            player_role = selected_roles[i]
            player = Player(player_name, player_role)
            self.players.append(player)

    def display_assigned_roles(self):
        print("プレイヤーと役職の割り当て結果:")
        for i, player in enumerate(self.players):
            print(f"プレイヤー{i + 1}: {player.name} - {player.role}")

    def run_game(self):
        while True:
            self.daytime_execution()
            if self.check_end_game():
                break
            self.nighttime_actions()
            if self.check_end_game():
                break

    def daytime_execution(self):
        votes = self.collect_votes()
        self.execute_player(votes)

    def collect_votes(self):
        votes = [0] * len(self.players)
        print("昼の処刑タイムです。")
        for player in self.players:
            if player.is_alive:
                self.cast_vote(player, votes)
        return votes

    def cast_vote(self, player, votes):
        while True:
            try:
                vote_index = int(input(f"{player.name}さんの投票したいプレイヤーの番号を入力してください: ")) - 1
                if 0 <= vote_index < len(self.players) and self.players[vote_index].is_alive:
                    votes[vote_index] += 1
                    print(f"{self.players[vote_index].name}に投票しました！")
                    break
                else:
                    print('有効な番号を入力してください。再入力してください。')
            except ValueError:
                print('数字を入力してください。')

    def execute_player(self, votes):
        max_votes = max(votes)
        max_vote_indices = [i for i, vote in enumerate(votes) if vote == max_votes]
        target_player = self.players[random.choice(max_vote_indices)] if len(max_vote_indices) > 1 else self.players[max_vote_indices[0]]
        target_player.is_alive = False
        print(f"{target_player.name}の処刑が行われました")
        self.num_players_alive -= 1

    #役職増やしても人狼は一番最後
    def nighttime_actions(self):
        self.knight_action()
        self.diviner_action()
        self.werewolf_action()

    def knight_action(self):
        knight = self.get_alive_player_by_role('騎士')
        if knight:
            if target_indices:
                self.protect_player(knight)

    def protect_player(self, knight):
        while True:
            try:
                target_index = int(input(f"護衛したいプレイヤーの番号を入力してください（1-{len(self.players)}）: ")) - 1
                if 0 <= target_index < len(self.players) and self.players[target_index].is_alive and self.players[target_index] != knight:
                    target_player = self.players[target_index]
                    target_player.is_protected = True
                    print(f"{target_player.name}は騎士に守られています。")
                    break
                else:
                    print('有効な番号を入力してください。再入力してください。')
            except ValueError:
                print('数字を入力してください。')

    def diviner_action(self):
        diviners = [player for player in self.players if player.role == '占い' and player.is_alive]
        for diviner in diviners:
            print(f"{diviner.name}の占いの行動です。")
            target_indices = [i for i, p in enumerate(self.players) if p.is_alive and p != diviner]
            if target_indices:
                target_index = int(input(f"{diviner.name}さん、占いたいプレイヤーの番号を入力してください（1-{len(self.players)}）: ")) - 1
                target_player = self.players[target_index]
                if target_player.role == '人狼':
                    print(f"{target_player.name}は人狼です！")
                else:
                    print(f"{target_player.name}は人狼ではありません。")

    def divine_player(self, diviner):
        while True:
            try:
                target_index = int(input(f"占いたいプレイヤーの番号を入力してください（1-{len(self.players)}）: ")) - 1
                if 0 <= target_index < len(self.players) and self.players[target_index].is_alive and self.players[target_index] != diviner:
                    target_player = self.players[target_index]
                    if target_player.role == '人狼':
                        print(f"{target_player.name}は人狼です！")
                    else:
                        print(f"{target_player.name}は人狼ではありません。")
                    break
                else:
                    print('有効な番号を入力してください。再入力してください。')
            except ValueError:
                print('数字を入力してください。')

    def werewolf_action(self):
        wolves = [player for player in self.players if player.role == '人狼' and player.is_alive]
        if wolves:
            target_indices = [i for i, p in enumerate(self.players) if p.is_alive and p.role != '人狼']
            if target_indices:
                self.attack_player()

    def attack_player(self):
        while True:
            try:
                target_index = int(input(f"襲撃したいプレイヤーの番号を入力してください（1-{len(self.players)}）: ")) - 1
                if 0 <= target_index < len(self.players) and self.players[target_index].is_alive and self.players[target_index].role != '人狼':
                    target_player = self.players[target_index]
                    if not target_player.is_protected:
                        print(f"{target_player.name}が人狼に襲われました。")
                        target_player.is_alive = False
                        self.num_players_alive -= 1
                    else:
                        print("騎士の護衛が成功し、平和な夜が明けました。")
                    target_player.is_protected = False
                    break
                else:
                    print('有効な番号を入力してください。再入力してください。')
            except ValueError:
                print('数字を入力してください。')


    #役職者の生存確認
    def get_alive_player_by_role(self, role):
        return next((player for player in self.players if player.role == role and player.is_alive), None)

    def check_end_game(self):
        num_werewolves = sum(1 for player in self.players if player.role == '人狼' and player.is_alive)
        num_citizens = sum(1 for player in self.players if player.is_alive and player.role != '人狼')

        if num_werewolves == 0:
            print("市民チームの勝利です！")
            return True
        elif num_werewolves >= num_citizens:
            print("人狼チームの勝利です！")
            return True
        return False

num_players = int(input('プレイ人数を入力してください: '))
game = Game(num_players)
game.start()
