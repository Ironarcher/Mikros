import kivy
kivy.require("1.9.0")

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.stacklayout import StackLayout

class Bubble(Widget):
	pass

class MainLayout(StackLayout):
	pass

class UIApp(App):
	def build(self):
		lay = StackLayout()
		btn = Button(text="hello", width=40, height=40)
		btn2 = Button(text="sup", width=40, height=40)
		lay.add_widget(btn)
		lay.add_widget(btn2)
		return lay

if __name__ == "__main__":
	UIApp().run()