import os
import subprocess
import threading
import time

import tkinter as tk
from tkinter import filedialog, ttk

import logging
logging.basicConfig(
    filename='logs.log',  # Имя файла для записи логов
    level=logging.DEBUG,             # Уровень логирования
    format='%(asctime)s - %(levelname)s - %(message)s'  # Формат записи
)


class Execution:
    def change_folder(self):
        """ Changes the current working directory to a selected directory. """
        try:
            new_directory = filedialog.askdirectory() + "/"
            os.chdir(new_directory)
            logging.info(f'Changed working directory to: {new_directory}')
        except Exception as e:
            logging.error(f'Error changing directory: {e}')

    def create_folders(self, input_string: str, time_sleep: int, num_iterations=0, start_pos=0):
        """ Create folders based on the specified names. """
        input_list = input_string.split("\n")
        if num_iterations == 0:
            for item in input_list:
                try:
                    os.mkdir(item)
                    logging.info(f'Created folder: {item}')
                    time.sleep(time_sleep)
                except Exception as error:
                    logging.warning(f'Failed to create folder {item}: {error}')

    def remove_folders(self, input_string: str):
        """ Remove folders based on the specified conditions. """
        input_list = input_string.split("\n")
        for folder in input_list:
            try:
                os.rmdir(folder)
                logging.info(f'Removed folder: {folder}')
            except Exception as error:
                logging.warning(f'Failed to remove folder {folder}: {error}')

    def modify_folders(self, input_string: str):
        """ Modify folder names based on specified conditions. """
        for it in os.listdir(os.getcwd()):
            if os.path.isdir(it):
                try:
                    new_name = it + "_modified"  # Пример изменения имени
                    os.rename(it, new_name)
                    logging.info(f'Modified folder name from {it} to {new_name}')
                except Exception as error:
                    logging.error(f'Error modifying folder {it}: {error}')

    def get_folder_list(self):
        """ Retrieves the list of folders in the current working directory. """
        self.folders_list = ""
        for it in os.listdir(os.getcwd()):
            if os.path.isdir(it):
                self.folders_list += it + "\n"
        logging.info('Retrieved folder list.')


# UI class
class WindowUI:
    """
    Class for creating the user interface of the Mass Directory Manager.

    This class sets up the main window, tabs, and controls for folder management operations.
    It provides a graphical interface for users to create, remove, modify folders,
    and manage the working directory.

    Methods:
        __init__: Initializes the user interface components.
        focus_next_widget: Focuses the next widget in the tab order.
        focus_previous_widget: Focuses the previous widget in the tab order.
        clear_logs: Clears the log text area.
        increment_selector: Toggles the increment mode UI elements.
        new_create_folders: Initiates the creation of folders in a separate thread.
        new_remove_folders: Initiates the removal of folders in a separate thread.
        new_modify_folders: Initiates the modification of folder names in a separate thread.
        new_folders_list: Retrieves and displays the list of folders in the log area.
        new_change_folder: Changes the current working directory.
        new_open_current_folder: Opens the current working directory in the file explorer.
    """
    def __init__(self):
        """
        Initializes the user interface for the Mass Directory Manager.

        Sets up the main window, tabs, and controls for folder management operations.
        """
        self.execution = Execution()

        # global
        width = 700
        height = 600
        self.root = tk.Tk()
        self.root.geometry(f"{width}x{height}")
        self.root.title("Mass Directory Manager")

        tab_control = ttk.Notebook(self.root)
        another_tab_control = ttk.Notebook(self.root)

        self.tab1 = tk.Frame(tab_control)
        self.tab2 = tk.Frame(tab_control)
        self.tab3 = tk.Frame(tab_control)
        self.tab4 = tk.Frame(another_tab_control)

        tab_control.add(self.tab1, text=" Create folders ")
        tab_control.add(self.tab2, text=" Remove folders ")
        tab_control.add(self.tab3, text=" Modify folders ")
        tab_control.pack(side="left", anchor="n", expand=True, fill=tk.BOTH)
        another_tab_control.add(self.tab4, text="Output")
        another_tab_control.pack(side="right", anchor="n", expand=True, fill=tk.BOTH)

        self.root.bind("<Escape>", lambda y: self.root.geometry(f"{width}x{height}"))
        self.root.bind("<F1>", lambda z: tab_control.select(self.tab1))
        self.root.bind("<F2>", lambda z: tab_control.select(self.tab2))
        self.root.bind("<F3>", lambda z: tab_control.select(self.tab3))

        # tab1 - create folders

        text_box_1 = tk.Text(self.tab1, width=40)
        text_box_1.pack(expand=True, fill=tk.BOTH)

        button_go_1 = tk.Button(self.tab1, text="Go!",
                              command=lambda: [self.new_create_folders(text_box_1.get("1.0",
                                                                                      'end-1c'), v1.get())])
        button_go_1.pack(side="bottom", pady=10)

        v1 = tk.DoubleVar()

        timeout_text = tk.Label(self.tab1, text="Time to pause between actions (in seconds)")
        timeout_text.pack()
        timeout_slider = tk.Scale(self.tab1, variable=v1, from_=0, to=60, orient=tk.HORIZONTAL)
        timeout_slider.pack(anchor=tk.CENTER, expand=True, fill=tk.BOTH)

        self.increment_variable = tk.IntVar()

        increment_button_1 = tk.Checkbutton(self.tab1, text="Increment mode", variable=self.increment_variable,
                                            onvalue=1, offvalue=0,
                                            command=lambda: [self.increment_selector(self.tab1)])
        increment_button_1.pack(side="left", anchor="sw")

        # tab2 - remove folders

        test_box_2 = tk.Text(self.tab2, width=40)
        test_box_2.pack(expand=True, fill=tk.BOTH)

        v4 = tk.IntVar()

        startswith_1 = tk.Checkbutton(self.tab2, text="Starts with", variable=v4, onvalue=1, offvalue=0)
        startswith_1.pack()
        endswith_1 = tk.Checkbutton(self.tab2, text="Ends with", variable=v4, onvalue=2, offvalue=0)
        endswith_1.pack()

        entry_box_1 = tk.Entry(self.tab2)
        entry_box_1.pack()

        button_go_2 = tk.Button(self.tab2, text="Go!", command=lambda: [
            self.new_remove_folders(test_box_2.get("1.0", 'end-1c'), v4.get(), entry_box_1.get())])
        button_go_2.pack(side="bottom", pady=10)

        increment_button_2 = tk.Checkbutton(self.tab2, text="Increment mode", variable=self.increment_variable,
                                            onvalue=1, offvalue=0,
                                            command=lambda: [self.increment_selector(self.tab2)])
        increment_button_2.pack(side="left", anchor="sw")

        # tab3 - modify folders

        v2 = tk.IntVar()

        startswith = tk.Checkbutton(self.tab3, text="Starts with", variable=v2, onvalue=1, offvalue=0)
        startswith.pack()
        endswith = tk.Checkbutton(self.tab3, text="Ends with", variable=v2, onvalue=2, offvalue=0)
        endswith.pack()

        entry_box_2 = tk.Entry(self.tab3)
        entry_box_2.pack()

        replace_label = tk.Label(self.tab3, text="Replace with:")
        replace_label.pack()
        entry_box_3 = tk.Entry(self.tab3)
        entry_box_3.pack()

        v3 = tk.DoubleVar()

        timeout_text2 = tk.Label(self.tab3, text="Time to pause between actions (in seconds)")
        timeout_text2.pack()
        timeout_slider = tk.Scale(self.tab3, variable=v3, from_=0, to=60, orient=tk.HORIZONTAL)
        timeout_slider.pack(anchor=tk.CENTER, expand=True, fill=tk.BOTH)

        button_go_3 = tk.Button(self.tab3, text="Go!", command=lambda: [
            self.new_modify_folders(entry_box_2.get(), v2.get(), entry_box_3.get(), v3.get())])
        button_go_3.pack(side="bottom", pady=10)

        # tab4 - output

        self.logs = tk.Text(self.tab4, state='normal', wrap='none', width=33)
        self.logs.pack(expand=True, fill=tk.BOTH)
        self.logs.configure(state="disabled")

        button_clear_logs = tk.Button(self.tab4, text="Clear logs", command=self.clear_logs)
        button_clear_logs.pack(padx=10, pady=5)

        button_folder_list = tk.Button(self.tab4, text="Get folders list", command=self.new_folders_list)
        button_folder_list.pack(padx=10, pady=5)

        button_select_folder = tk.Button(self.tab4, text="Change working folder", command=self.new_change_folder)
        button_select_folder.pack(padx=10, pady=5)

        button_open_folder = tk.Button(self.tab4, text="Explore working folder", command=self.new_open_current_folder)
        button_open_folder.pack(padx=10, pady=5)

        button_quit = tk.Button(self.tab4, text="Quit!", command=self.root.destroy)
        button_quit.pack(side="bottom", anchor="se", pady=8, padx=8)

    def focus_next_widget(self, event):
        """
        Focuses the next widget in the tab order.

        Args:
            event: The event that triggered this method.

        Returns:
            str: A string indicating to break the event propagation.
        """
        event.widget.tk_focusNext().focus()
        return ("break")

    def focus_previous_widget(self, event):
        """
        Focuses the previous widget in the tab order.

        Args:
            event: The event that triggered this method.

        Returns:
            str: A string indicating to break the event propagation.
        """
        event.widget.tk_focusPrev().focus()
        return ("break")

    def clear_logs(self):
        """
        Clears the log text area.

        Returns:
            None
        """
        self.logs.config(state=tk.NORMAL)
        self.logs.delete('1.0', tk.END)

    def increment_selector(self, selected_tab):
        """
        Toggles the increment mode UI elements in the specified tab.

        Args:
            selected_tab: The tab where the increment mode is being toggled.

        Returns:
            None
        """
        variable = self.increment_variable.get()
        if variable == 1:
            self.label_1 = tk.Label(selected_tab, text="Num to loop")
            self.label_1.pack(side="left", anchor="w", padx=2, expand=True, fill=tk.BOTH)
            self.increment_value = tk.Text(selected_tab, height=1, width=3)
            self.increment_value.pack(side="left", anchor="w", padx=2, expand=True, fill=tk.BOTH)
            self.increment_value.bind("<Tab>", self.focus_next_widget)

            self.label_2 = tk.Label(selected_tab, text="Pos to start")
            self.label_2.pack(side="left", anchor="e", padx=2, expand=True, fill=tk.BOTH)
            self.increment_start = tk.Text(selected_tab, height=1, width=2)
            self.increment_start.pack(side="left", anchor="e", padx=2, expand=True, fill=tk.BOTH)
            self.increment_start.bind("<Tab>", self.focus_next_widget)
        elif variable == 0:
            try:
                self.label_1.destroy()
                self.increment_value.destroy()
                self.label_2.destroy()
                self.increment_start.destroy()
            except Exception as error:
                print(f"Error while destroying widgets: {error}")

    def new_create_folders(self, entry_get="", sleep_value=0):
        """
        Initiates the creation of folders in a separate thread.

        Args:
            entry_get (str): The names of folders to create.
            sleep_value (int): The time to pause between actions.

        Returns:
            None
        """
        try:
            increment_value = self.increment_value.get(1.0, "end-1c")
            increment_start = self.increment_start.get(1.0, "end-1c")
        except Exception as error:
            print(f"Error while getting values: {error}")

            increment_value = 0
            increment_start = 0
        if increment_start == "":
            increment_start = 1
        if increment_value == "":
            increment_value = 0
        if str(increment_value).isdigit():
            increment_value = int(increment_value)
        if str(increment_start).isdigit():
            increment_start = int(increment_start)

        p = threading.Thread(target=self.execution.create_folders(entry_get, sleep_value,
                                                                  increment_value, increment_start))
        p.start()
        self.logs.configure(state="normal")
        self.logs.insert("1.0", f"---------------------------------\n{self.execution.function_outputs}")
        self.logs.configure(state="disabled")

    def new_remove_folders(self, entry_get="", mode_selected=0, starts_endswith=""):
        """
        Initiates the removal of folders in a separate thread.

        Args:
            entry_get (str): The names of folders to remove.
            mode_selected (int): The mode of removal (1 for 'starts with', 2 for 'ends with').
            starts_ends_with (str): The characters to match for removal.

        Returns:
            None
        """
        try:
            increment_value = self.increment_value.get(1.0, "end-1c")
            increment_start = self.increment_start.get(1.0, "end-1c")
        except Exception as error:
            print(f"Error while getting values: {error}")

            increment_value = 0
            increment_start = 0
        if increment_start == "":
            increment_start = 1
        if increment_value == "":
            increment_value = 0
        if str(increment_value).isdigit():
            increment_value = int(increment_value)
        if str(increment_start).isdigit():
            increment_start = int(increment_start)

        p = threading.Thread(
            target=self.execution.remove_folders(entry_get, mode_selected, starts_endswith,
                                                 increment_value, increment_start))
        p.start()
        self.logs.configure(state="normal")
        self.logs.insert("1.0", f"---------------------------------\n{self.execution.function_outputs}")
        self.logs.configure(state="disabled")

    def new_modify_folders(self, entry_get="", mode_selected=0, replace_with="", sleep_value=0):
        """
        Initiates the modification of folder names in a separate thread.

        Args:
            entry_get (str): The string to match against folder names.
            mode_selected (int): Mode selection; 1 for 'starts with', 2 for 'ends with'.
            replace_with (str): The string to replace matched portions of folder names.
            sleep_value (int): Pause time in seconds between modifications.

        Returns:
            None
        """
        p = threading.Thread(target=self.execution.modify_folders(entry_get, mode_selected, replace_with, sleep_value))
        p.start()
        self.logs.configure(state="normal")
        self.logs.insert("1.0", f"---------------------------------\n{self.execution.function_outputs}")
        self.logs.configure(state="disabled")

    def new_folders_list(self):
        """
        Initiates the retrieval of the folder list in a separate thread.

        Updates the logs with the current working directory and the list of folders.

        Returns:
            None
        """
        p = threading.Thread(target=self.execution.get_folder_list())
        p.start()
        self.logs.configure(state="normal")
        self.logs.insert("1.0",
                         f"---------------------------------\nCurrently working on:\n{os.getcwd()}."
                         f"\nFolders list:\n{self.execution.folders_list}")
        self.logs.configure(state="disabled")

    def new_change_folder(self):
        """
        Initiates the change of the working directory in a separate thread.

        Opens a dialog to select a new working directory.

        Returns:
            None
        """
        p = threading.Thread(target=self.execution.change_folder())
        p.start()

    def new_open_current_folder(self):
        """
        Opens the current working directory in the file explorer.

        Returns:
            None
        """
        subprocess.Popen(f'explorer "{os.getcwd()}"')


if __name__ == '__main__':
    startUI = WindowUI()
    startUI.root.mainloop()
