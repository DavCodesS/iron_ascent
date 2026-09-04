"""Tela MEU PROGRESSO: uma linha para cada divisao corporal."""

from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivymd.uix.label import MDIcon
from kivymd.uix.screen import MDScreen

from config import theme
from config.ranks import BODY_PARTS
from services.rank_system import progresso
from services.storage import storage
from widgets.components import (
    CardClicavel, XPBar, barra_superior, texto_simples, titulo,
)


class LinhaDivisao(CardClicavel):
    """Card resumido de uma divisao corporal."""

    def __init__(self, chave, ao_abrir, **kwargs):
        kwargs.setdefault("size_hint_y", None)
        kwargs.setdefault("height", dp(104))
        kwargs.setdefault("spacing", dp(6))
        super().__init__(**kwargs)
        self.chave = chave
        self.bind(on_release=lambda *_: ao_abrir(chave))

        cabecalho = BoxLayout(size_hint_y=None, height=dp(26), spacing=dp(10))
        self.icone = MDIcon(
            icon=BODY_PARTS[chave]["icon"], theme_text_color="Custom",
            theme_font_size="Custom", font_size=dp(22),
            text_color=theme.ACCENT, size_hint=(None, None), size=(dp(22), dp(22)),
            pos_hint={"center_y": 0.5},
        )
        cabecalho.add_widget(self.icone)
        cabecalho.add_widget(titulo(BODY_PARTS[chave]["label"], tamanho=15))
        self.label_percentual = texto_simples(
            "", tamanho=12, cor=theme.TEXT_MUTED, halign="right",
            size_hint_x=None, width=dp(50),
        )
        cabecalho.add_widget(self.label_percentual)
        self.add_widget(cabecalho)

        self.label_rank = texto_simples("", tamanho=13, cor=theme.TEXT_DIM)
        self.barra = XPBar(segmentos=16)
        self.add_widget(self.label_rank)
        self.add_widget(self.barra)

    def atualizar(self):
        xp = storage.body_part(self.chave)["xp"]
        info = progresso(xp)
        cor_rank = theme.cor(info["rank"]["cor"])

        self.label_rank.text = info["rank"]["nome"]
        self.label_rank.color = cor_rank
        self.label_percentual.text = f'{int(info["percentual"] * 100)}%'
        self.barra.cor = cor_rank
        self.barra.percentual = info["percentual"]
        self.cor_borda = cor_rank
        self.icone.text_color = cor_rank


class ProgressScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.md_bg_color = theme.BG

        raiz = BoxLayout(
            orientation="vertical",
            padding=(dp(theme.PADDING), dp(20), dp(theme.PADDING), dp(theme.PADDING)),
            spacing=dp(theme.GAP),
        )
        raiz.add_widget(barra_superior(
            "MEU PROGRESSO", lambda: setattr(self.manager, "current", "home")
        ))

        rolagem = ScrollView(do_scroll_x=False, bar_width=dp(2))
        lista = BoxLayout(
            orientation="vertical", spacing=dp(theme.GAP),
            size_hint_y=None, padding=(0, dp(4)),
        )
        lista.bind(minimum_height=lista.setter("height"))

        self.linhas = []
        for chave in BODY_PARTS:
            linha = LinhaDivisao(chave, self.abrir_detalhe)
            self.linhas.append(linha)
            lista.add_widget(linha)

        rolagem.add_widget(lista)
        raiz.add_widget(rolagem)
        self.add_widget(raiz)

    def on_pre_enter(self, *args):
        for linha in self.linhas:
            linha.atualizar()

    def abrir_detalhe(self, chave):
        tela = self.manager.get_screen("body_part_detail")
        tela.definir_divisao(chave)
        self.manager.current = "body_part_detail"
