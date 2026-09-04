"""Pecas visuais reutilizadas em varias telas.

Sao widgets simples desenhados na mao (canvas) para termos controle total
das cores e do visual "metalico" do app.
"""

import json
import os

from kivy.core.image import Image as CoreImage
from kivy.metrics import dp
from kivy.properties import ColorProperty, NumericProperty, StringProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.modalview import ModalView
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.graphics import Color, Line, Rectangle, RoundedRectangle
from kivy.animation import Animation
from kivymd.uix.label import MDIcon

from config import theme


class Card(BoxLayout):
    """Retangulo escuro com borda sutil, usado como base de quase tudo."""

    cor_fundo = ColorProperty(theme.SURFACE)
    cor_borda = ColorProperty(theme.BORDER)
    raio = NumericProperty(theme.RADIUS)

    def __init__(self, **kwargs):
        kwargs.setdefault("orientation", "vertical")
        kwargs.setdefault("padding", dp(theme.PADDING))
        kwargs.setdefault("spacing", dp(8))
        super().__init__(**kwargs)
        with self.canvas.before:
            self._cor = Color(rgba=self.cor_fundo)
            self._fundo = RoundedRectangle(radius=[self.raio])
            self._cor_linha = Color(rgba=self.cor_borda)
            self._linha = Line(width=1)
        self.bind(pos=self._redesenhar, size=self._redesenhar,
                  cor_fundo=self._atualizar_cores, cor_borda=self._atualizar_cores)

    def _redesenhar(self, *_):
        self._fundo.pos = self.pos
        self._fundo.size = self.size
        self._linha.rounded_rectangle = (
            self.x, self.y, self.width, self.height, self.raio
        )

    def _atualizar_cores(self, *_):
        self._cor.rgba = self.cor_fundo
        self._cor_linha.rgba = self.cor_borda


class CardClicavel(ButtonBehavior, Card):
    """Card que responde a toque. Use o evento on_release."""

    def on_press(self):
        self.cor_fundo = theme.SURFACE_LIGHT

    def on_release(self):
        self.cor_fundo = theme.SURFACE


class XPBar(Widget):
    """Barra de progresso segmentada, no estilo painel de jogo."""

    percentual = NumericProperty(0.0)   # 0.0 a 1.0
    cor = ColorProperty(theme.ACCENT)
    segmentos = NumericProperty(20)
    orientacao = StringProperty("horizontal")   # ou "vertical"

    def __init__(self, **kwargs):
        kwargs.setdefault("size_hint_y", None)
        kwargs.setdefault("height", dp(14))
        super().__init__(**kwargs)
        self.bind(pos=self._desenhar, size=self._desenhar,
                  percentual=self._desenhar, cor=self._desenhar,
                  orientacao=self._desenhar)
        self._desenhar()

    def _desenhar(self, *_):
        self.canvas.clear()
        total = int(self.segmentos)
        if total <= 0 or self.width <= 0 or self.height <= 0:
            return

        espaco = dp(2)
        vertical = self.orientacao == "vertical"
        comprimento = self.height if vertical else self.width
        passo = (comprimento - espaco * (total - 1)) / total
        preenchidos = self.percentual * total

        with self.canvas:
            for i in range(total):
                cheio = i < int(preenchidos)
                Color(rgba=self.cor if cheio else theme.SURFACE_LIGHT)
                if vertical:
                    pos = (self.x, self.y + i * (passo + espaco))
                    tamanho = (self.width, passo)
                else:
                    pos = (self.x + i * (passo + espaco), self.y)
                    tamanho = (passo, self.height)
                RoundedRectangle(pos=pos, size=tamanho, radius=[dp(2)])

    def animar_para(self, valor: float, duracao: float = 0.4):
        """Anima a barra ate o novo valor (usado no ganho de XP)."""
        Animation.cancel_all(self, "percentual")
        Animation(percentual=max(0.0, min(1.0, valor)), d=duracao, t="out_quad").start(self)


class BotaoPrincipal(ButtonBehavior, BoxLayout):
    """Botao grande com icone, no estilo do app."""

    texto = StringProperty("")
    icone = StringProperty("chevron-right")
    cor_fundo = ColorProperty(theme.SURFACE_LIGHT)
    cor_texto = ColorProperty(theme.TEXT)

    def __init__(self, texto="", icone="chevron-right", destaque=False, **kwargs):
        kwargs.setdefault("orientation", "horizontal")
        kwargs.setdefault("size_hint_y", None)
        kwargs.setdefault("height", dp(58))
        kwargs.setdefault("padding", (dp(18), 0))
        kwargs.setdefault("spacing", dp(14))
        super().__init__(**kwargs)

        self.texto = texto
        self.icone = icone
        if destaque:
            self.cor_fundo = theme.ACCENT
            self.cor_texto = theme.BG

        with self.canvas.before:
            self._cor = Color(rgba=self.cor_fundo)
            self._fundo = RoundedRectangle(radius=[theme.RADIUS])
        self.bind(pos=self._redesenhar, size=self._redesenhar,
                  cor_fundo=lambda *_: setattr(self._cor, "rgba", self.cor_fundo))

        self._icone = MDIcon(
            icon=self.icone, theme_text_color="Custom", text_color=self.cor_texto,
            theme_font_size="Custom", font_size=dp(24),
            size_hint=(None, None), size=(dp(24), dp(24)),
            pos_hint={"center_y": 0.5},
        )
        self._label = Label(
            text=self.texto, bold=True, font_size=dp(15), color=self.cor_texto,
            halign="left", valign="middle",
        )
        self._label.bind(size=lambda w, v: setattr(w, "text_size", v))

        self.add_widget(self._icone)
        self.add_widget(self._label)

    def _redesenhar(self, *_):
        self._fundo.pos = self.pos
        self._fundo.size = self.size

    def on_press(self):
        self._cor.a = 0.75

    def on_release(self):
        self._cor.a = 1.0


def titulo(texto, tamanho=22, cor=theme.TEXT, halign="left", **kwargs):
    """Atalho para criar um Label de titulo ja configurado."""
    kwargs.setdefault("size_hint_y", None)
    kwargs.setdefault("height", dp(tamanho * 1.6))
    label = Label(
        text=texto, bold=True, font_size=dp(tamanho), color=cor,
        halign=halign, valign="middle", **kwargs
    )
    label.bind(size=lambda w, v: setattr(w, "text_size", v))
    return label


def texto_simples(texto, tamanho=13, cor=theme.TEXT_DIM, halign="left", **kwargs):
    kwargs.setdefault("size_hint_y", None)
    kwargs.setdefault("height", dp(tamanho * 1.5))
    label = Label(
        text=texto, font_size=dp(tamanho), color=cor,
        halign=halign, valign="middle", **kwargs
    )
    label.bind(size=lambda w, v: setattr(w, "text_size", v))
    return label


# ---------------------------------------------------------------------------
# Barra superior das telas internas
# ---------------------------------------------------------------------------

class IconeBotao(ButtonBehavior, MDIcon):
    """MDIcon que pode ser clicado."""

    def __init__(self, **kwargs):
        kwargs.setdefault("theme_text_color", "Custom")
        kwargs.setdefault("text_color", theme.TEXT)
        kwargs.setdefault("theme_font_size", "Custom")
        kwargs.setdefault("font_size", dp(24))
        kwargs.setdefault("size_hint", (None, None))
        kwargs.setdefault("size", (dp(28), dp(28)))
        super().__init__(**kwargs)


def barra_superior(texto, ao_voltar, acao_icone=None, ao_acionar=None):
    """Linha com botao de voltar, titulo e (opcional) um botao a direita."""
    barra = BoxLayout(
        orientation="horizontal", size_hint_y=None, height=dp(44), spacing=dp(12)
    )
    barra.add_widget(IconeBotao(
        icon="arrow-left", text_color=theme.ACCENT,
        pos_hint={"center_y": 0.5}, on_release=lambda *_: ao_voltar(),
    ))
    barra.label_titulo = titulo(texto, tamanho=18)
    barra.add_widget(barra.label_titulo)
    if acao_icone:
        barra.add_widget(IconeBotao(
            icon=acao_icone, text_color=theme.ACCENT,
            pos_hint={"center_y": 0.5}, on_release=lambda *_: ao_acionar(),
        ))
    return barra


# ---------------------------------------------------------------------------
# Campos e dialogos
# ---------------------------------------------------------------------------

class Campo(TextInput):
    """TextInput ja com as cores do app."""

    def __init__(self, **kwargs):
        kwargs.setdefault("multiline", False)
        kwargs.setdefault("size_hint_y", None)
        kwargs.setdefault("height", dp(42))
        kwargs.setdefault("font_size", dp(15))
        kwargs.setdefault("padding", [dp(10), dp(10)])
        kwargs.setdefault("background_color", theme.SURFACE_LIGHT)
        kwargs.setdefault("foreground_color", theme.TEXT)
        kwargs.setdefault("cursor_color", theme.ACCENT)
        kwargs.setdefault("background_normal", "")
        kwargs.setdefault("background_active", "")
        super().__init__(**kwargs)


class Chip(ButtonBehavior, BoxLayout):
    """Etiqueta selecionavel, usada para escolher a divisao corporal."""

    def __init__(self, texto, **kwargs):
        kwargs.setdefault("size_hint", (None, None))
        kwargs.setdefault("height", dp(32))
        kwargs.setdefault("width", dp(max(72, len(texto) * 10 + 24)))
        kwargs.setdefault("padding", (dp(12), 0))
        super().__init__(**kwargs)
        self.selecionado = False
        with self.canvas.before:
            self._cor = Color(rgba=theme.SURFACE_LIGHT)
            self._fundo = RoundedRectangle(radius=[dp(16)])
        self.bind(pos=self._redesenhar, size=self._redesenhar)
        self._label = Label(text=texto, font_size=dp(12), bold=True, color=theme.TEXT_DIM)
        self.add_widget(self._label)

    def _redesenhar(self, *_):
        self._fundo.pos = self.pos
        self._fundo.size = self.size

    def selecionar(self, valor: bool):
        self.selecionado = valor
        self._cor.rgba = theme.ACCENT if valor else theme.SURFACE_LIGHT
        self._label.color = theme.BG if valor else theme.TEXT_DIM


class DialogoBase(ModalView):
    """Janela flutuante com o visual do app."""

    def __init__(self, titulo_texto, **kwargs):
        kwargs.setdefault("size_hint", (0.9, None))
        kwargs.setdefault("auto_dismiss", True)
        kwargs.setdefault("background", "")
        kwargs.setdefault("background_color", (0, 0, 0, 0.6))
        super().__init__(**kwargs)
        self.caixa = Card(spacing=dp(12), cor_fundo=theme.SURFACE)
        self.caixa.add_widget(titulo(titulo_texto, tamanho=17, cor=theme.ACCENT))
        self.add_widget(self.caixa)

    def adicionar_botoes(self, texto_confirmar, ao_confirmar):
        linha = BoxLayout(size_hint_y=None, height=dp(46), spacing=dp(10))
        cancelar = BotaoPrincipal(texto="CANCELAR", icone="close", height=dp(46))
        cancelar.bind(on_release=lambda *_: self.dismiss())
        confirmar = BotaoPrincipal(
            texto=texto_confirmar, icone="check", destaque=True, height=dp(46)
        )
        confirmar.bind(on_release=lambda *_: ao_confirmar())
        linha.add_widget(cancelar)
        linha.add_widget(confirmar)
        self.caixa.add_widget(linha)


class DialogoTexto(DialogoBase):
    """Pede um unico texto. Usado para criar e renomear treinos."""

    def __init__(self, titulo_texto, ao_confirmar, valor_inicial="", dica="Nome", **kwargs):
        kwargs.setdefault("height", dp(190))
        super().__init__(titulo_texto, **kwargs)
        self.ao_confirmar = ao_confirmar
        self.campo = Campo(text=valor_inicial, hint_text=dica)
        self.caixa.add_widget(self.campo)
        self.caixa.add_widget(BoxLayout())
        self.adicionar_botoes("CONFIRMAR", self._confirmar)

    def _confirmar(self):
        texto = self.campo.text.strip()
        if texto:
            self.ao_confirmar(texto)
            self.dismiss()


class DialogoExercicio(DialogoBase):
    """Formulario de exercicio: nome, divisao corporal, series, repeticoes e peso."""

    def __init__(self, ao_confirmar, exercicio=None, **kwargs):
        from config.ranks import BODY_PARTS  # importado aqui para evitar ciclo

        kwargs.setdefault("height", dp(400))
        super().__init__("EXERCICIO" if exercicio else "NOVO EXERCICIO", **kwargs)
        self.ao_confirmar = ao_confirmar
        self.categoria = exercicio.categoria if exercicio else next(iter(BODY_PARTS))

        self.campo_nome = Campo(
            text=exercicio.nome if exercicio else "", hint_text="Nome do exercicio"
        )
        self.caixa.add_widget(self.campo_nome)

        # Escolha da divisao corporal
        self.caixa.add_widget(texto_simples("DIVISAO CORPORAL", tamanho=10,
                                            cor=theme.TEXT_MUTED))
        rolagem = ScrollView(size_hint_y=None, height=dp(38), do_scroll_y=False,
                             bar_width=0)
        faixa = BoxLayout(orientation="horizontal", spacing=dp(6),
                          size_hint_x=None, height=dp(34))
        faixa.bind(minimum_width=faixa.setter("width"))

        self.chips = {}
        for chave, info in BODY_PARTS.items():
            chip = Chip(info["label"])
            chip.bind(on_release=lambda _, c=chave: self.escolher(c))
            self.chips[chave] = chip
            faixa.add_widget(chip)
        rolagem.add_widget(faixa)
        self.caixa.add_widget(rolagem)
        self.escolher(self.categoria)

        # Numeros
        linha = BoxLayout(size_hint_y=None, height=dp(64), spacing=dp(8))
        self.campo_series = self._campo_numero(
            "SERIES", str(exercicio.series) if exercicio else "3")
        self.campo_reps = self._campo_numero(
            "REPETICOES", str(exercicio.repeticoes) if exercicio else "10")
        self.campo_peso = self._campo_numero(
            "PESO (KG)", str(exercicio.peso) if exercicio else "0", decimal=True)
        for coluna in (self.campo_series, self.campo_reps, self.campo_peso):
            linha.add_widget(coluna.parent_box)
        self.caixa.add_widget(linha)

        self.caixa.add_widget(BoxLayout())
        self.adicionar_botoes("SALVAR", self._confirmar)

    def _campo_numero(self, rotulo, valor, decimal=False):
        coluna = BoxLayout(orientation="vertical", spacing=dp(4))
        coluna.add_widget(texto_simples(rotulo, tamanho=9, cor=theme.TEXT_MUTED,
                                        halign="center", height=dp(14)))
        campo = Campo(text=valor, halign="center",
                      input_filter="float" if decimal else "int")
        coluna.add_widget(campo)
        campo.parent_box = coluna
        return campo

    def escolher(self, chave):
        self.categoria = chave
        for c, chip in self.chips.items():
            chip.selecionar(c == chave)

    def _confirmar(self):
        nome = self.campo_nome.text.strip()
        if not nome:
            return
        self.ao_confirmar({
            "nome": nome,
            "categoria": self.categoria,
            "series": int(self.campo_series.text or 1),
            "repeticoes": int(self.campo_reps.text or 1),
            "peso": float(self.campo_peso.text or 0),
        })
        self.dismiss()


class DialogoRankUp(ModalView):
    """Comemoracao mostrada quando uma divisao corporal sobe de rank."""

    def __init__(self, divisao, novo_rank, cor_rank=None, **kwargs):
        kwargs.setdefault("size_hint", (0.85, None))
        kwargs.setdefault("height", dp(250))
        kwargs.setdefault("background", "")
        kwargs.setdefault("background_color", (0, 0, 0, 0.75))
        super().__init__(**kwargs)

        cor_rank = cor_rank or theme.ACCENT
        caixa = Card(spacing=dp(6), cor_fundo=theme.SURFACE, cor_borda=cor_rank)
        caixa.add_widget(BoxLayout(size_hint_y=None, height=dp(4)))
        caixa.add_widget(titulo("RANK UP", tamanho=30, cor=cor_rank,
                                halign="center"))
        caixa.add_widget(texto_simples(divisao, tamanho=13, cor=theme.TEXT_DIM,
                                       halign="center"))
        caixa.add_widget(BoxLayout(size_hint_y=None, height=dp(6)))
        caixa.add_widget(texto_simples("NOVO RANK", tamanho=10, cor=theme.TEXT_MUTED,
                                       halign="center"))
        self.label_rank = titulo(novo_rank, tamanho=20, cor=cor_rank, halign="center")
        caixa.add_widget(self.label_rank)
        caixa.add_widget(BoxLayout())

        botao = BotaoPrincipal(texto="CONTINUAR", icone="chevron-right", destaque=True)
        botao.bind(on_release=lambda *_: self.dismiss())
        caixa.add_widget(botao)
        self.add_widget(caixa)

    def on_open(self):
        # Pequena animacao de entrada: o card cresce e o texto aparece.
        self.label_rank.opacity = 0
        Animation(opacity=1, d=0.45, t="out_quad").start(self.label_rank)


def feedback_xp(tela, texto_xp, ponto):
    """Mostra '+18 XP' subindo e desaparecendo na posicao indicada."""
    etiqueta = Label(
        text=texto_xp, bold=True, font_size=dp(17), color=theme.ACCENT,
        size_hint=(None, None), size=(dp(110), dp(28)),
        pos=(ponto[0], ponto[1]),
    )
    tela.add_widget(etiqueta)
    animacao = Animation(y=etiqueta.y + dp(55), opacity=0, d=0.9, t="out_quad")
    animacao.bind(on_complete=lambda *_: tela.remove_widget(etiqueta))
    animacao.start(etiqueta)


class Boneco(Widget):
    """Silhueta anatomica com cada musculo pintado na cor do seu rank.

    Cada divisao corporal e um PNG em assets/body/ contendo so aquele
    musculo. O Kivy multiplica a textura pela cor, entao a mesma imagem
    serve para qualquer rank: basta trocar a cor.
    """

    PASTA = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "assets", "body",
    )
    _mapa = None

    @classmethod
    def carregar_mapa(cls):
        if cls._mapa is None:
            with open(os.path.join(cls.PASTA, "mapa.json"), encoding="utf-8") as f:
                cls._mapa = json.load(f)
        return cls._mapa

    def __init__(self, vista="frente", ao_tocar=None, **kwargs):
        super().__init__(**kwargs)
        self.vista = vista
        self.ao_tocar = ao_tocar
        self.cores = {}

        dados = self.carregar_mapa()[vista]
        self.proporcao = dados["proporcao"]      # largura / altura
        self.poligonos = dados["regioes"]

        self.base = CoreImage(os.path.join(self.PASTA, f"{vista}_base.png")).texture
        self.camadas = []
        for nome in self.ORDEM:
            caminho = os.path.join(self.PASTA, f"{vista}_{nome}.png")
            if os.path.exists(caminho):
                self.camadas.append((nome, CoreImage(caminho).texture))

        self.bind(pos=self._desenhar, size=self._desenhar)
        self._desenhar()

    # Ordem de pintura: o que vem depois fica por cima nas sobreposicoes.
    ORDEM = ["pernas", "peito", "costas", "abdomen", "biceps", "triceps", "ombros"]

    def definir_cores(self, cores: dict):
        self.cores = cores
        self._desenhar()

    def _area(self):
        """Retangulo do desenho dentro do widget, mantendo a proporcao."""
        if self.width <= 0 or self.height <= 0:
            return 0, 0, 0, 0
        largura = min(self.width, self.height * self.proporcao)
        altura = largura / self.proporcao
        return (self.center_x - largura / 2, self.center_y - altura / 2,
                largura, altura)

    def _desenhar(self, *_):
        self.canvas.clear()
        x, y, largura, altura = self._area()
        if largura <= 0:
            return
        with self.canvas:
            Color(rgba=theme.BONECO_NEUTRO)
            Rectangle(texture=self.base, pos=(x, y), size=(largura, altura))
            for nome, textura in self.camadas:
                Color(rgba=self.cores.get(nome, theme.BONECO_NEUTRO))
                Rectangle(texture=textura, pos=(x, y), size=(largura, altura))

    # --- Toque --------------------------------------------------------------
    def on_touch_down(self, toque):
        if not self.ao_tocar or not self.collide_point(*toque.pos):
            return super().on_touch_down(toque)

        x, y, largura, altura = self._area()
        if largura <= 0:
            return super().on_touch_down(toque)

        # converte para % da figura, com Y contado do topo
        px = (toque.x - x) / largura * 100
        py = (1 - (toque.y - y) / altura) * 100

        for nome in reversed(self.ORDEM):
            for poligono in self.poligonos.get(nome, []):
                if dentro_do_poligono(px, py, poligono):
                    self.ao_tocar(nome)
                    return True
        return super().on_touch_down(toque)


def dentro_do_poligono(px, py, pontos) -> bool:
    """Teste do raio: conta quantas arestas o ponto cruza indo para a direita."""
    dentro = False
    total = len(pontos)
    for i in range(total):
        x1, y1 = pontos[i]
        x2, y2 = pontos[(i + 1) % total]
        if (y1 > py) != (y2 > py):
            corte = x1 + (py - y1) * (x2 - x1) / (y2 - y1)
            if px < corte:
                dentro = not dentro
    return dentro


class PainelCorpoAnatomico(Card):
    """Card da tela inicial com as duas vistas do boneco."""

    TITULOS = {"frente": "FRENTE", "costas": "COSTAS"}

    def __init__(self, ao_tocar=None, **kwargs):
        kwargs.setdefault("size_hint_y", None)
        kwargs.setdefault("height", dp(300))
        kwargs.setdefault("spacing", dp(6))
        super().__init__(**kwargs)

        self.add_widget(texto_simples("STATUS DO CORPO", tamanho=10,
                                      cor=theme.TEXT_MUTED))

        linha = BoxLayout(orientation="horizontal", spacing=dp(4))
        self.bonecos = []
        for chave_vista, rotulo in self.TITULOS.items():
            coluna = BoxLayout(orientation="vertical", spacing=dp(4))
            boneco = Boneco(vista=chave_vista, ao_tocar=ao_tocar)
            self.bonecos.append(boneco)
            coluna.add_widget(boneco)
            coluna.add_widget(Label(
                text=rotulo, font_size=dp(9), bold=True,
                color=theme.TEXT_MUTED, size_hint_y=None, height=dp(12),
            ))
            linha.add_widget(coluna)
        self.add_widget(linha)

    def atualizar(self, body_parts: dict):
        from config.ranks import BODY_PARTS
        from services.rank_system import rank_atual

        cores = {
            chave: theme.cor(rank_atual(body_parts[chave]["xp"])["cor"])
            for chave in BODY_PARTS
        }
        for boneco in self.bonecos:
            boneco.definir_cores(cores)
