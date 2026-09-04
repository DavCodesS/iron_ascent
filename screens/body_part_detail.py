"""Tela detalhada de uma divisao corporal: rank, XP e estatisticas."""

from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivymd.uix.screen import MDScreen

from config import theme
from config.ranks import BODY_PARTS
from services.rank_system import progresso
from services.storage import storage
from widgets.components import Card, XPBar, barra_superior, texto_simples, titulo


class BlocoNumero(Card):
    """Card pequeno com um numero grande e um rotulo embaixo."""

    def __init__(self, rotulo, **kwargs):
        kwargs.setdefault("size_hint_y", None)
        kwargs.setdefault("height", dp(78))
        kwargs.setdefault("spacing", dp(2))
        super().__init__(**kwargs)
        self.label_valor = titulo("0", tamanho=24, cor=theme.ACCENT, halign="center")
        self.add_widget(self.label_valor)
        self.add_widget(texto_simples(
            rotulo, tamanho=10, cor=theme.TEXT_MUTED, halign="center"
        ))

    def definir(self, valor):
        self.label_valor.text = str(valor)


class BodyPartDetailScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.md_bg_color = theme.BG
        self.chave = "peito"
        self.origem = "progress"

        raiz = BoxLayout(
            orientation="vertical",
            padding=(dp(theme.PADDING), dp(20), dp(theme.PADDING), dp(theme.PADDING)),
            spacing=dp(theme.GAP),
        )
        self.barra_topo = barra_superior(
            "", lambda: setattr(self.manager, "current", self.origem)
        )
        raiz.add_widget(self.barra_topo)

        rolagem = ScrollView(do_scroll_x=False, bar_width=dp(2))
        conteudo = BoxLayout(
            orientation="vertical", spacing=dp(theme.GAP), size_hint_y=None
        )
        conteudo.bind(minimum_height=conteudo.setter("height"))

        # Card principal do rank
        self.card_rank = Card(size_hint_y=None, height=dp(160), spacing=dp(8))
        self.card_rank.add_widget(texto_simples(
            "RANK ATUAL", tamanho=10, cor=theme.TEXT_MUTED
        ))
        self.label_rank = titulo("", tamanho=22, cor=theme.TEXT)
        self.barra = XPBar(segmentos=20)
        self.label_xp = texto_simples("", tamanho=13, cor=theme.TEXT_DIM)
        self.label_proximo = texto_simples("", tamanho=11, cor=theme.STEEL)
        for widget in (self.label_rank, self.barra, self.label_xp, self.label_proximo):
            self.card_rank.add_widget(widget)
        conteudo.add_widget(self.card_rank)

        # Estatisticas lado a lado
        linha = BoxLayout(size_hint_y=None, height=dp(78), spacing=dp(theme.GAP))
        self.bloco_exercicios = BlocoNumero("EXERCICIOS CONCLUIDOS")
        self.bloco_treinos = BlocoNumero("TREINOS COMPLETOS")
        linha.add_widget(self.bloco_exercicios)
        linha.add_widget(self.bloco_treinos)
        conteudo.add_widget(linha)

        rolagem.add_widget(conteudo)
        raiz.add_widget(rolagem)
        self.add_widget(raiz)

    def definir_divisao(self, chave, origem="progress"):
        """Chamado antes de trocar de tela. `origem` define para onde voltar."""
        self.chave = chave
        self.origem = origem

    def on_pre_enter(self, *args):
        dados = storage.body_part(self.chave)
        info = progresso(dados["xp"])

        cor_rank = theme.cor(info["rank"]["cor"])

        self.barra_topo.label_titulo.text = BODY_PARTS[self.chave]["label"]
        self.label_rank.text = info["rank"]["nome"]
        self.label_rank.color = cor_rank
        self.barra.cor = cor_rank
        self.barra.percentual = info["percentual"]
        self.card_rank.cor_borda = cor_rank
        self.bloco_exercicios.label_valor.color = cor_rank
        self.bloco_treinos.label_valor.color = cor_rank
        self.bloco_exercicios.definir(dados["exercicios_concluidos"])
        self.bloco_treinos.definir(dados["treinos_completos"])

        if info["proximo"]:
            self.label_xp.text = f'{info["xp_no_rank"]} / {info["xp_necessario"]} XP'
            self.label_proximo.text = f'PROXIMO RANK: {info["proximo"]["nome"]}'
        else:
            self.label_xp.text = f'{dados["xp"]} XP'
            self.label_proximo.text = "RANK MAXIMO ATINGIDO"
