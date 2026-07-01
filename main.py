import flet as ft
import os

# Forza rendering software (ottimo per Xiaomi/Android 16)
os.environ["FLET_RENDERER"] = "html"

def main(page: ft.Page):
    page.title = "Generatore Prompt AI"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20
    page.scroll = ft.ScrollMode.AUTO

    txt_ruolo = ft.TextField(label="Ruolo")
    txt_compito = ft.TextField(label="Compito", multiline=True)
    txt_output = ft.TextField(label="Risultato", multiline=True, read_only=True)

    def genera_click(e):
        txt_output.value = f"Ruolo: {txt_ruolo.value}\nCompito: {txt_compito.value}"
        page.update()

    # Nuova funzione Condividi
    def on_condividi(e):
        if txt_output.value:
            # Invoca il menu di condivisione di Android
            # Usiamo un URL speciale che Android intercetta come "Share"
            testo = txt_output.value.replace("\n", "%0A")
            page.launch_url(f"mailto:?body={testo}") # Alternativa universale di fallback
            
    page.add(
        ft.Text("Generatore Prompt AI", size=20, weight="bold"),
        txt_ruolo,
        txt_compito,
        ft.ElevatedButton("Genera", on_click=genera_click),
        txt_output,
        ft.FilledButton("Condividi Prompt", icon="share", on_click=on_condividi)
    )

ft.app(target=main)
