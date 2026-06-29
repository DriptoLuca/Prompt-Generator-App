import datetime
import flet as ft

APP_NAME = "Generatore di Prompt AI"
APP_VERSION = "4.0.0"

# Mappatura dei vincoli specifici per tipo di output
TIPI_OUTPUT = {
    "Testo": "- Produci l'output esclusivamente in formato testuale strutturato.\n- Cura la leggibilità, la formattazione in paragrafi e l'uso di elenchi puntati.",
    "Codice": "- Produci l'output sotto forma di codice sorgente pulito, commentato e pronto all'uso.\n- Includi solo blocchi di codice validi.",
    "Immagine": "- Genera una descrizione visuale dettagliata (prompt per text-to-image).\n- Specifica lo stile artistico, l'illuminazione, la composizione e i parametri tecnici.",
    "Video": "- Struttura l'output come uno storyboard o uno script sequenziale per la generazione video.\n- Includi indicazioni su movimenti di camera e transizioni."
}

class PromptExpansionLayer:
    def __init__(self, mode="rule_based", api_client=None):
        self.mode = mode
        self.api_client = api_client 

    def espandi(self, input_utente, tipo_output):
        if len((input_utente or "").strip()) > 150: 
            return input_utente

        input_clean = (input_utente or "").lower()
        
        archetipi_visivi = {
            "inquietante": {"Soggetto": "Una figura umana non identificata e distorta", "Atmosfera": "Tensione psicologica"},
            "noir": {"Soggetto": "Silhouette in movimento", "Ambiente": "Vicolo brutalista", "Stile": "Urban Noir"},
            "heritage": {"Ambiente": "Loft minimale", "Illuminazione": "Golden hour"}
        }
        archetipi_testo = {
            "social": {"Focus": "Contenuti virali", "Tono": "Coinvolgente", "Struttura": "Hook, Valore, CTA"}
        }
        
        target_dict = archetipi_visivi if tipo_output in ["Immagine", "Video"] else archetipi_testo
        if tipo_output == "Codice": target_dict = {}

        for key, assi in target_dict.items():
            if key in input_clean:
                testo_espanso = f"*(Espansione Semantica Attivata: archetipo '{key}')*\n"
                testo_espanso += f"Input originale: {input_utente}\n\n"
                for asse, valore in assi.items():
                    testo_espanso += f"- **{asse}**: {valore}\n"
                return testo_espanso

        return input_utente

def _indenta(testo, prefisso=""):
    righe = [riga.rstrip() for riga in (testo or "").splitlines()]
    return "\n".join(prefisso + riga for riga in righe)

def _formatta_istruzioni(testo):
    righe = [r.strip() for r in (testo or "").splitlines() if r.strip()]
    out = []
    for r in righe:
        if r.startswith(("-", "*", "•")) or (len(r) > 1 and r[0].isdigit() and r[1] in ".)"):
            out.append(r)
        else:
            out.append(f"- {r}")
    return "\n".join(out) if out else _indenta(testo)

def genera_prompt(nome="", ruolo="", compito="", istruzioni="", contesto="", tipo="Testo", usa_expander=True):
    nome = (nome or "").strip()
    ruolo = (ruolo or "").strip()
    compito = (compito or "").strip()
    istruzioni = (istruzioni or "").strip()
    contesto = (contesto or "").strip()
    tipo = tipo if tipo in TIPI_OUTPUT else "Testo"

    if usa_expander and compito:
        expander = PromptExpansionLayer()
        compito = expander.espandi(compito, tipo)

    titolo = f"PROMPT PER AGENTE AI{' — ' + nome if nome else ''}"
    barra = "=" * len(titolo)
    sezioni = [titolo, barra, ""]

    if nome == "Claude":
        sezioni.append(f"Sei {nome}, un agente AI specializzato. Agisci sempre coerentemente con l'identità e il ruolo descritti nei tag seguenti.\n")
        if ruolo: sezioni.append(f"<ruolo_e_caratteristiche>\n{_indenta(ruolo)}\n</ruolo_e_caratteristiche>\n")
        if compito: sezioni.append(f"<compito_principale>\n{_indenta(compito)}\n</compito_principale>\n")
        if istruzioni: sezioni.append(f"<istruzioni_specifiche>\n{_formatta_istruzioni(istruzioni)}\n</istruzioni_specifiche>\n")
        if contesto: sezioni.append(f"<contesto_aggiuntivo>\n{_indenta(contesto)}\n</contesto_aggiuntivo>\n")
        sezioni.append(f"<formato_output_richiesto>\nTipo di output: {tipo.upper()}\n{_indenta(TIPI_OUTPUT[tipo])}\n</formato_output_richiesto>\n")
    else:
        sezioni.append(f"Sei {nome}, un agente AI specializzato. Agisci coerentemente con l'identità descritta di seguito.\n")
        if nome == "Perplexity":
            sezioni.append("> **ISTRUZIONE**: Effettua sempre una ricerca sul web aggiornata. Includi citazioni precise alle fonti.\n")
        elif nome == "Gemini":
            sezioni.append("> **ISTRUZIONE**: Analizza attentamente le sezioni delimitate. Mantieni una separazione logica rigorosa.\n")

        if ruolo: sezioni.append(f"## RUOLO E CARATTERISTICHE\n{_indenta(ruolo)}\n")
        if compito: sezioni.append(f"## COMPITO\n{_indenta(compito)}\n")
        if istruzioni: sezioni.append(f"## ISTRUZIONI SPECIFICHE\n{_formatta_istruzioni(istruzioni)}\n")
        if contesto: sezioni.append(f"## CONTESTO AGGIUNTIVO\n{_indenta(contesto)}\n")
        sezioni.append(f"## FORMATO DI OUTPUT RICHIESTO\n**{tipo.upper()}**\n{_indenta(TIPI_OUTPUT[tipo])}\n")

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    sezioni.append("-" * len(titolo))
    sezioni.append(f"Generato il {timestamp} con {APP_NAME} v{APP_VERSION}")

    return "\n".join(sezioni).strip() + "\n"

# --- INTERFACCIA GRAFICA MOBILE CON FLET ---
def main(page: ft.Page):
    page.title = APP_NAME
    page.theme_mode = "light" 
    page.scroll = "adaptive"  
    page.padding = 20

    agenti_disponibili = ["Gemini", "ChatGPT", "Grok", "Claude", "Perplexity"]
    tipi_disponibili = list(TIPI_OUTPUT.keys())

    # Input Widgets
    dd_tipo = ft.Dropdown(label="Tipo di output", options=[ft.dropdown.Option(t) for t in tipi_disponibili], value="Testo", expand=True)
    sw_expander = ft.Switch(label="AI Expander (Espansione Semantica)", value=True)
    dd_agente = ft.Dropdown(label="Nome dell'agente", options=[ft.dropdown.Option(a) for a in agenti_disponibili], value=agenti_disponibili[0])
    
    txt_ruolo = ft.TextField(label="Ruolo / Caratteristiche", multiline=True, min_lines=2, max_lines=4)
    txt_compito = ft.TextField(label="Descrizione del Compito", multiline=True, min_lines=2, max_lines=4)
    txt_istruzioni = ft.TextField(label="Istruzioni specifiche", multiline=True, min_lines=2, max_lines=4)
    txt_contesto = ft.TextField(label="Contesto aggiuntivo", multiline=True, min_lines=2, max_lines=4)
    
    txt_output = ft.TextField(label="Prompt Generato", multiline=True, min_lines=8, read_only=True, border_color="blue")
    txt_status = ft.Text(value="Pronto.", color="grey", weight="bold")

    # Azioni
    def on_genera(e):
        prompt = genera_prompt(
            nome=dd_agente.value,
            ruolo=txt_ruolo.value,
            compito=txt_compito.value,
            istruzioni=txt_istruzioni.value,
            contesto=txt_contesto.value,
            tipo=dd_tipo.value,
            usa_expander=sw_expander.value
        )
        txt_output.value = prompt
        txt_status.value = "✓ Prompt generato con successo!"
        txt_status.color = "green"
        page.update()

    def on_copia(e):
        if txt_output.value:
            page.set_clipboard(txt_output.value)
            txt_status.value = "✓ Prompt copiato negli appunti!"
            txt_status.color = "blue"
            page.update()

    def on_pulisci(e):
        txt_ruolo.value = ""
        txt_compito.value = ""
        txt_istruzioni.value = ""
        txt_contesto.value = ""
        txt_output.value = ""
        dd_agente.value = agenti_disponibili[0]
        dd_tipo.value = "Testo"
        txt_status.value = "Campi svuotati."
        txt_status.color = "grey"
        page.update()

    btn_genera = ft.FilledButton("Genera", icon="auto_awesome", on_click=on_genera, expand=True)
    btn_copia = ft.OutlinedButton("Copia", icon="copy", on_click=on_copia, expand=True)
    btn_pulisci = ft.TextButton("Svuota", icon="delete", on_click=on_pulisci)

    # Layout finale
    page.add(
        ft.Text(APP_NAME, size=24, weight="bold", color="blue"),
        ft.Divider(),
        dd_tipo,
        sw_expander,
        dd_agente,
        txt_ruolo,
        txt_compito,
        txt_istruzioni,
        txt_contesto,
        ft.Row([btn_genera, btn_copia], alignment="spaceBetween"),
        btn_pulisci,
        txt_status,
        ft.Divider(),
        txt_output
    )

if __name__ == "__main__":
    # Aggiornato per Flet 0.80.0 e successivi
    ft.run(main)