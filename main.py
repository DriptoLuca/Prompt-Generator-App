import flet as ft

def main(page: ft.Page):
    # Configurazione di base ottimizzata per mobile
    page.title = "Generatore Prompt"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20
    page.scroll = ft.ScrollMode.AUTO
    
    # UI Layout con componenti minimi per evitare crash di rendering
    dd_tipo = ft.Dropdown(label="Tipo di output", options=[
        ft.dropdown.Option("Testo"),
        ft.dropdown.Option("Codice"),
        ft.dropdown.Option("Immagine"),
        ft.dropdown.Option("Video")
    ], value="Testo")
    
    dd_agente = ft.Dropdown(label="Agente", options=[
        ft.dropdown.Option("Gemini"),
        ft.dropdown.Option("ChatGPT"),
        ft.dropdown.Option("Claude")
    ], value="Gemini")
    
    txt_ruolo = ft.TextField(label="Ruolo")
    txt_compito = ft.TextField(label="Compito", multiline=True)
    
    txt_output = ft.TextField(
        label="Prompt Generato", 
        multiline=True, 
        read_only=True, 
        selectable=True,
        border_color=ft.colors.BLUE
    )

    def on_genera(e):
        # Versione semplificata della logica per evitare errori di calcolo stringhe
        txt_output.value = f"Agente: {dd_agente.value}\nTipo: {dd_tipo.value}\nRuolo: {txt_ruolo.value}\nCompito: {txt_compito.value}"
        page.update()

    def on_copia(e):
        if txt_output.value:
            page.clipboard.set(txt_output.value)
            page.show_snack_bar(ft.SnackBar(ft.Text("Copiato!")))

    # Aggiunta elementi al layout
    page.add(
        ft.Text("Generatore Prompt", size=20, weight="bold"),
        dd_tipo,
        dd_agente,
        txt_ruolo,
        txt_compito,
        ft.ElevatedButton("Genera", on_click=on_genera),
        txt_output,
        ft.ElevatedButton("Copia", on_click=on_copia)
    )
    
    # Forza un refresh grafico finale per evitare la schermata bianca
    page.update()

# Avvio sicuro
if __name__ == "__main__":
    ft.app(target=main)
