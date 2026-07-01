import flet as ft

def main(page: ft.Page):
    # Configurazione di base per stabilità su mobile
    page.title = "Generatore Prompt AI"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20
    
    # Definizione dei widget
    titolo = ft.Text("Generatore Prompt AI", size=20, weight="bold")
    txt_ruolo = ft.TextField(label="Ruolo")
    txt_compito = ft.TextField(label="Compito", multiline=True)
    txt_output = ft.TextField(
        label="Risultato", 
        multiline=True, 
        read_only=True, 
        selectable=True,
        border_color=ft.colors.BLUE
    )

    # Logica di generazione
    def genera_click(e):
        txt_output.value = f"Ruolo: {txt_ruolo.value}\nCompito: {txt_compito.value}"
        page.update()

    # Logica di copia
    def on_copia(e):
        if txt_output.value:
            page.clipboard.set(txt_output.value)
            page.show_snack_bar(ft.SnackBar(ft.Text("Prompt copiato negli appunti!")))

    # Layout a colonna scrollabile per evitare problemi di visualizzazione su Android
    page.add(
        ft.Column(
            [
                titolo,
                txt_ruolo,
                txt_compito,
                ft.ElevatedButton("Genera", on_click=genera_click),
                txt_output,
                ft.OutlinedButton("Copia", icon="copy", on_click=on_copia)
            ],
            scroll=ft.ScrollMode.AUTO,
            expand=True
        )
    )
    
    # Forza il rendering finale
    page.update()

if __name__ == "__main__":
    ft.app(target=main)
