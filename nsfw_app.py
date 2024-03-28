from kivy.app import App
from kivy.core.window import Window
from kivy.graphics import Line, Color
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserIconView
import os

class Background(BoxLayout):
    def __init__(self):
        super(Background, self).__init__()
        self.width = Window.size[0]
        self.height = Window.size[1]
        self.add_gradient()

    def add_gradient(self):
        alpha_channel_rate = 0
        increase_rate = 1 / self.height  # Change here

        for sep in range(self.height):   # Change here
            # Adjusting color values for the gradient
            red_value = 1 - alpha_channel_rate
            green_value = 1 - alpha_channel_rate
            blue_value = 1 - alpha_channel_rate
            self.canvas.add(Color(rgba=(red_value, green_value, blue_value, 1)))
            self.canvas.add(Line(points=[0, sep, self.width, sep], width=0.25))  # Change here
            alpha_channel_rate += increase_rate


class NSFW_App(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')

        # Get the path to the font file
        font_path = os.path.join(os.getcwd(), 'fonts', 'HelveticaNeueBold.ttf')

        # Add NSFW detector label with font change
        nsfw_label = Label(text='NSFW Detector', size_hint_y=None, height=100, color=(1, 1, 1, 1), font_name=font_path, font_size='30sp')  # Change font size here
        layout.add_widget(nsfw_label)

        # Add spacing
        layout.add_widget(Label(size_hint_y=None, height=200))  # Adding space

        # Add file upload button
        file_upload_button = Button(text='Upload File', size_hint_y=None)
        file_upload_button.bind(on_press=self.show_file_chooser)
        layout.add_widget(file_upload_button)

        # Add background with gradient
        background = Background()
        layout.add_widget(background)

        return layout

    def show_file_chooser(self, instance):
        file_chooser = FileChooserIconView()
        file_chooser.path = os.getcwd()
        file_chooser.bind(on_submit=self.handle_file_selection)
        popup = Popup(title="Choose a file", content=file_chooser, size_hint=(0.9, 0.9))
        popup.open()

    def handle_file_selection(self, instance, selected_file):
        print("Selected file:", selected_file[0])

if __name__ == "__main__":
    NSFW_App().run()
