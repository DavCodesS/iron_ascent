[app]

title = Iron Ascent
package.name = ironascent
package.domain = org.ironascent

source.dir = .

# Extensoes que entram no APK. png e json sao essenciais: sem eles o
# boneco de assets/body/ nao vai junto.
source.include_exts = py,png,json,txt

# Pastas que NAO devem entrar no APK.
source.exclude_dirs = tools, bin, .buildozer, __pycache__, data

version = 0.1

# Lista recomendada pela documentacao do KivyMD 2.0.
requirements = python3,
    kivy,
    kivymd==2.0.0,
    materialyoucolor==3.0.3,
    pillow,
    exceptiongroup,
    asyncgui,
    asynckivy,
    android

orientation = portrait
fullscreen = 0

# Cor da tela enquanto o app carrega (o mesmo fundo do app).
android.presplash_color = #0B0D10

# O app nao usa internet, camera nem armazenamento externo,
# entao nao pede nenhuma permissao.
android.permissions =

android.accept_sdk_license = True
android.api = 34
android.minapi = 24
android.archs = arm64-v8a

# Nao empacotar como App Bundle: para instalar direto no celular queremos APK.
android.release_artifact = apk

[buildozer]
log_level = 2
warn_on_root = 1
