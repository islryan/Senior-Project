import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
import os

# Load the model outside the Kivy App class
model_path = 'C:/Users/ambar/OneDrive/Documents/nsfw_model-master/nsfw_mobilenet2.224x224.h5'  # Update this path
model = load_model(model_path)
categories = ['Drawings', 'Hentai', 'Neutral', 'Porn', 'Sexy']

def classify_image(image_path, model):
    img = image.load_img(image_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array_expanded_dims = np.expand_dims(img_array, axis=0)
    return model.predict(preprocess_input(img_array_expanded_dims))

class NSFW_App(App):
    def build(self):
        self.title = 'NSFW Image Classifier'
        layout = BoxLayout(orientation='vertical')
        self.label = Label(text='NSFW Detector', size_hint_y=None, height=50)
        layout.add_widget(self.label)
        file_upload_button = Button(text='Upload File', size_hint_y=None, height=50)
        file_upload_button.bind(on_press=self.show_file_chooser)
        layout.add_widget(file_upload_button)
        return layout

    def show_file_chooser(self, instance):
        home_path = os.path.expanduser('~')  # Starts at the user's home directory
        self.file_chooser = FileChooserIconView(multiselect=True)  # Enable multiselect
        self.file_chooser.path = home_path

        # Create the layout for the popup
        chooser_layout = BoxLayout(orientation='vertical', spacing=5)
        chooser_layout.add_widget(self.file_chooser)
        
        # Add the "Analyze these images" button
        analyze_button = Button(text='Analyze these images', size_hint_y=None, height=50)
        analyze_button.bind(on_press=self.trigger_file_analysis)
        
        chooser_layout.add_widget(analyze_button)

        # Create the file chooser popup
        self.chooser_popup = Popup(title="Choose files", content=chooser_layout, size_hint=(0.9, 0.9))
        self.chooser_popup.open()

    def trigger_file_analysis(self, instance):
        # Close the file chooser popup and pass the selected files to the analysis method
        self.chooser_popup.dismiss()
        selected_files = self.file_chooser.selection
        self.handle_file_selection(instance, selected_files, None)

    def handle_file_selection(self, instance, selected_files, touch):
        # Container for the results
        results_container = BoxLayout(orientation='vertical', size_hint_y=None, spacing=5)
        # This line will ensure the results container can grow as needed
        results_container.bind(minimum_height=results_container.setter('height'))

        # Scroll view to contain the results container
        scroll_view = ScrollView(size_hint=(1, 1), size=(Window.width, Window.height * 0.8), bar_width=10)

        # Calculate the height for the labels
        label_height = 30  # adjust the height as needed
        for image_path in selected_files:
            results = classify_image(image_path, model)
            results_str = f"Results for {os.path.basename(image_path)}:\n" + \
                          "\n".join([f" - {cat}: {score*100:.2f}%" for cat, score in zip(categories, results[0])]) + "\n"
            # Calculate the total height required for this label based on the number of lines (results)
            total_label_height = label_height * (results_str.count('\n') + 1)
            result_label = Label(text=results_str, size_hint_y=None, height=total_label_height)
            results_container.add_widget(result_label)

        # Add the results container to the scroll view
        scroll_view.add_widget(results_container)

        # Main layout for the popup content
        results_popup_content = BoxLayout(orientation='vertical')
        results_popup_content.add_widget(scroll_view)

        # Button to close the results popup
        close_button = Button(text='Close', size_hint_y=None, height=50)
        close_button.bind(on_press=lambda x: results_popup.dismiss())
        results_popup_content.add_widget(close_button)

        # Popup to display the results
        results_popup = Popup(title="Analysis Results", content=results_popup_content, size_hint=(0.9, 0.9))
        results_popup.open()

if __name__ == "__main__":
    NSFW_App().run()
