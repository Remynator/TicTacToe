from tkinter import *
from PIL import ImageTk, Image
import random
import time

root = Tk()
root.title("Tic Tac Toe")

root.iconbitmap('images/icon.ico')

grid = [
    ["X", "O", "X"],
    ["X", " ", "O"],
    ["O", "O", "X"],
]

width = 600
height = 600

canvas = Canvas(root, width=width, height=height, bg="#ffffff")
w = width / 3
h = height / 3
xr = w / 4
yr = h / 4

pop = Toplevel(root)
is_game_over = False
is_random_position = False


def callback(event):
    # print("you clicked at", event.x, event.y)
    x, y = event.x, event.y
    new_position(x, y)


def exit_game():
    pop.destroy()
    root.destroy()


def msg_box(winner):
    global pop

    if is_game_over:
        pop = Toplevel(root)

    pop.title("Winner?")
    pop.geometry("250x100")
    pop.iconbitmap('images/icon.ico')

    msg = ""

    if winner[0] == "tie":
        msg = "It is a tie."
    elif winner[0] == "lose" and winner[1] == players[1][1]:
        msg = players[0][0] + " is the winner."
    elif winner[0] == "lose" and winner[1] == players[1][0]:
        msg = players[0][1] + " is the winner."

    pop_text = Label(pop, text=msg)
    pop_text.pack(pady=10)

    pop_frame = Frame(pop)
    pop_frame.pack(pady=10)

    pop_new_game = Button(pop_frame, text="New Game", padx=10, pady=5, command=new_game)
    pop_new_game.grid(row=0, column=0)
    pop_exit_game = Button(pop_frame, text="Exit Game", padx=10, pady=5, command=exit_game)
    pop_exit_game.grid(row=0, column=1)


def new_game():
    global pop
    global is_game_over
    global is_random_position
    global players
    pop.destroy()
    is_game_over = False
    players = [[player1_name.get(), player2_name.get()], ["X", "O"]]
    for i in range(3):
        for j in range(3):
            grid[i][j] = " "
    canvas.delete("all")
    draw_grid(grid)
    player_label.config(text=players[0][0] + "'s (" + players[1][0] + ") turn")
    is_random_position = False


def random_position():
    global is_game_over
    global is_random_position
    is_random_position = True
    if not is_game_over:
        x = random.randint(0, 2) * (width / 3) + (width / 6)
        y = random.randint(0, 2) * (height / 3) + (height / 6)
        new_position(x, y)


def random_game():
    global is_game_over
    new_game()
    is_game_over = False
    while not is_game_over:
        random_position()
        root.update()
        time.sleep(.500)


canvas.bind("<Button-1>", callback)
new_game_button = Button(root, text="New Game", command=new_game)
random_game_button = Button(root, text="Random game", command=random_game)
random_position_button = Button(root, text="Random Position", command=random_position)
exit_game_button = Button(root, text="Exit game", command=exit_game)
new_game_button.config(width=int(width / 20), height=int(width / 150))
random_game_button.config(width=int(width / 20), height=int(width / 150))
random_position_button.config(width=int(width / 20), height=int(width / 150))
exit_game_button.config(width=int(width / 20), height=int(width / 150))
player_label = Label(root, text="")
player1_name = Entry(root)
player2_name = Entry(root)
logo = ImageTk.PhotoImage(Image.open("images/logo128.jpg"))
logo_label = Label(image=logo)

logo_label.grid(row=0, column=5)
new_game_button.grid(row=4, column=5)
random_game_button.grid(row=5, column=5)
random_position_button.grid(row=6, column=5)
exit_game_button.grid(row=7, column=5)

player_label.grid(row=1, column=5)
player1_name.grid(row=2, column=5)
player2_name.grid(row=3, column=5)
player1_name.insert(0, "Player 1")
player2_name.insert(0, "Player 2")

players = [[player1_name.get(), player2_name.get()], ["X", "O"]]


def gameover(board):
    global is_game_over
    is_game_over = False
    # checking rows
    for i in range(3):
        check = ["row"]
        row = []
        for j in range(3):
            row.append(board[i][j])
            if len(row) == 3:
                if row[0] == " " and row[1] == " " and row[2] == " ":
                    check.append(" ")
                elif row[0] == row[1] and row[0] == row[2]:
                    check.append(i)
                    is_game_over = True
                    return check
    # checking columns
    for j in range(3):
        check = ["col"]
        col = []
        for i in range(3):
            col.append(board[i][j])
            if len(col) == 3:
                if col[0] == " " and col[1] == " " and col[2] == " ":
                    check.append(" ")
                elif col[0] == col[1] and col[0] == col[2]:
                    check.append(j)
                    is_game_over = True
                    return check
    # checking diagonals
    for x in range(2):
        check = ["dia"]
        dia = []
        for i in range(3):
            j = [2 - i, i][x == 0]
            dia.append(board[i][j])
            if len(dia) == 3:
                if dia[0] == " " and dia[1] == " " and dia[2] == " ":
                    check.append(" ")
                elif dia[0] == dia[1] and dia[0] == dia[2]:
                    check.append(x)
                    is_game_over = True
                    return check
    # checking tie
    tie = []
    for i in range(3):
        check = ["tie"]
        for j in range(3):
            tie.append(board[i][j])
            if len(tie) == 9 and not (tie.__contains__(" ")):
                is_game_over = True
                return check
    is_game_over = False
    return [" ", " "]


def draw_board():
    canvas.create_line(w * 1, 0, w * 1, height, width=6)
    canvas.create_line(w * 2, 0, w * 2, height, width=6)
    canvas.create_line(0, h * 1, width, h * 1, width=6)
    canvas.create_line(0, h * 2, width, h * 2, width=6)


def draw_grid(board):
    draw_board()
    for i in range(3):
        for j in range(3):
            x = w * j + w / 2
            y = h * i + h / 2
            spot = board[i][j]
            if spot == players[1][0]:
                canvas.create_line(x - xr, y - yr, x + xr, y + yr, width=4)
                canvas.create_line(x + xr, y - yr, x - xr, y + yr, width=4)
            elif spot == players[1][1]:
                canvas.create_oval(x - xr, y - yr, x + xr, y + yr, width=4)
    canvas.grid(row=0, column=0, rowspan=15, columnspan=5)


def draw_win_line():
    game_over = gameover(grid)
    if game_over[0] == "row":
        canvas.create_line(xr, h * game_over[1] + h / 2, width - xr, h * game_over[1] + h / 2, width=15, fill="#ff0000")
        winner = ["lose", player_label.cget("text")[-7]]
        msg_box(winner)
    elif game_over[0] == "col":
        canvas.create_line(w * game_over[1] + w / 2, yr, w * game_over[1] + w / 2, height - yr, width=15,
                           fill="#ff0000")
        winner = ["lose", player_label.cget("text")[-7]]
        msg_box(winner)
    elif game_over[0] == "dia":
        if game_over[1] == 0:
            canvas.create_line(xr, yr, width - xr, height - yr, width=15, fill="#ff0000")
            winner = ["lose", player_label.cget("text")[-7]]
            msg_box(winner)
        else:
            canvas.create_line(xr, height - yr, width - xr, yr, width=15, fill="#ff0000")
            winner = ["lose", player_label.cget("text")[-7]]
            msg_box(winner)
    elif game_over[0] == "tie":
        canvas.create_line(xr * 2.25, yr * 3.25, xr * 3.75, yr * 3.25, width=6, fill="#ff0000")
        canvas.create_line(xr * 3.00, yr * 3.25, xr * 3.00, yr * 5.25, width=6, fill="#ff0000")

        canvas.create_line(xr * 5.25, yr * 3.25, xr * 6.75, yr * 3.25, width=6, fill="#ff0000")
        canvas.create_line(xr * 5.25, yr * 5.25, xr * 6.75, yr * 5.25, width=6, fill="#ff0000")
        canvas.create_line(xr * 6.00, yr * 3.25, xr * 6.00, yr * 5.25, width=6, fill="#ff0000")

        canvas.create_line(xr * 8.25, yr * 3.25, xr * 9.75, yr * 3.25, width=6, fill="#ff0000")
        canvas.create_line(xr * 8.25, yr * 5.25, xr * 9.75, yr * 5.25, width=6, fill="#ff0000")
        canvas.create_line(xr * 8.25, yr * 4.25, xr * 9.00, yr * 4.25, width=6, fill="#ff0000")
        canvas.create_line(xr * 8.25, yr * 3.25, xr * 8.25, yr * 5.25, width=6, fill="#ff0000")
        winner = ["tie", player_label.cget("text")[-7]]
        msg_box(winner)


def new_position(x, y):
    row_nr = ""
    col_nr = ""
    if 0 < y < height / 3:
        row_nr = 0
    elif height / 3 < y < height / 3 * 2:
        row_nr = 1
    elif height / 3 * 2 < y < height:
        row_nr = 2

    if 0 < x < width / 3:
        col_nr = 0
    elif width / 3 < x < width / 3 * 2:
        col_nr = 1
    elif width / 3 * 2 < x < width:
        col_nr = 2

    # print(str(row_nr) + ", " + str(col_nr))
    place_XO(row_nr, col_nr)


def place_XO(row, col):
    global is_random_position
    if grid[row][col] == " " and not is_game_over:
        for i in range(3):
            for j in range(3):
                if i == row and j == col:
                    player = player_label.cget("text")[-7]
                    if player == players[1][0]:
                        grid[i][j] = players[1][0]
                        player_label.config(text=players[0][1] + "'s (" + players[1][1] + ") turn")
                    else:
                        grid[i][j] = players[1][1]
                        player_label.config(text=players[0][0] + "'s (" + players[1][0] + ") turn")
                    draw_grid(grid)
                    draw_win_line()
        is_random_position = False
    elif is_random_position:
        random_position()


new_game()
draw_grid(grid)

root.mainloop()
