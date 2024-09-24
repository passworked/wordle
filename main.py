from random import choice
from colorama import Fore, Style, init

init(autoreset=True)

class WordGameLetter:
    '''
    0 = 'gray'
    1 = 'yellow'
    2 = 'green'
    '''
    def __init__(self, letter: str, color: int) -> None:
        self.color = color
        self.text = letter

class WordleGame:
    def __init__(self, total_try_chance) -> None:
        self.load_word_set()
        self.generate_correct_answer()
        self.total_try_chance: int = total_try_chance
        self.now_try_chance: int = 0

    def generate_correct_answer(self) -> None:
        self.correct_ans = choice(self.word_set).strip()  # 去除换行符
        print(f"正确答案是: {self.correct_ans}")  # 仅用于调试
        self.correct_ans_list = self._split_word(self.correct_ans)

    def load_word_set(self):
        with open('word_list.txt', 'r') as f:
            self.word_set = [line.strip() for line in f.readlines()]  # 去除换行符

    def guess_the_word(self, word):
        self.now_word_split: list[WordGameLetter] = self._split_guess_word(word)
        for pos in range(len(self.now_word_split)):
            if self.now_word_split[pos].text in self.correct_ans_list:
                self.now_word_split[pos].color = 1  # Yellow
            if self.now_word_split[pos].text == self.correct_ans_list[pos]:
                self.now_word_split[pos].color = 2  # Green
        self.now_try_chance += 1
        if self.win(self.now_word_split):
            print(f'您赢了，正确单词是 {self.correct_ans}，您一共猜了 {self.now_try_chance} 次')
            return False  # 游戏结束
        if self.lose():
            print(f'您输了，正确单词是 {self.correct_ans}')
            return False  # 游戏结束
        self.guess_output()
        return True  # 游戏继续

    def _split_guess_word(self, word: str) -> list[WordGameLetter]:
        return [WordGameLetter(letter, 0) for letter in word]

    def _split_word(self, word: str) -> list[str]:
        return list(word)

    def is_word(self, word: str):
        return word in self.word_set 

    def win(self, now_word_split: list[WordGameLetter]):
        for letter in now_word_split:
            if letter.color != 2:
                return False
        return True

    def lose(self):
        return self.total_try_chance <= self.now_try_chance

    def guess_output(self):
        self.print_colorful_text()
        print(f'您猜的结果是本次游戏可以猜 {self.total_try_chance} 次，已经尝试 {self.now_try_chance} 次')

    def print_colorful_text(self):
        for letter in self.now_word_split:
            if letter.color == 0:
                print(Fore.LIGHTBLACK_EX + letter.text + Style.RESET_ALL, end='')
            elif letter.color == 1:
                print(Fore.YELLOW + letter.text + Style.RESET_ALL, end='')
            elif letter.color == 2:
                print(Fore.GREEN + letter.text + Style.RESET_ALL, end='')
        print()  # 换行

if __name__ == '__main__':
    word_game = WordleGame(10)
    game_active = True

    while game_active:
        word = input('请输入您的猜测: ')
        game_active = word_game.guess_the_word(word)