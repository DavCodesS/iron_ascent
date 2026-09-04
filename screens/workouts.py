"""Tela MEUS TREINOS: lista, cria, renomeia e exclui treinos."""

from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivymd.uix.screen import MDScreen

from config import theme
from config.ranks import BODY_PARTS
from services.storage import storage
from services.xp_system import calcular_xp_treino
from widgets.components import (
    CardClicavel, DialogoTexto, IconeBotao, barra_superior, texto_simples, titulo,
)


class CardTreino(CardClicavel):
    def __init__(self, treino, ao_abrir, ao_renomear, ao_excluir, **kwargs):
        kwargs.setdefault("size_hint_y", None)
        kwargs.setdefault("height", dp(92))
        kwargs.setdefault("spacing", dp(6))
        super().__init__(**kwargs)
        self.bind(on_release=lambda *_: ao_abrir(treino))

        cabecalho = BoxLayout(size_hint_y=None, height=dp(26), spacing=dp(8))
        cabecalho.add_widget(titulo(treino.nome, tamanho=15))
        cabecalho.add_widget(IconeBotao(
            icon="pencil", font_size=dp(18), text_color=theme.TEXT_MUTED,
            size=(dp(22), dp(22)), pos_hint={"center_y": 0.5},
            on_release=lambda *_: ao_renomear(treino),
        ))
        cabecalho.add_widget(IconeBotao(
            icon="delete", font_size=dp(18), text_color=theme.DANGER,
            size=(dp(22), dp(22)), pos_hint={"center_y": 0.5},
            on_release=lambda *_: ao_excluir(treino),
        ))
        self.add_widget(cabecalho)

        rotulos = [BODY_PARTS[c]["label"] for c in treino.categorias()]
        self.add_widget(texto_simples(
            " + ".join(rotulos) or "Sem exercicios", tamanho=11, cor=theme.STEEL
        ))

        xp = sum(calcular_xp_treino(treino).values())
        self.add_widget(texto_simples(
            f"{len(treino.exercicios)} exercicios   |   +{xp} XP",
            tamanho=12, cor=theme.TEXT_DIM,
        ))


class WorkoutsScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.md_bg_color = theme.BG

        raiz = BoxLayout(
            orientation="vertical",
            padding=(dp(theme.PADDING), dp(20), dp(theme.PADDING), dp(theme.PADDING)),
            spacing=dp(theme.GAP),
        )
        raiz.add_widget(barra_superior(
            "MEUS TREINOS",
            lambda: setattr(self.manager, "current", "home"),
            acao_icone="plus", ao_acionar=self.criar_treino,
        ))

        rolagem = ScrollView(do_scroll_x=False, bar_width=dp(2))
        self.lista = BoxLayout(
            orientation="vertical", spacing=dp(theme.GAP),
            size_hint_y=None, padding=(0, dp(4)),
        )
        self.lista.bind(minimum_height=self.lista.setter("height"))
        rolagem.add_widget(self.lista)
        raiz.add_widget(rolagem)
        self.add_widget(raiz)

    def on_pre_enter(self, *args):
        self.recarregar()

    def recarregar(self):
        self.lista.clear_widgets()

        if not storage.workouts:
            self.lista.add_widget(texto_simples(
                "Nenhum treino ainda.\nToque em + para criar o primeiro.",
                tamanho=13, cor=theme.TEXT_MUTED, height=dp(60),
            ))
            return

        for treino in storage.workouts:
            self.lista.add_widget(CardTreino(
                treino, self.abrir_treino, self.renomear_treino, self.excluir_treino
            ))

    # --- Acoes --------------------------------------------------------------
    def criar_treino(self):
        def confirmar(nome):
            storage.criar_treino(nome)
            self.recarregar()

        DialogoTexto("NOVO TREINO", confirmar, dica="Ex: PEITO + TRICEPS").open()

    def renomear_treino(self, treino):
        def confirmar(nome):
            storage.editar_treino(treino, nome)
            self.recarregar()

        DialogoTexto("RENOMEAR TREINO", confirmar, valor_inicial=treino.nome).open()

    def excluir_treino(self, treino):
        storage.excluir_treino(treino)
        self.recarregar()

    def abrir_treino(self, treino):
        tela = self.manager.get_screen("workout_detail")
        tela.definir_treino(treino)
        self.manager.current = "workout_detail"
