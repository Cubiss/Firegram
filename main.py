import tkinter
import PIL.Image
import PIL.ImageTk


class Firegram:
    def __init__(self, start_state):
        self.neighbors = [[3, 4], [2, 4], [1, 3], [0, 2], [0, 1]]
        self.current_state = start_state
        self.state_history = []

        self.root = root = tkinter.Tk()
        self.root.geometry("600x600")
        self.canvas = canvas = tkinter.Canvas(root, width=600, height=600)

        im = PIL.Image.open("resources/pentagram.png")
        self.img = PIL.ImageTk.PhotoImage(im)

        canvas.create_image(1, 1, anchor=tkinter.NW, image=self.img)
        canvas.place(x=0, y=0, relwidth=1, relheight=1)
        canvas.bind("<Button-1>", lambda event: print(f"x={event.x}, y={event.y}"))

        self.buttons = []
        for i in range(5):
            self.buttons.append(tkinter.Button(root, text=str(i)))

        self.buttons[0]['command'] = lambda: self.activate_brazier(0) and self.set_button_colors()
        self.buttons[1]['command'] = lambda: self.activate_brazier(1) and self.set_button_colors()
        self.buttons[2]['command'] = lambda: self.activate_brazier(2) and self.set_button_colors()
        self.buttons[3]['command'] = lambda: self.activate_brazier(3) and self.set_button_colors()
        self.buttons[4]['command'] = lambda: self.activate_brazier(4) and self.set_button_colors()
        self.buttons[0].place(x=290, y=45)
        self.buttons[1].place(x=45, y=229)
        self.buttons[2].place(x=531, y=231)
        self.buttons[3].place(x=135, y=519)
        self.buttons[4].place(x=415, y=528)

    def set_state(self, state):
        self.current_state = state
        self.set_button_colors()

    def set_button_colors(self):
        for brazier, button in zip(self.current_state, self.buttons):
            button['bg'] = 'green' if brazier else 'red'

    def start(self):
        self.root.mainloop()

    @staticmethod
    def brazier_repr(brazier):
        return 'x' if brazier else 'o'

    def __str__(self):
        return f'''  {self.brazier_repr(self.current_state[0])}
    {self.brazier_repr(self.current_state[1])}   {self.brazier_repr(self.current_state[2])}
     {self.brazier_repr(self.current_state[3])} {self.brazier_repr(self.current_state[4])}'''

    def is_solved(self, state=None):
        return all(state or self.current_state)

    def activate_brazier(self, x, state=None, checks=True):
        state = state or self.current_state
        state = list(state)

        if checks and state[x]:
            return None
        else:
            state[x] = True
            for n in self.neighbors[x]:
                state[n] = not state[n]

        self.state_history.append(self.current_state)
        self.current_state = state
        return state

    solve_calls = 0

    def solve(self, state_history, action_history, state, best_size=float('inf')):
        if action_history == [3]:
            pass

        self.solve_calls += 1

        state_history = state_history.copy()
        action_history = action_history.copy()
        state = state.copy()

        if len(state_history) >= best_size:
            return None, None

        if self.is_solved(state.copy()):
            return state_history, action_history

        shortest_solution = None
        shortest_actions = None

        for action in range(5):
            new_state = self.activate_brazier(action, state)
            if new_state is None:
                continue

            if new_state not in state_history:
                solution, actions = self.solve(state_history + [new_state], action_history + [action], new_state, best_size)
                if solution is None:
                    continue
                else:
                    if shortest_solution is None or len(solution) < len(shortest_solution):
                        shortest_solution = solution
                        shortest_actions = actions
                        best_size = min(best_size, len(shortest_solution))
                        continue
        else:
            return shortest_solution, shortest_actions


def main():

    start_state = [False, False, False, False, False]

    gui = Firegram(start_state)

    solution, actions = gui.solve([], [], start_state)

    print()
    print("starting state:", start_state)
    print("solve calls:   ", gui.solve_calls)
    print("best solution: ", len(actions))
    print("actions:       ", actions)
    print("solution:      ", solution)

    gui.set_state(start_state)

    gui.start()


if __name__ == '__main__':

    main()
