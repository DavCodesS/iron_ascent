"""Tela TREINO ATIVO: marca exercicios como concluidos e distribui o XP."""

from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scrollview import ScrollView
from kivymd.uix.label import MDIcon
from kivymd.uix.screen import MDScreen

from config import theme
from config.ranks import BODY_PARTS
from services.rank_system import houve_rank_up
from services.storage import storage
from services.xp_system import calcular_xp_exercicio
from widgets.components import (
    BotaoPrincipal, CardClicavel, DialogoRankUp, XPBar,
    barra_superior, feedback_xp, texto_simples, titulo,
)


class CardExercicioAtivo(CardClicavel):
    """Card que o usuario toca para marcar o exercicio como concluido."""

    def __init__(self, exercicio, ao_concluir, **kwargs):
        kwargs.setdefault("size_hint_y", None)
        kwargs.setdefault("height", dp(80))
        kwargs.setdefault("spacing", dp(4))
        kwargs.setdefault("orientation", "horizontal")
        kwargs.setdefault("padding", (dp(14), dp(10)))
        super().__init__(**kwargs)
        self.exercicio = exercicio
        self.ao_concluir = ao_concluir
        self.bind(on_release=lambda *_: self.tocar())

        self.marca = MDIcon(
            icon="circle-outline", theme_text_color="Custom",
            theme_font_size="Custom", font_size=dp(26),
            text_color=theme.TEXT_MUTED,
            size_hint=(None, None), size=(dp(30), dp(30)),
            pos_hint={"center_y": 0.5},
        )
        self.add_widget(self.marca)

        coluna = BoxLayout(orientation="vertical", spacing=dp(3),
                           padding=(dp(10), 0, 0, 0))
        self.label_nome = titulo(exercicio.nome, tamanho=14)
        self.label_detalhe = texto_simples(
            f"{exercicio.series} x {exercicio.repeticoes}  |  {exercicio.peso:g} kg",
            tamanho=12, cor=theme.TEXT_DIM,
        )
        self.label_xp = texto_simples(
            f'+{calcular_xp_exercicio(exercicio)} XP '
            f'{BODY_PARTS[exercicio.categoria]["label"]}',
            tamanho=11, cor=theme.ACCENT,
        )
        for widget in (self.label_nome, self.label_detalhe, self.label_xp):
            coluna.add_widget(widget)
        self.add_widget(coluna)

        self.aplicar_estado()

    def tocar(self):
        if not self.exercicio.concluido:
            self.ao_concluir(self)

    def aplicar_estado(self):
        if self.exercicio.concluido:
            self.marca.icon = "check-circle"
            self.marca.text_color = theme.SUCCESS
            self.label_nome.color = theme.TEXT_MUTED
            self.label_xp.color = theme.TEXT_MUTED
            self.cor_borda = theme.SUCCESS
        else:
            self.marca.icon = "circle-outline"
            self.marca.text_color = theme.TEXT_MUTED


class ActiveTrainingScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.md_bg_color = theme.BG
        self.treino = None
        self.xp_ganho = {}

        # FloatLayout permite jogar o "+18 XP" flutuando por cima de tudo.
        self.pilha = FloatLayout()
        raiz = BoxLayout(
            orientation="vertical",
            padding=(dp(theme.PADDING), dp(20), dp(theme.PADDING), dp(theme.PADDING)),
            spacing=dp(theme.GAP),
        )
        self.barra_topo = barra_superior("", self.sair)
        raiz.add_widget(self.barra_topo)

        self.label_progresso = texto_simples("", tamanho=12, cor=theme.TEXT_DIM)
        self.barra_progresso = XPBar(segmentos=1, cor=theme.SUCCESS)
        raiz.add_widget(self.label_progresso)
        raiz.add_widget(self.barra_progresso)

        rolagem = ScrollView(do_scroll_x=False, bar_width=dp(2))
        self.lista = BoxLayout(
            orientation="vertical", spacing=dp(theme.GAP),
            size_hint_y=None, padding=(0, dp(4)),
        )
        self.lista.bind(minimum_height=self.lista.setter("height"))
        rolagem.add_widget(self.lista)
        raiz.add_widget(rolagem)

        raiz.add_widget(BotaoPrincipal(
            texto="FINALIZAR TREINO", icone="flag-checkered", destaque=True,
            on_release=lambda *_: self.finalizar(),
        ))

        self.pilha.add_widget(raiz)
        self.add_widget(self.pilha)

    def definir_treino(self, treino):
        self.treino = treino

    def on_pre_enter(self, *args):
        """Comeca um treino do zero: desmarca tudo e zera o XP da sessao."""
        self.xp_ganho = {}
        for exercicio in self.treino.exercicios:
            exercicio.concluido = False

        self.barra_topo.label_titulo.text = self.treino.nome
        self.barra_progresso.segmentos = max(1, len(self.treino.exercicios))

        self.lista.clear_widgets()
        self.cards = []
        for exercicio in self.treino.exercicios:
            card = CardExercicioAtivo(exercicio, self.concluir)
            self.cards.append(card)
            self.lista.add_widget(card)

        self.atualizar_progresso()

    # --- Progresso ----------------------------------------------------------
    def contar_concluidos(self):
        return sum(1 for e in self.treino.exercicios if e.concluido)

    def atualizar_progresso(self):
        total = len(self.treino.exercicios)
        feitos = self.contar_concluidos()
        self.label_progresso.text = f"{feitos} / {total} exercicios concluidos"
        self.barra_progresso.animar_para(feitos / total if total else 0)

    # --- Acao principal -----------------------------------------------------
    def concluir(self, card):
        exercicio = card.exercicio
        categoria = exercicio.categoria
        xp = calcular_xp_exercicio(exercicio)

        xp_antes = storage.body_part(categoria)["xp"]
        storage.adicionar_xp(categoria, xp)          # ja salva no data.json
        xp_depois = storage.body_part(categoria)["xp"]

        exercicio.concluido = True
        self.xp_ganho[categoria] = self.xp_ganho.get(categoria, 0) + xp

        card.aplicar_estado()
        self.atualizar_progresso()
        feedback_xp(self.pilha, f"+{xp} XP", (card.right - dp(120), card.center_y))

        novo_rank = houve_rank_up(xp_antes, xp_depois)
        if novo_rank:
            DialogoRankUp(
                BODY_PARTS[categoria]["label"], novo_rank["nome"],
                cor_rank=theme.cor(novo_rank["cor"]),
            ).open()

    # --- Saidas -------------------------------------------------------------
    def finalizar(self):
        feitos = self.contar_concluidos()
        if feitos:
            storage.finalizar_treino(self.treino, self.xp_ganho, feitos)
        self.manager.current = "home"

    def sair(self):
        """Sair sem finalizar: o XP ja ganho continua valendo, mas nao vai ao historico."""
        self.manager.current = "workout_detail"
