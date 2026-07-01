import flet as ft
import os

# Forza il rendering software per evitare il crash su GPU nuove/Xiaomi
os.environ["FLET_RENDERER"] = "html" 

def main(page: ft.Page):
    page.title = "Generatore Prompt AI"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20
    page.scroll = ft.ScrollMode.AUTO

    # Componenti base
    txt_ruolo = ft.TextField(label="Ruolo")
    txt_compito = ft.TextField(label="Compito", multiline=True)
    txt_output = ft.TextField(label="Risultato", multiline=True, read_only=True, selectable=True)

    def genera_click(e):
        txt_output.value = f"Ruolo: {txt_ruolo.value}\nCompito: {txt_compito.value}"
        page.update()

    # Logica di copia separata con gestione errore
    def on_copia(e):
        if txt_output.value:
            try:
                # Tentativo sicuro di accesso alla clipboard
                page.set_clipboard(txt_output.value)
                page.show_snack_bar(ft.SnackBar(ft.Text("Copiato negli appunti!")))
            except Exception:
                # Fallback se il metodo fallisce
                page.show_snack_bar(ft.SnackBar(ft.Text("Errore clipboard, seleziona il testo manualmente")))
            page.update()

    # Costruzione interfaccia
    page.add(
        ft.Text("Generatore Prompt AI", size=20, weight="bold"),
        txt_ruolo,
        txt_compito,
        ft.ElevatedButton("Genera", on_click=genera_click),
        txt_output,
        ft.OutlinedButton("Copia Prompt", icon="copy", on_click=on_copia)
    )

ft.app(target=main)
