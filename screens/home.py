"""Tela inicial: identidade do app, rank geral e botoes de navegacao."""

from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivymd.uix.screen import MDScreen

from config import theme
from services.rank_system import calcular_rank_geral
from services.storage import storage
from widgets.components import (
    BotaoPrincipal, Card, PainelCorpoAnatomico, XPBar, texto_simples, titulo,
)


class HomeScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.md_bg_color = theme.BG

        raiz = BoxLayout(
            orientation="vertical",
            padding=(dp(theme.PADDING), dp(28), dp(theme.PADDING), dp(theme.PADDING)),
            spacing=dp(theme.GAP),
        )

        # --- Cabecalho ------------------------------------------------------
        raiz.add_widget(titulo("IRON ASCENT", tamanho=30, cor=theme.ACCENT))
        raiz.add_widget(texto_simples(
            "SISTEMA DE PROGRESSAO DE COMBATE", tamanho=11, cor=theme.TEXT_MUTED
        ))
        raiz.add_widget(BoxLayout(size_hint_y=None, height=dp(8)))

        # --- Card do rank geral --------------------------------------------
        self.card_rank = Card(size_hint_y=None, height=dp(148), spacing=dp(7))
        self.label_titulo_rank = texto_simples("RANK GERAL", tamanho=11, cor=theme.TEXT_MUTED)
        self.label_rank = titulo("", tamanho=22, cor=theme.TEXT)
        self.barra = XPBar()
        self.label_xp = texto_simples("", tamanho=12, cor=theme.TEXT_DIM)
        self.label_proximo = texto_simples("", tamanho=11, cor=theme.STEEL)

        for widget in (self.label_titulo_rank, self.label_rank, self.barra,
                       self.label_xp, self.label_proximo):
            self.card_rank.add_widget(widget)
        raiz.add_widget(self.card_rank)

        # --- Visao geral do corpo ------------------------------------------
        self.painel = PainelCorpoAnatomico(ao_tocar=self.abrir_divisao)
        raiz.add_widget(self.painel)

        # --- Navegacao ------------------------------------------------------
        raiz.add_widget(BotaoPrincipal(
            texto="COMECAR TREINO", icone="play-circle", destaque=True,
            on_release=lambda *_: self.ir_para("workouts"),
        ))
        raiz.add_widget(BotaoPrincipal(
            texto="MEU PROGRESSO", icone="chart-line",
            on_release=lambda *_: self.ir_para("progress"),
        ))
        raiz.add_widget(BotaoPrincipal(
            texto="MEUS TREINOS", icone="playlist-check",
            on_release=lambda *_: self.ir_para("workouts"),
        ))
        raiz.add_widget(BotaoPrincipal(
            texto="HISTORICO", icone="history",
            on_release=lambda *_: self.ir_para("history"),
        ))

        raiz.add_widget(BoxLayout(size_hint_y=None, height=dp(8)))
        raiz.bind(minimum_height=raiz.setter("height"))
        raiz.size_hint_y = None

        rolagem = ScrollView(do_scroll_x=False, bar_width=dp(2))
        rolagem.add_widget(raiz)
        self.add_widget(rolagem)

    def on_pre_enter(self, *args):
        """Sempre que a tela aparece, recalcula o rank a partir dos dados."""
        self.atualizar()

    def atualizar(self):
        info = calcular_rank_geral(storage.dados["body_parts"])
        cor_rank = theme.cor(info["rank"]["cor"])

        self.label_rank.text = info["rank"]["nome"]
        self.label_rank.color = cor_rank
        self.barra.cor = cor_rank
        self.barra.animar_para(info["percentual"])
        self.card_rank.cor_borda = cor_rank
        self.painel.atualizar(storage.dados["body_parts"])

        if info["proximo"]:
            self.label_xp.text = (
                f'{info["xp_no_rank"]} / {info["xp_necessario"]} XP  '
                f'(total {info["xp_total"]})'
            )
            self.label_proximo.text = f'PROXIMO: {info["proximo"]["nome"]}'
        else:
            self.label_xp.text = f'{info["xp_total"]} XP TOTAL'
            self.label_proximo.text = "RANK MAXIMO ATINGIDO"

    def abrir_divisao(self, chave):
        """Tocar numa parte do boneco abre o detalhe daquela divisao."""
        tela = self.manager.get_screen("body_part_detail")
        tela.definir_divisao(chave, origem="home")
        self.manager.current = "body_part_detail"

    def ir_para(self, nome_tela):
        if self.manager.has_screen(nome_tela):
            self.manager.current = nome_tela
