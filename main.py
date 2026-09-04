"""IRON ASCENT - ponto de entrada.

Este arquivo so monta o app e registra as telas.
Toda a logica fica em services/, models/ e screens/.
"""

import os

from kivy.core.window import Window
from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager

from config import theme
from screens.active_training import ActiveTrainingScreen
from screens.body_part_detail import BodyPartDetailScreen
from screens.history import HistoryScreen
from screens.home import HomeScreen
from screens.progress import ProgressScreen
from screens.workout_detail import WorkoutDetailScreen
from screens.workouts import WorkoutsScreen

# No computador, simula o formato de um celular.
# No Android a tela ja e do tamanho certo, entao nao mexemos nela.
NO_ANDROID = "ANDROID_ARGUMENT" in os.environ
if not NO_ANDROID:
    Window.size = (400, 780)


class IronAscentApp(MDApp):
    def build(self):
        self.title = "Iron Ascent"
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Orange"
        Window.clearcolor = theme.BG

        gerenciador = MDScreenManager()
        gerenciador.add_widget(HomeScreen(name="home"))
        gerenciador.add_widget(ProgressScreen(name="progress"))
        gerenciador.add_widget(BodyPartDetailScreen(name="body_part_detail"))
        gerenciador.add_widget(WorkoutsScreen(name="workouts"))
        gerenciador.add_widget(WorkoutDetailScreen(name="workout_detail"))
        gerenciador.add_widget(ActiveTrainingScreen(name="active_training"))
        gerenciador.add_widget(HistoryScreen(name="history"))
        gerenciador.current = "home"
        return gerenciador


if __name__ == "__main__":
    IronAscentApp().run()
