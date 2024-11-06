import datetime
import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import HIDDEN, NORMAL
from tkcalendar import Calendar  # Import for the calendar


class Task:
    def __init__(self, title, description, due_date):
        self.title = title
        self.description = description
        self.due_date = due_date
        self.completed = False
        self.priority = "Normal"
        self.on_hold = False
        self.comments = []

    def set_priority(self, priority):
        """Sets the priority of the task."""
        if priority in ["High", "Normal", "Low"]:
            self.priority = priority
        else:
            raise ValueError("Invalid priority")

    def mark_as_completed(self):
        """Marks the task as completed."""
        self.completed = True

    def __str__(self):
        """Returns a string representation of the task."""
        status = "Completed" if self.completed else "In Progress"
        hold_status = "On Hold" if self.on_hold else "Active"
        comments = "\n  Comments: " + "; ".join(self.comments) if self.comments else ""
        return (f"{self.title} - {self.description} "
                f"(Due: {self.due_date}, Status: {status}, "
                f"Priority: {self.priority}, State: {hold_status}){comments}")


class TaskManager:
    def __init__(self):
        self.tasks = []

    def hold_task(self, title):
        """Pauses the task by title."""
        for task in self.tasks:
            if task.title == title:
                task.on_hold = True
                return f"Task '{title}' has been paused."
        return f"Task '{title}' not found."

    def resume_task(self, title):
        """Resumes the task by title."""
        for task in self.tasks:
            if task.title == title:
                task.on_hold = False
                return f"Task '{title}' has been resumed."
        return f"Task '{title}' not found."

    def sort_tasks_by_priority(self):
        """Sorts tasks by priority."""
        self.tasks.sort(key=lambda task: {"High": 1, "Normal": 2, "Low": 3}[task.priority])
        return "Tasks sorted by priority."

    def sort_tasks_by_due_date(self):
        """Sorts tasks by due date."""
        self.tasks.sort(key=lambda task: task.due_date)
        return "Tasks sorted by due date."

    def add_comment_to_task(self, title, comment):
        """Adds a comment to the task."""
        for task in self.tasks:
            if task.title == title:
                task.comments.append(comment)
                return f"Comment added to task '{title}'."
        return f"Task '{title}' not found."

    def add_task(self, title, description, due_date, priority):
        """Adds a new task."""
        task = Task(title, description, due_date)
        task.set_priority(priority)
        self.tasks.append(task)
        return f"Task '{title}' added with priority '{priority}'."

    def list_tasks(self):
        """Returns the list of tasks."""
        if not self.tasks:
            return "The task list is empty."
        return "\n".join([f"- {task}" for task in self.tasks])

    def mark_task_as_completed(self, title):
        """Marks the task as completed by title."""
        for task in self.tasks:
            if task.title == title:
                task.mark_as_completed()
                return f"Task '{title}' has been marked as completed."
        return f"Task '{title}' not found."

    def delete_task(self, title):
        """Deletes the task by title."""
        for task in self.tasks:
            if task.title == title:
                self.tasks.remove(task)
                return f"Task '{title}' has been deleted."
        return f"Task '{title}' not found."

    def search_task(self, keyword):
        """Searches for a task by keyword."""
        results = [task for task in self.tasks if keyword.lower() in task.title.lower()]
        if not results:
            return f"No tasks found with the keyword '{keyword}'."
        return "\n".join([f"- {task}" for task in results])


class TaskManagerApp(tk.Tk):
    def __init__(self, task_manager):
        super().__init__()
        self.task_manager = task_manager
        self.title("Task Manager with Cat")
        self.configure(bg="#f4f4f9")
        self.geometry("1000x800")  # Increased window size
        self.priority_var = tk.StringVar(value="Normal")  # Variable for priority
        self.create_widgets()
        self.create_pet()

    def create_widgets(self):
        """Creates the application widgets."""
        self.title_label = tk.Label(
            self,
            text="Task Manager",
            font=("Arial", 20, "bold"),
            bg="#f4f4f9",
            fg="#333"
        )
        self.title_label.pack(pady=10)

        self.task_list = tk.Text(
            self,
            height=10,
            width=80,
            wrap="word",
            font=("Arial", 10)
        )
        self.task_list.pack(pady=10)
        self.task_list.config(state=tk.DISABLED)

        self.show_tasks()

        button_frame = tk.Frame(self, bg="#f4f4f9")
        button_frame.pack(pady=10)

        self.add_task_button = tk.Button(
            button_frame,
            text="Add Task",
            command=self.open_add_task_window,
            bg="#4CAF50",
            fg="white",
            width=25
        )
        self.add_task_button.grid(row=0, column=0, padx=5, pady=5)

        self.show_tasks_button = tk.Button(
            button_frame,
            text="Show All Tasks",
            command=self.show_tasks,
            bg="#2196F3",
            fg="white",
            width=25
        )
        self.show_tasks_button.grid(row=0, column=1, padx=5, pady=5)

        self.delete_task_button = tk.Button(
            button_frame,
            text="Delete Task",
            command=self.delete_task,
            bg="#F44336",
            fg="white",
            width=25
        )
        self.delete_task_button.grid(row=1, column=0, padx=5, pady=5)

        self.complete_task_button = tk.Button(
            button_frame,
            text="Complete Task",
            command=self.complete_task,
            bg="#9C27B0",
            fg="white",
            width=25
        )
        self.complete_task_button.grid(row=1, column=1, padx=5, pady=5)

        self.search_task_button = tk.Button(
            button_frame,
            text="Search Task",
            command=self.search_task,
            bg="#FF9800",
            fg="white",
            width=25
        )
        self.search_task_button.grid(row=2, column=0, padx=5, pady=5)

        self.hold_task_button = tk.Button(
            button_frame,
            text="Hold Task",
            command=self.hold_task,
            bg="#FF6347",
            fg="white",
            width=25
        )
        self.hold_task_button.grid(row=2, column=1, padx=5, pady=5)

        self.resume_task_button = tk.Button(
            button_frame,
            text="Resume Task",
            command=self.resume_task,
            bg="#32CD32",
            fg="white",
            width=25
        )
        self.resume_task_button.grid(row=3, column=0, padx=5, pady=5)

        self.sort_priority_button = tk.Button(
            button_frame,
            text="Sort by Priority",
            command=self.sort_by_priority,
            bg="#8B0000",
            fg="white",
            width=25
        )
        self.sort_priority_button.grid(row=3, column=1, padx=5, pady=5)

        self.sort_due_date_button = tk.Button(
            button_frame,
            text="Sort by Due Date",
            command=self.sort_by_due_date,
            bg="#1E90FF",
            fg="white",
            width=25
        )
        self.sort_due_date_button.grid(row=4, column=0, padx=5, pady=5)

        self.add_comment_button = tk.Button(
            button_frame,
            text="Add Comment",
            command=self.add_comment,
            bg="#FFD700",
            fg="black",
            width=25
        )
        self.add_comment_button.grid(row=4, column=1, padx=5, pady=5)

    def create_pet(self):
        """Creates a visual representation of the pet."""
        self.canvas = tk.Canvas(
            self,
            width=200,
            height=100,
            bg="lightgreen",
            highlightthickness=0
        )  # Canvas dimensions remain reduced
        self.canvas.pack(anchor="n", padx=10, pady=10)  # Changed anchor to "n" (north) and added padding

        self.canvas.body_color = "magenta"

        # The pet parameters remain unchanged
        self.body = self.canvas.create_oval(
            10, 5, 190, 95,
            outline=self.canvas.body_color,
            fill=self.canvas.body_color
        )
        self.ear_left = self.canvas.create_polygon(
            30, 0, 30, 15, 15, 5,
            outline=self.canvas.body_color,
            fill=self.canvas.body_color
        )
        self.ear_right = self.canvas.create_polygon(
            170, 0, 170, 15, 185, 5,
            outline=self.canvas.body_color,
            fill=self.canvas.body_color
        )
        self.eye_left = self.canvas.create_oval(40, 35, 55, 50, outline="black", fill="white")
        self.pupil_left = self.canvas.create_oval(45, 40, 50, 45, outline="black", fill="black")
        self.eye_right = self.canvas.create_oval(145, 35, 160, 50, outline="black", fill="white")
        self.pupil_right = self.canvas.create_oval(150, 40, 155, 45, outline="black", fill="black")
        self.mouth_normal = self.canvas.create_line(60, 75, 100, 85, 140, 75, smooth=1, width=2)
        self.mouth_happy = self.canvas.create_line(60, 75, 100, 95, 140, 75, smooth=1, width=2, state=HIDDEN)
        self.cheek_left = self.canvas.create_oval(35, 65, 45, 75, outline="pink", fill="pink", state=HIDDEN)
        self.cheek_right = self.canvas.create_oval(155, 65, 165, 75, outline="pink", fill="pink", state=HIDDEN)

        self.toggle_eyes()
        self.canvas.bind('<Motion>', self.show_happy)
        self.canvas.bind('<Leave>', self.hide_happy)

    def sort_by_priority(self):
        """Sorts the tasks by priority."""
        result = self.task_manager.sort_tasks_by_priority()
        messagebox.showinfo("Result", result)
        self.show_tasks()

    def sort_by_due_date(self):
        """Sorts the tasks by due date."""
        result = self.task_manager.sort_tasks_by_due_date()
        messagebox.showinfo("Result", result)
        self.show_tasks()

    def add_comment(self):
        """Adds a comment to the selected task."""
        title = simpledialog.askstring("Add Comment", "Enter the task title:")
        if title:
            comment = simpledialog.askstring("Comment", "Enter the comment:")
            if comment:
                result = self.task_manager.add_comment_to_task(title, comment)
                messagebox.showinfo("Result", result)
                self.show_tasks()

    def toggle_eyes(self):
        """Toggles the eyes of the pet animation."""
        current_color = self.canvas.itemcget(self.eye_left, 'fill')
        new_color = self.canvas.body_color if current_color == "white" else "white"
        current_state = self.canvas.itemcget(self.pupil_left, 'state')
        new_state = NORMAL if current_state == HIDDEN else HIDDEN

        self.canvas.itemconfigure(self.pupil_left, state=new_state)
        self.canvas.itemconfigure(self.pupil_right, state=new_state)
        self.canvas.itemconfigure(self.eye_left, fill=new_color)
        self.canvas.itemconfigure(self.eye_right, fill=new_color)
        self.after(500, self.toggle_eyes)

    def show_happy(self, event):
        """Shows the happy expression of the pet when hovered over."""
        if 35 < event.x < 265 and 20 < event.y < 250:
            self.canvas.itemconfigure(self.cheek_left, state=NORMAL)
            self.canvas.itemconfigure(self.cheek_right, state=NORMAL)
            self.canvas.itemconfigure(self.mouth_happy, state=NORMAL)
            self.canvas.itemconfigure(self.mouth_normal, state=HIDDEN)

    def hide_happy(self, event):
        """Hides the happy expression of the pet when not hovered."""
        self.canvas.itemconfigure(self.cheek_left, state=HIDDEN)
        self.canvas.itemconfigure(self.cheek_right, state=HIDDEN)
        self.canvas.itemconfigure(self.mouth_happy, state=HIDDEN)
        self.canvas.itemconfigure(self.mouth_normal, state=NORMAL)

    def open_add_task_window(self):
        """Opens a window to add a new task."""
        add_task_window = tk.Toplevel(self)
        add_task_window.title("Add Task")
        add_task_window.geometry("500x500")  # Increased window size for task input

        tk.Label(add_task_window, text="Task Title:").pack(pady=5)
        title_entry = tk.Entry(add_task_window, width=50)
        title_entry.pack(pady=5)

        tk.Label(add_task_window, text="Task Description:").pack(pady=5)
        description_entry = tk.Entry(add_task_window, width=50)
        description_entry.pack(pady=5)

        tk.Label(add_task_window, text="Due Date:").pack(pady=5)
        calendar = Calendar(add_task_window, selectmode="day")
        calendar.pack(pady=5)

        tk.Label(add_task_window, text="Priority:").pack(pady=5)
        priority_frame = tk.Frame(add_task_window)
        priority_frame.pack(pady=5)
        tk.Radiobutton(priority_frame, text="High", variable=self.priority_var, value="High").pack(side=tk.LEFT)
        tk.Radiobutton(priority_frame, text="Normal", variable=self.priority_var, value="Normal").pack(side=tk.LEFT)
        tk.Radiobutton(priority_frame, text="Low", variable=self.priority_var, value="Low").pack(side=tk.LEFT)

        tk.Button(add_task_window,
                  text="Add",
                  command=lambda: self.add_task(title_entry, description_entry, calendar))\
            .pack(pady=10)

    def add_task(self, title_entry, description_entry, calendar):
        """Adds a task using the input from the task form."""
        title = title_entry.get()
        description = description_entry.get()
        due_date = calendar.get_date()  # Get the date in MM/DD/YY format
        due_date = datetime.datetime.strptime(due_date, "%m/%d/%y").strftime("%Y-%m-%d")

        priority = self.priority_var.get()

        try:
            # Convert the date from string to date object using the format "YYYY-MM-DD"
            due_date = datetime.datetime.strptime(due_date, "%Y-%m-%d").date()
            result = self.task_manager.add_task(title, description, due_date, priority)
            messagebox.showinfo("Success", result)
            self.show_tasks()
        except ValueError:
            messagebox.showerror("Error", "Invalid date format.")

    def show_tasks(self):
        """Displays the current list of tasks."""
        self.task_list.config(state=tk.NORMAL)
        self.task_list.delete(1.0, tk.END)
        self.task_list.insert(tk.END, self.task_manager.list_tasks())
        self.task_list.config(state=tk.DISABLED)

    def delete_task(self):
        """Deletes the specified task."""
        title = simpledialog.askstring("Delete Task", "Enter the task title:")
        if title:
            result = self.task_manager.delete_task(title)
            messagebox.showinfo("Result", result)
            self.show_tasks()

    def complete_task(self):
        """Marks the specified task as completed."""
        title = simpledialog.askstring("Complete Task", "Enter the task title:")
        if title:
            result = self.task_manager.mark_task_as_completed(title)
            messagebox.showinfo("Result", result)
            self.show_tasks()

    def search_task(self):
        """Searches for a task using the provided keyword."""
        keyword = simpledialog.askstring("Search Task", "Enter a keyword for search:")
        if keyword:
            result = self.task_manager.search_task(keyword)
            messagebox.showinfo("Search Result", result)

    def hold_task(self):
        """Pauses the specified task."""
        title = simpledialog.askstring("Hold Task", "Enter the task title:")
        if title:
            result = self.task_manager.hold_task(title)
            messagebox.showinfo("Result", result)
            self.show_tasks()

    def resume_task(self):
        """Resumes the specified task."""
        title = simpledialog.askstring("Resume Task", "Enter the task title:")
        if title:
            result = self.task_manager.resume_task(title)
            messagebox.showinfo("Result", result)
            self.show_tasks()


if __name__ == "__main__":
    task_manager = TaskManager()
    app = TaskManagerApp(task_manager)
    app.mainloop()
