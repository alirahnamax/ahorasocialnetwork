import kivy
from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
import webbrowser
import requests
import os
import pickle

class MainApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical')
        self.image = Image(source='logo.png')
        self.layout.add_widget(self.image)

        self.label = Label(text='ساخته شده توسط علی رهنما', font_size='10sp')
        self.layout.add_widget(self.label)

        Clock.schedule_once(self.check_internet, 5)  # بعد از 5 ثانیه بررسی اینترنت

        self.session = requests.Session()
        self.load_session()  # بارگذاری سشن از فایل

        return self.layout

    def check_internet(self, dt):
        try:
            # بررسی اتصال به اینترنت (پینگ به گوگل)
            requests.get('https://www.google.com', timeout=5)
            self.check_website()
        except requests.ConnectionError:
            self.show_no_connection()

    def check_website(self):
        try:
            # بررسی اتصال به سایت مورد نظر
            response = self.session.get('https://socialnetwork.ahura.life/', timeout=5)
            if response.status_code == 200:
                webbrowser.open('https://socialnetwork.ahura.life/')
            else:
                self.show_website_error()
        except requests.ConnectionError:
            self.show_website_error()

    def show_no_connection(self):
        layout = BoxLayout(orientation='vertical')
        label = Label(text='متاسفانه اینترنت شما قطع میباشد', font_size='20sp')
        layout.add_widget(label)
        self.layout.clear_widgets()
        self.layout.add_widget(layout)

    def show_website_error(self):
        layout = BoxLayout(orientation='vertical')
        label = Label(text='بنظر می‌آید اتصال سایت قطع است', font_size='20sp')
        layout.add_widget(label)
        self.layout.clear_widgets()
        self.layout.add_widget(layout)

    def load_session(self):
        if os.path.exists('session.pkl'):
            with open('session.pkl', 'rb') as f:
                self.session.cookies.update(pickle.load(f))

    def save_session(self):
        with open('session.pkl', 'wb') as f:
            pickle.dump(self.session.cookies, f)

    def on_stop(self):
        self.save_session()  # ذخیره سشن هنگام بستن برنامه

if __name__ == '__main__':
    MainApp().run()
