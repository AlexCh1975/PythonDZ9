from telegram import ReplyKeyboardRemove
from toke import *
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler
)


board = list(range(1, 10))
player = chr(10060)
counter = 0
CHOICE = 0

def draw_board(board):
    text = ''
    text += f'\n{"-" * 25}\n'
    for i in range(3):
        for j in range(3):
            text += f'{board[j + i * 3]:^10}'
        text += f'\n{"-" * 25}\n' 
    return text

def check_win(board):
    win_coord = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6))
    n = [board[x[0]] for x in win_coord if board[x[0]] == board[x[1]] == board[x[2]]]
    return n[0] if n else n


def choice(update, _):
    global player, counter
    pos = update.message.text
    pos = int(pos)
    if pos not in board:
        update.message.reply_text(f'{pos} Некорректный ввод! {chr(9940)}\nПовторите попытку.')
    else:
        board.insert(board.index(pos), player)
        board.remove(pos)
        update.message.reply_text(draw_board(board))
        if check_win(board):
            update.message.reply_text(f"{player} - Выиграл{chr(127942)}")
            return end(update, _)
        
        player = chr(11093) if player == chr(10060) else chr(10060)
        counter += 1
    if counter == 9:
        update.message.reply_text(f'Ничья {chr(129318)}{chr(129309)}!')
        return end(update, _)
        
    update.message.reply_text('Ходит {}'.format(chr(10060) if player == chr(10060) else chr(11093)))
    

def start(update, _):
    global board, player, counter
    board = list(range(1, 10))
    update.message.reply_text('Поиграем в крестики нолики!') 
    update.message.reply_text(draw_board(board))
    update.message.reply_text(f'Первый ходит {player}')
    return CHOICE

def end(update, _):
    update.message.reply_text('Спасибо за игру', reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

if __name__ == '__main__':  
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states = {
            CHOICE: [
                MessageHandler(Filters.text, choice),
            ]
        },
           
        fallbacks=[CommandHandler('exit', end)],
    )
    dp.add_handler(conv_handler)
    print("server start")
    updater.start_polling()
    updater.idle()