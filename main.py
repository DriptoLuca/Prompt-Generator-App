import flet as ft

def main(page: ft.Page):
    # Configurazione di rendering super-sicura
    page.title = "App"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.vertical_alignment = ft.MainAxisAlignment.START
    
    # Widget essenziali (niente decorazioni che possono crashare)
    titolo = ft.Text("Generatore Prompt AI", size=20)
    output = ft.TextField(label="Risultato", multiline=True, read_only=True)
    
    def genera_click(e):
        output.value = "Test di generazione riuscito."
        page.update()

    page.add(
        titolo,
        ft.ElevatedButton("Genera", on_click=genera_click),
        output
    )

if __name__ == "__main__":
    # Avvio standard senza argomenti complessi
    ft.app(target=main)
