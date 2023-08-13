from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.checkbox import CheckBox
import uuid


class TodoApp(App):
    task_list = []

    def build(self):
        # Set background color to white
        Window.clearcolor = (1, 1, 1, 1)

        # Create the root layout
        root_layout = BoxLayout(orientation='vertical')

        # Create the input box
        input_box = TextInput(size_hint=(1, 0.1), multiline=False, hint_text="Enter task", hint_text_color=(0, 1, 0, 1))
        root_layout.add_widget(input_box)

        # Create the 'Add Task' button
        add_button = Button(text="Add Task", size_hint=(1, 0.1), background_color=(0, 1, 0, 1), color=(1, 1, 1, 1))
        add_button.bind(on_press=lambda button: self.add_task(input_box))
        root_layout.add_widget(add_button)

        # Create the scrollable task list
        scroll_view = ScrollView()
        root_layout.add_widget(scroll_view)

        self.task_list_layout = GridLayout(cols=1, spacing=5, size_hint_y=None)
        self.task_list_layout.bind(minimum_height=self.task_list_layout.setter('height'))
        scroll_view.add_widget(self.task_list_layout)

        # Create the 'Remove Selected' button
        remove_selected_button = Button(text="Remove Selected", size_hint=(1, 0.1),
                                        background_color=(1, 0, 0, 1), color=(1, 1, 1, 1))
        remove_selected_button.bind(on_press=self.remove_selected_tasks)
        root_layout.add_widget(remove_selected_button)

        return root_layout

    def add_task(self, input_box):
        task_text = input_box.text.strip()
        if task_text:
            task_id = str(uuid.uuid4())
            self.task_list.append({"id": task_id, "text": task_text, "selected": False})
            input_box.text = ""
            self.refresh_task_list()

    def remove_task(self, button):
        task_id = button.id
        self.task_list = [task for task in self.task_list if task["id"] != task_id]
        self.refresh_task_list()

    def remove_selected_tasks(self, button):
        self.task_list = [task for task in self.task_list if not task["selected"]]
        self.refresh_task_list()

    def toggle_task_selection(self, checkbox, task_id):
        for task in self.task_list:
            if task["id"] == task_id:
                task["selected"] = checkbox.active

    def refresh_task_list(self):
        self.task_list_layout.clear_widgets()
        for task in self.task_list:
            task_label = Label(text=task["text"], size_hint_y=None, height=40, color=(0, 1, 0, 1))
            self.task_list_layout.add_widget(task_label)

            remove_button = Button(text="Remove", size_hint=(None, None), size=(100, 40),
                                   background_color=(1, 0, 0, 1), color=(1, 1, 1, 1))
            remove_button.bind(on_press=self.remove_task)
            remove_button.id = task["id"]
            self.task_list_layout.add_widget(remove_button)

            checkbox = CheckBox(size_hint=(None, None), size=(40, 40))
            checkbox.bind(active=lambda checkbox, active, task_id=task["id"]:
                          self.toggle_task_selection(checkbox, task_id))
            self.task_list_layout.add_widget(checkbox)

    def on_start(self):
        Window.bind(on_key_down=self.key_action)

    def key_action(self, instance, keyboard, keycode, text, modifiers):
        if keycode == 27:  # Keycode for Escape key
            App.get_running_app().stop()


if __name__ == '__main__':
    TodoApp().run()
