from tkinter import *
import Game
import Database

# assign variables to proper statements
my_cursor = Database.my_cursor
mydb = Database.mydb

class Page(Tk):
    """ Create empty container for future windows """
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        # container that will be filled with other frames
        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # dictionary for frames
        self.frames = {}

        # fill self.frames with a bunch of possible frames 
        for F in (StartPage, RegisterPage, LoginPage, LoggedUser, MyScores, Leaderboard):

            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # show StartPage
        self.show_frame(StartPage)

    def show_frame(self, cont):
        """ Raise frame to the top. """
        frame = self.frames[cont]
        frame.tkraise()
        # create custom event
        frame.event_generate("<<ShowFrame>>")


class StartPage(Frame):
    """ Page with main buttons. """
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        # create StartPage label
        self.start_page_label =  Label(self, text = 'Welcome to the "Login interface with Tkinter"', font = 14).pack(fill = X, pady = 10)

        # create buttons with lambda function for app navigation
        self.register_button = Button(self, text = 'Register', font = 10, width = 30, height = 2, command = lambda: controller.show_frame(RegisterPage)).pack(pady = 30)
        self.login_button = Button(self, text='Login', font=10, width=30, height=2, command = lambda: controller.show_frame(LoginPage)).pack(pady=10)


class RegisterPage(Frame):
    """ Page with for registration needed actions. """
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        # create buttons in upper left corner for navigation
        self.start_page_button = Button(self, text='StartPage', font=5, width = 10,  command=lambda: controller.show_frame(StartPage)).pack(side = LEFT, anchor = NW)
        self.login_button = Button(self, text='Login', font=5, width=10, command=lambda: controller.show_frame(LoginPage)).pack(side=LEFT, anchor=NW)

        # create RegisterPage label
        self.register_label =  Label(self, text = 'Welcome to the registration section', font = 14).place(anchor = N, relx = 0.5, rely =0.2)

        # username
        self.username_label = Label(self, text='Username: ', font=10).place(anchor=N, relx=0.3, rely=0.4)
        self.username_entry = Entry(self ,width=30)
        self.username_entry.place(anchor=N, relx=0.6, rely=0.4)

        # password
        self.password_label = Label(self, text='Password: ', font=10).place(anchor=N, relx=0.3, rely=0.55)
        self.password_entry = Entry(self, width=30)
        self.password_entry.place(anchor=N, relx=0.6, rely=0.55)

        # submit button
        self.submit_button = Button(self, text='Submit', font=5, width=20, height=1, command = self.save_account).place(anchor=N, relx=0.5, rely=0.8)

        # creating a variable for entry widget
        self.text = StringVar()
        self.text.set('')

    def save_account(self):
        """Method that saves given input"""
        # save entries as variables
        username = self.username_entry.get()
        password = self.password_entry.get()

        # setting text to blank before new log in session
        self.text.set('')

        # checks if username is already used 
        # when new username selected, the SQL query returns empty list == False; "if" statement can run because condition is not False
        my_cursor.execute("SELECT username FROM Players WHERE username = ?", (username, ))
        username_query_result = my_cursor.fetchall()
        if not username_query_result:
            my_cursor.execute("INSERT INTO Players (username, password) VALUES (?, ?)", (username, password))
            mydb.commit()
            self.text.set('Registration success!')
            color = 'green'
        else:
            self.text.set('Username already exists!')
            color = 'red'

        # clear the entry 
        self.username_entry.delete(0, END)
        self.password_entry.delete(0, END)

        # display label with registration outcome
        Label(self, textvariable=self.text, font=10, fg = color).place(anchor=N, relx=0.5, rely=0.67)


class LoginPage(Frame):
    """ Page with for logging needed actions. """
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        # create buttons in upper left corner for navigation
        self.start_page_button = Button(self, text = 'StartPage', font = 5, width = 10, command = lambda: controller.show_frame(StartPage)).pack(side = LEFT, anchor = NW)
        self.register_button = Button(self, text='Register', font=5, width=10, command = lambda: controller.show_frame(RegisterPage)).pack(side = LEFT, anchor = NW)

        # create LoginPage label
        self.login_label = Label(self, text='Welcome to the login section', font=14).place(anchor = N, relx = 0.5, rely =0.2)

        # username
        self.username_label = Label(self, text = 'Username: ', font = 10).place(anchor = N, relx = 0.3, rely =0.4)
        self.username_entry = Entry(self,  width = 30)
        self.username_entry.place(anchor = N, relx = 0.6, rely =0.4)

        # password
        self.password_label = Label(self, text = 'Password: ', font = 10).place(anchor = N, relx = 0.3, rely =0.55)
        self.password_entry = Entry(self, width = 30, show = '*')
        self.password_entry.place(anchor = N, relx = 0.6, rely =0.55)

        # submit button
        self.submit_button = Button(self, text='Submit', font=5, width=20, height=1, command = lambda: self.login_verify(controller) ).place(anchor=N, relx=0.5, rely=0.8)

        # creating a variable for entry widget
        self.text = StringVar()
        self.text.set('')

    def login_verify(self,cont):
        """ Method that verify given input. """
        # create global variable
        global username

        # save entries as variables
        username = self.username_entry.get()
        password = self.password_entry.get()

        # setting text to blank before new login session
        self.text.set('')

        # checks if username is exists and if it match the password 
        my_cursor.execute("SELECT username FROM Players WHERE username = ?", (username, ))
        username_query = my_cursor.fetchall()
        if username_query:
            my_cursor.execute("SELECT password FROM Players WHERE username = ?", (username, ))
            password_query_result = my_cursor.fetchall()
            if password == password_query_result[0][0]:
                # LoginPage.place_forget(cont)
                cont.show_frame(LoggedUser)
            else:
                self.text.set('Incorrect password!')
        else:
            self.text.set('User not found!')

        # display login outcome
        self.verify_label = Label(self, textvariable = self.text, font=10, fg='red').place(anchor=N, relx=0.5, rely=0.67)

        # clear the entry 
        self.username_entry.delete(0, END)
        self.password_entry.delete(0, END)


class LoggedUser(Frame):
    """ Page with actions that user could need. """
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        # create buttons in upper left corner for logout
        self.start_page_button = Button(self, text='Log out', font=5, width=10, command=lambda: controller.show_frame(StartPage)).pack(side=LEFT, anchor=NW)

        # button that starts the game
        self.play_button = Button(self, text='Play', font=10, width=30, height=2, command= self.play_the_game).place(anchor=N, relx=0.5, rely=0.25)

        # button that shows user's scores
        self.user_scores_button = Button(self, text='Show my scores', font=10, width=30, height=2, command=lambda: controller.show_frame(MyScores)).place(anchor=N, relx=0.5, rely=0.5)

        # button that shows best scores
        self.leaderboard_button = Button(self, text='Leaderboard', font=10, width=30, height=2, command=lambda: controller.show_frame(Leaderboard)).place(anchor=N, relx=0.5, rely=0.75)

        # bind method to an event
        self.bind("<<ShowFrame>>", self.on_show_frame)

    def play_the_game(self):
        """ starts the game and save it's result to the database"""
        Game.the_game()
        my_cursor.execute("INSERT INTO Scores (username, score) VALUES (?, ?)", ( username, Game.pass_score()))
        mydb.commit()

    def on_show_frame(self, *args):
        """ Method allows to refresh frame with proper username displayed. """
        self.logged_user_label = Label(self, text="Welcome to Your account\n" + username, font=14, fg='green').place(anchor=N, relx=0.5, rely=0.05)


class MyScores(Frame):
    """ Page that shows user's best scores. """
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        # create buttons in upper left corner for navigation
        self.start_page_button = Button(self, text='Log out', font=5, width=10, command=lambda: controller.show_frame(StartPage)).pack(side=LEFT, anchor=NW)
        self.back_button = Button(self, text='Back', font=5, width=10, command=lambda: controller.show_frame(LoggedUser)).pack(side=LEFT, anchor=NW)

        # bind method to an event
        self.bind("<<ShowFrame>>", self.on_show_frame)

    def on_show_frame(self, *args):
        """ Method allows to display frame with scores belonging to proper user. """
        # get data from database in descending order
        my_cursor.execute("SELECT score FROM Scores WHERE username = ? ORDER BY score DESC LIMIT 10", (username, ))
        top_scores = my_cursor.fetchall()

        Label(self, text="Top 10 best scores for " + username, font=14, fg='green').place(anchor=N, relx=0.5, rely=0.15)

        # display scores
        i=1
        if top_scores:
            for score in top_scores:
                self.scores_list = Label(self, text='%d' % (score[0])).place(anchor=N, relx=0.5, rely=0.2 + i/15)
                i += 1



class Leaderboard(Frame):
    """ Page that shows all best scores. """
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        # create buttons in upper left corner for navigation
        self.start_page_button = Button(self, text='Log out', font=5, width=10, command=lambda: controller.show_frame(StartPage)).pack(side=LEFT, anchor=NW)
        self.back_button = Button(self, text='Back', font=5, width=10, command=lambda: controller.show_frame(LoggedUser)).pack(side=LEFT, anchor=NW)

        # bind method to an event
        self.bind("<<ShowFrame>>", self.on_show_frame)

    def on_show_frame(self, *args):
        """ Method allows to display frame with scores belonging to proper user. """
        # get data from database in descending order
        my_cursor.execute("SELECT score , username FROM Scores ORDER BY score DESC LIMIT 10")
        top_scores = my_cursor.fetchall()

        Label(self, text="Top 10 best scores", font=14, fg='green').place(anchor=N, relx=0.5, rely=0.15)
        Label(self, text = "Username\tScore").place(anchor=N, relx=0.5, rely=0.225)

        # display scores
        i=1
        if top_scores:
            for score in top_scores:
                self.scores_list = Label(self, text='%s\t\t%d' % (score[1], score[0])).place(anchor=N, relx=0.5, rely=0.25 + i/15)
                i += 1



# create an instance
app = Page()
# set the window geometry
app.geometry('500x300')
# set window title
app.title('Space Journey Login System')
app.mainloop()
