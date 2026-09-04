"""Tela de um treino: lista, adiciona e remove exercicios."""

from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivymd.uix.label import MDIcon
from kivymd.uix.screen import MDScreen

from config import theme
from config.ranks import BODY_PARTS
from models.exercise import Exercise
from services.storage import storage
from services.xp_system import calcular_xp_exercicio
from widgets.components import (
    BotaoPrincipal, Card, DialogoExercicio, IconeBotao,
    barra_superior, texto_simples, titulo,
)


class CardExercicio(Card):
    def __init__(self, exercicio, ao_remover, **kwargs):
        kwargs.setdefault("size_hint_y", None)
        kwargs.setdefault("height", dp(88))
        kwargs.setdefault("spacing", dp(6))
        super().__init__(**kwargs)

        cabecalho = BoxLayout(size_hint_y=None, height=dp(26), spacing=dp(8))
        cabecalho.add_widget(MDIcon(
            icon=BODY_PARTS[exercicio.categoria]["icon"], theme_text_color="Custom",
            theme_font_size="Custom", font_size=dp(20),
            text_color=theme.STEEL, size_hint=(None, None), size=(dp(20), dp(20)),
            pos_hint={"center_y": 0.5},
        ))
        cabecalho.add_widget(titulo(exercicio.nome, tamanho=14))
        cabecalho.add_widget(IconeBotao(
            icon="delete", font_size=dp(18), text_color=theme.DANGER,
            size=(dp(22), dp(22)), pos_hint={"center_y": 0.5},
            on_release=lambda *_: ao_remover(exercicio),
        ))
        self.add_widget(cabecalho)

        self.add_widget(texto_simples(
            f"{exercicio.series} series  x  {exercicio.repeticoes} reps"
            f"  |  {exercicio.peso:g} kg",
            tamanho=12, cor=theme.TEXT_DIM,
        ))
        self.add_widget(texto_simples(
            f'+{calcular_xp_exercicio(exercicio)} XP '
            f'{BODY_PARTS[exercicio.categoria]["label"]}',
            tamanho=11, cor=theme.ACCENT,
        ))


class WorkoutDetailScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.md_bg_color = theme.BG
        self.treino = None

        raiz = BoxLayout(
            orientation="vertical",
            padding=(dp(theme.PADDING), dp(20), dp(theme.PADDING), dp(theme.PADDING)),
            spacing=dp(theme.GAP),
        )
        self.barra_topo = barra_superior(
            "", lambda: setattr(self.manager, "current", "workouts"),
            acao_icone="plus", ao_acionar=self.adicionar_exercicio,
        )
        raiz.add_widget(self.barra_topo)

        rolagem = ScrollView(do_scroll_x=False, bar_width=dp(2))
        self.lista = BoxLayout(
            orientation="vertical", spacing=dp(theme.GAP),
            size_hint_y=None, padding=(0, dp(4)),
        )
        self.lista.bind(minimum_height=self.lista.setter("height"))
        rolagem.add_widget(self.lista)
        raiz.add_widget(rolagem)

        self.botao_iniciar = BotaoPrincipal(
            texto="INICIAR TREINO", icone="play-circle", destaque=True,
            on_release=lambda *_: self.iniciar(),
        )
        raiz.add_widget(self.botao_iniciar)
        self.add_widget(raiz)

    def definir_treino(self, treino):
        self.treino = treino

    def on_pre_enter(self, *args):
        self.recarregar()

    def recarregar(self):
        self.barra_topo.label_titulo.text = self.treino.nome
        self.lista.clear_widgets()

        if not self.treino.exercicios:
            self.lista.add_widget(texto_simples(
                "Nenhum exercicio ainda.\nToque em + para adicionar.",
                tamanho=13, cor=theme.TEXT_MUTED, height=dp(60),
            ))
            return

        for exercicio in self.treino.exercicios:
            self.lista.add_widget(CardExercicio(exercicio, self.remover_exercicio))

    # --- Acoes --------------------------------------------------------------
    def adicionar_exercicio(self):
        def confirmar(dados):
            storage.adicionar_exercicio(self.treino, Exercise(**dados))
            self.recarregar()

        DialogoExercicio(confirmar).open()

    def remover_exercicio(self, exercicio):
        storage.remover_exercicio(self.treino, exercicio)
        self.recarregar()

    def iniciar(self):
        """Sera ligado a tela de treino ativo na proxima etapa."""
        if self.manager.has_screen("active_training"):
            tela = self.manager.get_screen("active_training")
            tela.definir_treino(self.treino)
            self.manager.current = "active_training"
