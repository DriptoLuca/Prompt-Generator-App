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
                testo_espanso = f"*(Espansione Semantica Attivata: archetipo '{key}')*\nInput originale: {input_utente}\n\n"
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
        sezioni.append(f"Sei {nome}, un agente AI specializzato.\n")
        if ruolo: sezioni.append(f"<ruolo>\n{_indenta(ruolo)}\n</ruolo>\n")
        if compito: sezioni.append(f"<compito>\n{_indenta(compito)}\n</compito>\n")
        sezioni.append(f"<formato>\n{_indenta(TIPI_OUTPUT[tipo])}\n</formato>\n")
    else:
        sezioni.append(f"Sei {nome}, un agente AI specializzato.\n")
        if ruolo: sezioni.append(f"## RUOLO\n{_indenta(ruolo)}\n")
        if compito: sezioni.append(f"## COMPITO\n{_indenta(compito)}\n")
        sezioni.append(f"## FORMATO\n**{tipo.upper()}**\n{_indenta(TIPI_OUTPUT[tipo])}\n")
    return "\n".join(sezioni).strip() + "\n"

def main(page: ft.Page):
    # Configurazione di stabilità per Android 16
    page.theme = ft.Theme(font_family="sans-serif")
    page.title = APP_NAME
    page.theme_mode = "light"
    page.scroll = "adaptive"
    page.padding = 20

    agenti = ["Gemini", "ChatGPT", "Grok", "Claude", "Perplexity"]
    dd_tipo = ft.Dropdown(label="Tipo", options=[ft.dropdown.Option(t) for t in TIPI_OUTPUT.keys()], value="Testo")
    dd_agente = ft.Dropdown(label="Agente", options=[ft.dropdown.Option(a) for a in agenti], value=agenti[0])
    txt_ruolo = ft.TextField(label="Ruolo", multiline=True, min_lines=2)
    txt_compito = ft.TextField(label="Compito", multiline=True, min_lines=2)
    txt_output = ft.TextField(label="Risultato", multiline=True, min_lines=8, read_only=True, selectable=True, border_color="blue")

    def on_genera(e):
        txt_output.value = genera_prompt(nome=dd_agente.value, ruolo=txt_ruolo.value, compito=txt_compito.value, tipo=dd_tipo.value)
        page.update()

    def on_copia(e):
        if txt_output.value:
            page.clipboard.set(txt_output.value)
            page.update()

    page.add(
        ft.Text(APP_NAME, size=20, weight="bold", color="blue"),
        dd_tipo, dd_agente, txt_ruolo, txt_compito,
        ft.FilledButton("Genera Prompt", icon="auto_awesome", on_click=on_genera),
        txt_output,
        ft.Row([ft.OutlinedButton("Copia", icon="copy", on_click=on_copia)])
    )

if __name__ == "__main__":
    ft.run(main)
