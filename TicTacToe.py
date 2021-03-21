from tkinter import *
from PIL import ImageTk, Image


class Cell:

    def __init__(self, i, j, w, r):
        self.i = i
        self.j = j
        self.w = w
        self.r = r
        self.n = None

    def __int__(self):
        self.canvas = self.place()

    def place(self):
        x = (self.i + 0.5) * self.w
        y = (self.j + 0.5) * self.w
        draw = self.canvas

        for i in range(len(draw)):
            if draw[i] is not None:
                draw = canvas.delete(draw[i])

        if self.n is not None:
            if self.n == players[1][0]:
                draw[0] = canvas.create_line(x - self.r, y - self.r, x + self.r, y + self.r, width=4)
                draw[1] = canvas.create_line(x + self.r, y - self.r, x - self.r, y + self.r, width=4)
            elif self.n == players[1][1]:
                draw[2] = canvas.create_oval(x - self.r, y - self.r, x + self.r, y + self.r, width=4)

        return draw


root = Tk()
root.title("Tic Tac Toe")

# root.iconbitmap('images/icon.ico')

grid = []

width = 600
height = 600

cell_width = width / 3
cell_border = cell_width / 4

pop = Toplevel(root)
is_game_over = False
win_line = ""


def index(row, col):
    return row * 3 + col


def new_game():
    global players, is_game_over
    canvas.delete("all")
    pop.destroy()
    grid.clear()
    is_game_over = False
    players = [[player1_name.get(), player2_name.get()], ["X", "O"]]

    for j in range(3):
        for i in range(3):
            cell = Cell(i, j, cell_width, cell_border)
            cell.canvas = [None, None, None]
            grid.append(cell)

    draw_board()
    player_label.config(text=players[0][0] + "'s (" + players[1][0] + ") turn")


def draw_board():
    canvas.create_line(cell_width * 1, 0, cell_width * 1, height, width=6)
    canvas.create_line(cell_width * 2, 0, cell_width * 2, height, width=6)
    canvas.create_line(0, cell_width * 1, width, cell_width * 1, width=6)
    canvas.create_line(0, cell_width * 2, width, cell_width * 2, width=6)


def position_clicked(event):
    # print("you clicked at", event.x, event.y)
    x, y = event.x, event.y

    if x < 0:
        x = 0
    elif x >= width:
        x = width - 1

    if y < 0:
        y = 0
    elif y >= height:
        y = height - 1

    row, col = int(y / cell_width), int(x / cell_width)

    place_XO(row, col)


def place_XO(row, col):
    if grid[index(row, col)].n is None and not is_game_over:

        player = player_label.cget("text")[-7]
        if player == players[1][0]:
            grid[index(row, col)].n = players[1][0]
            player_label.config(text=players[0][1] + "'s (" + players[1][1] + ") turn")
        else:
            grid[index(row, col)].n = players[1][1]
            player_label.config(text=players[0][0] + "'s (" + players[1][0] + ") turn")
        grid[index(row, col)].place()
        root.update()
        gameover()


def gameover():
    global is_game_over, win_line
    is_game_over = False

    # checking rows
    for i in range(3):
        if grid[index(i, 0)].n is None or grid[index(i, 1)].n is None or grid[index(i, 2)].n is None:
            win_line = None
        elif grid[index(i, 0)].n == grid[index(i, 1)].n and grid[index(i, 0)].n == grid[index(i, 2)].n:
            is_game_over = True
            win_line = f"Row {i}"
            draw_win_line()
            return

    # checking columns
    for j in range(3):
        if grid[index(0, j)].n is None or grid[index(1, j)].n is None or grid[index(2, j)].n is None:
            win_line = None
        elif grid[index(0, j)].n == grid[index(1, j)].n and grid[index(0, j)].n == grid[index(2, j)].n:
            is_game_over = True
            win_line = f"Col {j}"
            draw_win_line()
            return

    # checking diagonals
    for x in range(2):
        if grid[index(0, 2 * x)].n is None or grid[index(1, 1)].n is None or grid[index(2, 2 - 2 * x)].n is None:
            win_line = None
        elif grid[index(0, 2 * x)].n == grid[index(1, 1)].n and grid[index(0, 2 * x)].n == grid[index(2, 2 - 2 * x)].n:
            is_game_over = True
            win_line = f"Dia {x}"
            draw_win_line()
            return

    # checking tie
    for i in range(len(grid)):
        if grid[i].n is None:
            break
        elif i == len(grid) - 1:
            is_game_over = True
            win_line = f"Tie "
            draw_win_line()
            return


def draw_win_line():
    global win_line
    win_line = win_line.split()

    if win_line[0] == "Row":
        canvas.create_line(cell_border, cell_width * int(win_line[1]) + cell_width / 2,
                           width - cell_border, cell_width * int(win_line[1]) + cell_width / 2,
                           width=15, fill="#ff0000")

        winner = ["lose", player_label.cget("text")[-7]]
        msg_box(winner)
    elif win_line[0] == "Col":
        canvas.create_line(cell_width * int(win_line[1]) + cell_width / 2, cell_border,
                           cell_width * int(win_line[1]) + cell_width / 2, height - cell_border,
                           width=15, fill="#ff0000")

        winner = ["lose", player_label.cget("text")[-7]]
        msg_box(winner)
    elif win_line[0] == "Dia":
        if int(win_line[1]) == 0:
            canvas.create_line(cell_border, cell_border, width - cell_border, height - cell_border,
                               width=15, fill="#ff0000")

            winner = ["lose", player_label.cget("text")[-7]]
            msg_box(winner)
        else:
            canvas.create_line(cell_border, height - cell_border, width - cell_border, cell_border,
                               width=15, fill="#ff0000")

            winner = ["lose", player_label.cget("text")[-7]]
            msg_box(winner)
    elif win_line[0] == "Tie":
        canvas.create_line(cell_border * 2.25, cell_border * 3.25, cell_border * 3.75, cell_border * 3.25,
                           width=6, fill="#ff0000")
        canvas.create_line(cell_border * 3.00, cell_border * 3.25, cell_border * 3.00, cell_border * 5.25,
                           width=6, fill="#ff0000")

        canvas.create_line(cell_border * 5.25, cell_border * 3.25, cell_border * 6.75, cell_border * 3.25,
                           width=6, fill="#ff0000")
        canvas.create_line(cell_border * 5.25, cell_border * 5.25, cell_border * 6.75, cell_border * 5.25,
                           width=6, fill="#ff0000")
        canvas.create_line(cell_border * 6.00, cell_border * 3.25, cell_border * 6.00, cell_border * 5.25,
                           width=6, fill="#ff0000")

        canvas.create_line(cell_border * 8.25, cell_border * 3.25, cell_border * 9.75, cell_border * 3.25,
                           width=6, fill="#ff0000")
        canvas.create_line(cell_border * 8.25, cell_border * 5.25, cell_border * 9.75, cell_border * 5.25,
                           width=6, fill="#ff0000")
        canvas.create_line(cell_border * 8.25, cell_border * 4.25, cell_border * 9.00, cell_border * 4.25,
                           width=6, fill="#ff0000")
        canvas.create_line(cell_border * 8.25, cell_border * 3.25, cell_border * 8.25, cell_border * 5.25,
                           width=6, fill="#ff0000")

        winner = ["tie", player_label.cget("text")[-7]]
        msg_box(winner)


def msg_box(winner):
    global pop

    if is_game_over:
        pop = Toplevel(root)

    pop.title("Winner?")

    x = root.winfo_rootx() + width / 2 - 130
    y = root.winfo_rooty() + 2 * cell_width - 100

    pop.geometry('%dx%d+%d+%d' % (250, 100, x, y))
    # pop.iconbitmap('images/icon.ico')

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
    pop_exit_game = Button(pop_frame, text="Exit Game", padx=10, pady=5, command=root.quit)
    pop_exit_game.grid(row=0, column=1)


canvas = Canvas(root, width=width, height=height, bg="#ffffff")
canvas.bind("<Button-1>", position_clicked)
new_game_button = Button(root, text="New Game", command=new_game)
exit_game_button = Button(root, text="Exit game", command=root.quit)
new_game_button.config(width=int(width / 20), height=int(width / 150))
exit_game_button.config(width=int(width / 20), height=int(width / 150))
player_label = Label(root, text="")
player1_name = Entry(root)
player2_name = Entry(root)
logo = ImageTk.PhotoImage(Image.open("images/logo128.jpg"))
logo_label = Label(image=logo)

canvas.grid(row=0, column=0, rowspan=15, columnspan=3)
new_game_button.grid(row=4, column=5)
exit_game_button.grid(row=7, column=5)
# logo_label.grid(row=0, column=5)

player_label.grid(row=1, column=5)
player1_name.grid(row=2, column=5)
player2_name.grid(row=3, column=5)
player1_name.insert(0, "Player 1")
player2_name.insert(0, "Player 2")

players = [[player1_name.get(), player2_name.get()], ["X", "O"]]

new_game()

root.mainloop()
