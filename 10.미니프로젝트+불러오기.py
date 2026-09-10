import random


class RankingBoard:

    def __init__(self, rank, rank_level):
        self.rank = rank
        self.rank_level = rank_level

    def add_record(self, id, trial, level):
        if id not in self.rank:
            self.rank[id] = []
            self.rank_level[id] = []

        self.rank[id].append(trial)
        self.rank_level[id].append(level)

    def past_history(self, id):
        print("\n==================================")
        print("과거이력조회")

        if id not in self.rank:
            print(f"{id}님의 게임 기록이 없습니다.")
            return

        print(f"\n===== {id}님의 게임 기록 =====")

        total = 0

        for i in range(len(self.rank[id])):
            print(
                f"{i + 1}번째 기록 : {self.rank[id][i]}회 / {self.rank_level[id][i]}모드"
            )
            total += self.rank[id][i]

        average = total / len(self.rank[id])

        print("----------------------------------")
        print(f"총 게임 횟수 : {len(self.rank[id])}회")
        print(f"평균 기록 : {average:.2f}회")
        print(f"최고 기록 : {min(self.rank[id])}회")
        print("==================================")

    def ranking_view(self):
        print("\n==================================")
        print("랭킹보기")

        if len(self.rank) == 0:
            print("아직 게임 기록이 없습니다.")
            return

        ranking = []

        for id in self.rank:
            best_trial = min(self.rank[id])
            best_index = self.rank[id].index(best_trial)
            best_level = self.rank_level[id][best_index]

            ranking.append((id, best_trial, best_level))

        for i in range(len(ranking)):
            for j in range(i + 1, len(ranking)):
                if ranking[i][1] > ranking[j][1]:
                    temp = ranking[i]
                    ranking[i] = ranking[j]
                    ranking[j] = temp

        for i in range(len(ranking)):
            if i >= 3:
                break

            print(
                f"{i + 1}등 {ranking[i][0]}님 {ranking[i][1]}회 {ranking[i][2]}모드"
            )


class UpDownGame:

    def __init__(self, ranking_board):
        self.ranking_board = ranking_board
        self.id = ""
        self.level = ""
        self.trial = 0
        self.limit = 0
        self.target = 0
        self.max_num = 100
        self.i = 0
        self.count = 0
        self.success = False

    def limit_num(self, level):
        self.level = level

        if self.level == "hard":
            return 10

        if self.level == "expert":
            while True:
                try:
                    self.count = int(
                        input("도전 횟수를 입력해주세요 (1~10회): ")
                    )
                    if 1 <= self.count <= 10:
                        return self.count
                    print("1~10회 이내로 입력해주세요.")
                except ValueError:
                    print("숫자로 입력해주세요.")

    def success_ment(self, id, trial):
        print("\nanswer")
        print(f"{id}님 {trial}번의 시도 만에 성공하셨습니다.")
        print("            축  하  합  니  다")

    def failure_ment(self, id, limit, target):
        print(f"\n{id}님 {limit}번의 시도를 모두 사용하셨습니다.")
        print(f"정답은 {target}였습니다.")
        print("게임에 실패하셨습니다.")

    def up_down_trial(self, i, target, trial, limit):
        self.i = i
        self.target = target
        self.trial = trial
        self.limit = limit

        if self.i > self.target:
            print(f"Down, {self.limit - self.trial}회 남으셨습니다.")
            return self.trial, False

        elif self.i < self.target:
            print(f"up, {self.limit - self.trial}회 남으셨습니다.")
            return self.trial, False

        else:
            self.success_ment(self.id, self.trial)
            self.save_ranking(self.id, self.trial, self.level)
            return self.trial, True

    def up_down_determinant(self, target, trial, limit, id, level, max_num):
        self.target = target
        self.trial = trial
        self.limit = limit
        self.id = id
        self.level = level
        self.max_num = max_num

        while True:
            try:
                self.i = int(input(f"1~{self.max_num} 중 번호를 누르세요: "))

                if 1 <= self.i <= self.max_num:
                    break

                print(f"1~{self.max_num} 사이의 숫자를 입력해주세요.")

            except ValueError:
                print("숫자를 입력해주세요.")

        self.trial += 1

        if self.level == "easy":

            if self.i > self.target:
                print("Down")
                return self.trial, False

            elif self.i < self.target:
                print("up")
                return self.trial, False

            else:
                self.success_ment(self.id, self.trial)
                self.save_ranking(self.id, self.trial, self.level)
                return self.trial, True

        else:
            return self.up_down_trial(
                self.i, self.target, self.trial, self.limit
            )

    def save_ranking(self, id, trial, level):
        self.id = id
        self.trial = trial
        self.level = level
        with open("ranking.txt", "a", encoding="utf-8") as file:
            file.write(f"{self.id},{self.trial},{self.level}\n")

    def up_down_hardmode(self, target, trial, limit, id, level, max_num):
        self.target = target
        self.trial = trial
        self.limit = limit
        self.id = id
        self.level = level
        self.max_num = max_num

        while self.trial < self.limit:

            self.trial, self.success = self.up_down_determinant(
                self.target,
                self.trial,
                self.limit,
                self.id,
                self.level,
                self.max_num,
            )

            if self.success:
                return self.trial, True

        self.failure_ment(self.id, self.limit, self.target)

        return self.trial, False

    def easy_mode(self, id):
        self.id = id
        self.level = "easy"

        print("\n업앤다운 이지모드를 시작하겠습니다.")

        self.trial = 0
        self.target = random.randint(1, 100)

        while True:
            self.trial, self.success = self.up_down_determinant(
                self.target, self.trial, 0, self.id, self.level, 100
            )

            if self.success:
                self.ranking_board.add_record(self.id, self.trial, self.level)
                return

    def hard_mode(self, id):
        self.id = id
        self.level = "hard"

        print("\n업앤다운 하드모드를 시작하겠습니다.")
        print("이번 게임은 10번 안에 끝내셔야 합니다.")

        self.trial = 0
        self.target = random.randint(1, 100)

        self.limit = self.limit_num(self.level)

        self.trial, self.success = self.up_down_hardmode(
            self.target, self.trial, self.limit, self.id, self.level, 100
        )

        if self.success:
            self.ranking_board.add_record(self.id, self.trial, self.level)

    def expert_mode(self, id):
        self.id = id
        self.level = "expert"

        print("\n업앤다운 전문가모드를 시작하겠습니다.")
        print("이번 게임은 10이하의 숫자로 자율 도전이 가능합니다.")
        print("1부터 200 사이의 번호를 맞추셔야 합니다.")

        self.trial = 0
        self.target = random.randint(1, 200)

        self.limit = self.limit_num(self.level)

        print(f"{self.limit}번 이내로 정답을 찾아주세요.")

        self.trial, self.success = self.up_down_hardmode(
            self.target, self.trial, self.limit, self.id, self.level, 200
        )

        if self.success:
            self.ranking_board.add_record(self.id, self.trial, self.level)

    def mode_select(self, id):
        self.id = id

        while True:
            print("\n==================================")
            print("업앤다운 게임의 모드를 선택해주세요")

            try:
                self.seq3 = int(
                    input(
                        "1번을 누르시면 이지모드\n2번을 누르시면 하드모드\n3번을 누르시면 전문가모드\n입니다, 1,2,3번 중에 입력해주세요: "
                    )
                )

                if self.seq3 == 1:
                    self.easy_mode(self.id)
                    break

                elif self.seq3 == 2:
                    self.hard_mode(self.id)
                    break

                elif self.seq3 == 3:
                    self.expert_mode(self.id)
                    break

                else:
                    print("1,2,3 중에서 번호를 입력해주십시오.")

            except ValueError:
                print("숫자로 입력해주세요.")

    def start(self):
        print("\n==================================")
        print("업앤다운 게임에 오신걸 환영합니다.")

        while True:
            self.id = input("ID를 입력해주세요: ")
            if self.id.strip():
                break
            print("ID를 한 글자 이상 입력해주세요.")

        while True:
            try:
                self.seq2 = int(
                    input(
                        "\n1번을 누르시면 업앤다운 게임시작\n2번을 누르시면 과거이력조회\n3번을 누르시면 랭킹보기\n4번을 누르시면 메인메뉴 이동\n입니다, 1,2,3,4번 중에 입력해주세요: "
                    )
                )

                if self.seq2 == 1:
                    print("\n==================================")
                    print("업앤다운 게임시작")
                    self.mode_select(self.id)

                elif self.seq2 == 2:
                    self.ranking_board.past_history(self.id)

                elif self.seq2 == 3:
                    self.ranking_board.ranking_view()

                elif self.seq2 == 4:
                    print("\n==================================")
                    print("업앤다운 게임 종료")
                    break

                else:
                    print("1,2,3,4번의 값 중에서 입력해주십시오.")

            except ValueError:
                print("숫자로 입력해주세요.")


# ==========================================
# LottoGame 클래스 (리스트만 사용)
# ==========================================
class LottoGame:

    def __init__(self):
        # 맵 대신 리스트 2개를 사용해 순서대로 매칭합니다.
        self.user_ids = []      # ID를 저장할 리스트
        self.lotto_list = []    # 번호 리스트를 저장할 리스트
        self.current_id = ""

    def lotto_auto(self, lottery_total):
        while len(lottery_total) < 6:
            lottery_num = random.randint(1, 45)
            if lottery_num not in lottery_total:
                lottery_total.append(lottery_num)

        lottery_total.sort()
        return lottery_total

    def lotto_print(self, lottery_total):
        print("추천 로또 번호 : ", end="")
        for num in lottery_total:
            print(num, end=" ")
        print()

    def lotto_manual(self):
        lottery_total = []

        while True:
            try:
                n = int(input("수동으로 몇 개를 입력할까요? (1~6): "))
                if 1 <= n <= 6:
                    break
                print("1~6 사이의 숫자를 입력해주세요.")
            except ValueError:
                print("숫자로 입력해주세요.")

        while len(lottery_total) < n:
            try:
                x = int(input("1~45 중 입력해주세요: "))

                if x < 1 or x > 45:
                    print("1~45 사이의 숫자만 입력해주세요.")
                    continue

                if x in lottery_total:
                    print("이미 입력한 숫자입니다.")
                    continue

                lottery_total.append(x)

            except ValueError:
                print("숫자로 입력해주세요.")

        return self.lotto_auto(lottery_total)

    # 1. lotto.txt 파일에 [아이디,번호1,번호2,번호3,번호4,번호5,번호6] 저장
    
    def save_lotto(self, id, lotto_numbers):
        # 숫자를 문자로 바꿔서 쉼표로 연결합니다.
        line = f"{id}"
        for num in lotto_numbers:
            line += f",{num}"

        with open("lotto.txt", "a", encoding="utf-8") as file:
            file.write(line + "\n")

    # 2. lotto.txt 파일에서 해당 ID가 들어간 행만 가져와서 출력
    def load_lotto_file(self, id):
        print(f"\n===== {id}님의 파일 저장 이력 =====")

        try:
            with open("lotto.txt", "r", encoding="utf-8") as file:
                lines = file.readlines()

            count = 0
            for line in lines:
                # 쉼표 기준으로 문자열 분할
                data = line.strip().split(",")
                
                # 맨 앞의 ID가 현재 찾는 ID와 같다면
                 # 아이디를 딕셔너리를 키로 가지고 리스트가 추가되는 방법을 하려고 했으나
                    # 딕셔너리를 불러오는 방법을 몰라서 이 방법을 채택함.
                if data[0] == id:
                    count += 1
                    print(f"{count}번째 이력: ", end="")
                    # 1번 인덱스부터 끝까지(번호들만) 출력
                    for i in range(1, len(data)):
                        print(data[i], end=" ")
                    print()

            if count == 0:
                print("저장된 이력이 없습니다.")

        except FileNotFoundError:
            print("아직 저장된 로또 파일(lotto.txt)이 없습니다.")

    # 3. 리스트 데이터에서 나의 이력 출력
    def lotto_history_view(self, id):
        print(f"\n===== {id}님의 프로그램 이력 (리스트 데이터) =====")
        
        count = 0
        for i in range(len(self.user_ids)):
            if self.user_ids[i] == id:
                count += 1
                print(f"{count}번째 이력: ", end="")
                for num in self.lotto_list[i]:
                    print(num, end=" ")
                print()

        if count == 0:
            print("현재 실행 중 기록된 이력이 없습니다.")

    def lotto_draw(self, id):
        reaction = input(
            "자동으로 추천하실 겁니까? 자동 또는 수동으로 입력해주세요: "
        )
        print()

        if reaction == "자동":
            lottery_total = self.lotto_auto([])

        elif reaction == "수동":
            lottery_total = self.lotto_manual()

        else:
            print("자동 또는 수동으로 정확히 입력해주세요.")
            return

        self.lotto_print(lottery_total)

        # 리스트에 각각 추가
        self.user_ids.append(id)
        self.lotto_list.append(lottery_total)

        # 파일에도 아이디와 함께 저장
        self.save_lotto(id, lottery_total)

    def start(self):
        print("\n==================================")
        print("로또 번호 추천 시스템에 오신 것을 환영합니다.")

        while True:
            self.current_id = input("ID를 입력해주세요: ")
            if self.current_id.strip():
                break
            print("ID를 한 글자 이상 입력해주세요.")

        while True:
            try:
                start_num = int(
                    input(
                        "\n1번: 추첨하기 / 2번: 실행이력 보기 / 3번: 파일이력 조회 / 4번: 메인메뉴 이동\n번호를 입력하세요: "
                    )
                )

                if start_num == 1:
                    self.lotto_draw(self.current_id)

                elif start_num == 2:
                    self.lotto_history_view(self.current_id)

                elif start_num == 3:
                    self.load_lotto_file(self.current_id)

                elif start_num == 4:
                    print("메인메뉴로 이동합니다.")
                    break

                else:
                    print("1, 2, 3, 4 중에서 입력해주세요.")

            except ValueError:
                print("숫자로 입력해주세요.")


class RockSP:

    def __init__(self):
        self.rsp_list = ["가위", "바위", "보"]
        self.win = {}
        self.call = ""

    def rsp_start(self):
        print("\n==================================")
        self.call = input("닉네임을 입력해주세요: ")
        self.call = self.call.replace(" ", "")
        print("가위바위보를 시작합시다.")
        while True:
            try:
                seq2 = int(
                    input(
                        "\n1번을 누르시면 가위바위보 시작\n"
                        "2번을 누르시면 나의 과거이력조회\n"
                        "3번을 누르시면 메인메뉴 이동\n"
                        "입니다, 1,2,3번 중에 입력해주세요: "
                    )
                )
                if seq2 == 1:
                    print("\n==================================")
                    print("가위-바위-보 시작~!")
                    self.rsp()
                elif seq2 == 2:
                    self.history_(self.call)

                elif seq2 == 3:
                    print("\n==================================")
                    print("가위바위보 게임 종료")
                    break
                else:
                    print("1,2,3번의 값 중에서 입력해주십시오.")
            except ValueError:
                print("숫자로 입력해주세요.")

    def user_choose(self):
        while True:
            user_choice = input('"가위", "바위", "보" 중에서 입력해주세요: ')
            if user_choice == "가위":
                return 1
            elif user_choice == "바위":
                return 2
            elif user_choice == "보":
                return 3
            else:
                print("다시 입력해주세요.")

    def rsp(self):
        user = self.user_choose()
        computer = random.randint(1, 3)
        result = computer - user
        print(
            f"상대 : {self.rsp_list[computer-1]} \n{self.call}님:"
            f" {self.rsp_list[user-1]}"
        )
        if result == -1 or result == 2:
            print("이겼습니다!")
            check = 1
        elif result == -2 or result == 1:
            print("졌습니다.")
            check = -1
        else:
            print("비겼습니다.")
            check = 0
        self.add_record(self.call, check)

    def add_record(self, id, check):
        if id not in self.win:
            self.win[id] = []

        self.win[id].append(check)

    def history_(self, id):
        if id not in self.win:
            print(f"{id}님의 게임 기록이 없습니다.")
            return

        t = len(self.win[id])
        w = self.win[id].count(1)
        l = self.win[id].count(-1)
        print(f"{t}번의 게임 중 {w}번 이기셨고, {l}번 졌습니다.")


class MainMenu:

    def __init__(self, ranking_board, up_down, lotto):
        self.ranking_board = ranking_board
        self.up_down = up_down
        self.lotto = lotto
        self.rsp = RockSP()

    def start(self):
        while True:
            try:
                self.seq1 = int(
                    input(
                        "\n==================================\n"
                        "번호를 누르세요\n"
                        "1번을 누르면 로또 번호\n"
                        "2번을 누르면 업앤다운이 나옵니다.\n"
                        "3번을 누르면 가위바위보가 나옵니다.\n"
                        "4번을 누르면 프로그램이 종료 됩니다.\n"
                        "1번과 2번 3번 그리고 4번 중에 눌러주십시오: "
                    )
                )

                if self.seq1 == 1:
                    self.lotto.start()

                elif self.seq1 == 2:
                    self.up_down.start()

                elif self.seq1 == 3:
                    self.rsp.rsp_start()

                elif self.seq1 == 4:
                    print("프로그램 종료")
                    break

                else:
                    print("1번과 2번, 3번 4번중에 입력해주세요.")

            except ValueError:
                print("숫자로 입력해주세요.")


def init_ranking_file(board):
    sample_data = [
        ("지민", 5, "easy"),
        ("지민", 8, "hard"),
        ("지민", 6, "expert"),
        ("1", 7, "easy"),
        ("1", 4, "hard"),
        ("소정", 9, "easy"),
        ("소정", 6, "hard"),
        ("소정", 10, "expert"),
        ("소정", 5, "easy"),
        (1, 2, "easy"),
    ]

    with open("ranking.txt", "w", encoding="utf-8") as file:
        for name, trial, level in sample_data:
            board.add_record(name, trial, level)
            file.write(f"{name},{trial},{level}\n")


def load_ranking():
    players = []

    try:
        with open("ranking.txt", "r", encoding="utf-8") as file:
            lines = file.readlines()

        for line in lines:
            data = line.strip().split(",")
            if len(data) >= 3:
                player = {
                    "name": data[0],
                    "시도횟수": int(data[1]),
                    "난이도": data[2],
                }
                players.append(player)

    except FileNotFoundError:
        print("\n[알림] 아직 저장된 랭킹 파일(ranking.txt)이 없습니다.")

    return players


# ==========================================
# 실행부
# ==========================================

rank = {}
rank_level = {}

ranking_board = RankingBoard(rank, rank_level)

init_ranking_file(ranking_board)

up_down = UpDownGame(ranking_board)
lotto = LottoGame()
main = MainMenu(ranking_board, up_down, lotto)

main.start()

print("\n===== 저장된 파일 랭킹 불러오기 =====")
players = load_ranking()
print(players)