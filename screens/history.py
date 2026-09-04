"""Tela HISTORICO: treinos finalizados, do mais recente para o mais antigo."""

from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivymd.uix.screen import MDScreen

from config import theme
from config.ranks import BODY_PARTS
from services.storage import storage
from widgets.components import Card, barra_superior, texto_simples, titulo


class CardHistorico(Card):
    def __init__(self, entrada, **kwargs):
        kwargs.setdefault("size_hint_y", None)
        kwargs.setdefault("height", dp(100))
        kwargs.setdefault("spacing", dp(5))
        super().__init__(**kwargs)

        cabecalho = BoxLayout(size_hint_y=None, height=dp(24), spacing=dp(8))
        cabecalho.add_widget(titulo(entrada.get("treino", "Treino"), tamanho=14))
        cabecalho.add_widget(texto_simples(
            entrada.get("data", ""), tamanho=11, cor=theme.TEXT_MUTED,
            halign="right", size_hint_x=None, width=dp(80),
        ))
        self.add_widget(cabecalho)

        self.add_widget(texto_simples(
            f'{entrada.get("exercicios_concluidos", 0)} exercicios concluidos',
            tamanho=12, cor=theme.TEXT_DIM,
        ))

        ganhos = entrada.get("xp", {})
        resumo = "   ".join(
            f'{BODY_PARTS.get(c, {}).get("label", c.upper())} +{v}'
            for c, v in ganhos.items()
        )
        self.add_widget(texto_simples(resumo or "-", tamanho=11, cor=theme.ACCENT))


class HistoryScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.md_bg_color = theme.BG

        raiz = BoxLayout(
            orientation="vertical",
            padding=(dp(theme.PADDING), dp(20), dp(theme.PADDING), dp(theme.PADDING)),
            spacing=dp(theme.GAP),
        )
        raiz.add_widget(barra_superior(
            "HISTORICO", lambda: setattr(self.manager, "current", "home")
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
        self.lista.clear_widgets()

        if not storage.historico:
            self.lista.add_widget(texto_simples(
                "Nenhum treino finalizado ainda.",
                tamanho=13, cor=theme.TEXT_MUTED, height=dp(40),
            ))
            return

        for entrada in storage.historico:
            self.lista.add_widget(CardHistorico(entrada))
