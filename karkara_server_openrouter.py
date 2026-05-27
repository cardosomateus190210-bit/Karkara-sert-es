#!/usr/bin/env python3
import os, json, random
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

API_KEY = os.environ.get("OPENROUTER_API_KEY", "")
PORT    = 5000
HOST    = "localhost"
API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL   = "google/gemma-3-27b-it:free"


# ═══════════════════════════════════════════════════
#   RESPOSTAS DA IA — edite aqui à vontade!
# ═══════════════════════════════════════════════════

def get_resposta(mensagem: str) -> str:
    """
    Retorna uma resposta para a mensagem do usuário.
    Adicione quantas perguntas/respostas quiser abaixo!
    """
    msg = mensagem.lower().strip()
      # ── esteregue ──────────────────────────────────
    if any(p in msg for p in ["paje", "lucas", "indio", "paje-chan"]):
        return "Ele vive no meio da floresta seu melhor amigo é o curupira, ele usa arco e lança e um ser pacifico e vive no meio da mata e seu inimigo eo Wiliam graxeiro"
    
    if any(p in msg for p in ["william", "gleyson", "borracheiro", "graxa", "oleo de carro", "william gleyson", "67", "will", "wl"]):
        return "👋William “Borracheiro” é uma lenda viva da EEEP.Dizem que ele não estuda… ele sobrevive no ambiente escolar igual um boss secreto de oficina mecânica. Seu uniforme já perdeu a cor original faz tempo, porque agora ele é oficialmente 78% graxa e 22% energia de doido."
    # ── Saudações ──────────────────────────────────
    if any(p in msg for p in ["oi", "olá", "ola", "bom dia", "boa tarde", "boa noite", "tudo bem", "e ai", "eai"]):
        return "👋 Olá! Sou a Karkará IA, assistente do produtor rural do semiárido. Como posso te ajudar hoje? Pode perguntar sobre irrigação, pragas, solo, plantio ou colheita!"

    # ── Irrigação ──────────────────────────────────
    if any(p in msg for p in ["irrigacao", "irrigação", "regar", "agua", "água", "gotejamento"]):
        return "💧 Para irrigação no semiárido, o gotejamento é o mais eficiente — economiza até 50% de água entregando direto na raiz. Irrigue cedo (antes das 9h) ou tarde (após 17h) para reduzir evaporação."

    # ── Solo ───────────────────────────────────────
    if any(p in msg for p in ["solo", "terra", "ph", "calcario", "calcário", "adubo", "fertilizante", "umidade"]):
        return "🌱 Use cobertura morta (palha, bagaço) para reter umidade. Solo ácido? Aplique calcário para corrigir o pH e melhorar a absorção de nutrientes. Adubo orgânico (esterco curtido) enriquece o solo a cada ciclo."

    # ── Pragas ─────────────────────────────────────
    if any(p in msg for p in ["praga", "inseto", "lagarta", "pulgao", "pulgão", "mosca", "bicho", "doenca", "doença", "fungo"]):
        return "🐛 Monitore as plantas 2x por semana. Para pulgões, aplique extrato de nim ou calda bordalesa. Joaninhas e vespas são aliadas naturais — evite inseticidas amplos que as eliminam."

    # ── Milho ──────────────────────────────────────
    if "milho" in msg:
        return "🌽 Plante milho no início da estação chuvosa. Variedades crioulas adaptadas ao semiárido resistem melhor à seca. Consórcie com feijão para aproveitar melhor o solo!"

    # ── Feijão ─────────────────────────────────────
    if any(p in msg for p in ["feijao", "feijão"]):
        return "🫘 O feijão-de-corda é o mais indicado para o semiárido. Plante no início das chuvas e consórcie com milho — o feijão fixa nitrogênio no solo, beneficiando os dois."

    # ── Seca ───────────────────────────────────────
    if any(p in msg for p in ["seca", "estiagem", "chuva", "clima", "calor"]):
        return "☀️ Na seca, priorize culturas resistentes como palma forrageira, mandacaru e feijão-de-corda. Cisterna e barragem calçada são essenciais para guardar água da chuva."

    # ── Plantio ────────────────────────────────────
    if any(p in msg for p in ["plantio", "plantar", "semente", "muda", "época", "epocа"]):
        return "🌾 Plante sempre no início das chuvas. Sementes crioulas adaptadas à região resistem melhor ao calor e à irregularidade do semiárido. Deixe espaçamento adequado para ventilação."

    # ── Colheita ───────────────────────────────────
    if any(p in msg for p in ["colheita", "colher", "armazenar", "armazenamento", "estoque"]):
        return "🧺 Colha no ponto certo! Tomate sai verde-maduro para suportar o transporte. Grãos como milho e feijão devem secar até 13% de umidade antes de armazenar para evitar fungos."

    # ── Palma ──────────────────────────────────────
    if "palma" in msg:
        return "🌵 A palma forrageira é uma das melhores opções para o semiárido! Resiste bem à seca, serve de alimentação para o gado e precisa de pouca água. Plante em fileiras duplas para melhor aproveitamento."

    # ── Caprinocultura / Bovinocultura ─────────────
    if any(p in msg for p in ["bode", "cabra", "gado", "vaca", "animal", "ração", "racao"]):
        return "🐐 Para criação de animais no semiárido, a palma forrageira é excelente como ração. Bodes e ovelhas adaptados à região (como o Morada Nova) são mais resistentes ao calor e à seca."

    # ── Resposta padrão ────────────────────────────
    return random.choice([
        "🌾 Boa pergunta! Pode me dar mais detalhes sobre sua lavoura? Assim consigo te ajudar melhor com dicas práticas para o semiárido.",
        "👨‍🌾 Não entendi muito bem. Pode reformular? Estou aqui para ajudar com irrigação, pragas, solo, plantio e colheita no Nordeste!",
        "🌱 Me conta mais sobre sua situação! Qual cultura você está plantando e qual é o problema que está enfrentando?",
    ])

# ═══════════════════════════════════════════════════


def chamar_openrouter(or_messages):
    """Chama a API do OpenRouter. Retorna o texto ou None se falhar."""
    payload = {"model": MODEL, "messages": or_messages}
    req = Request(
        API_URL,
        data    = json.dumps(payload).encode(),
        headers = {
            "Content-Type":  "application/json",
            "Authorization": f"Bearer {API_KEY}",
            "HTTP-Referer":  "http://localhost:5000",
            "X-Title":       "Karkara IA",
        },
        method = "POST",
    )
    try:
        with urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read())
        texto = data["choices"][0]["message"]["content"]
        return texto if texto and texto.strip() else None
    except Exception as e:
        print(f"  >> OpenRouter falhou: {e}")
        return None


class KarkaraHandler(BaseHTTPRequestHandler):

    def log_message(self, fmt, *args):
        print(f"  [{self.address_string()}] {fmt % args}")

    def do_OPTIONS(self):
        self._cors(204)

    def do_POST(self):
        if not self.path.startswith("/api/chat"):
            self._json({"error": "Rota nao encontrada."}, 404)
            return

        length = int(self.headers.get("Content-Length", 0))
        body   = json.loads(self.rfile.read(length) or b"{}")

        system   = body.get("system", "")
        messages = body.get("messages", [])

        # pega o texto da última mensagem do usuário
        ultima_msg = ""
        for m in reversed(messages):
            if m.get("role") == "user":
                c = m.get("content", "")
                ultima_msg = c if isinstance(c, str) else " ".join(
                    p.get("text","") for p in c if p.get("type")=="text"
                )
                break

        # tenta OpenRouter primeiro
        texto = None
        if API_KEY:
            or_messages = []
            if system:
                or_messages.append({"role": "system", "content": system})
            for msg in messages:
                role    = msg.get("role", "user")
                content = msg.get("content", "")
                if isinstance(content, list):
                    content = " ".join(p.get("text","") for p in content if p.get("type")=="text")
                or_messages.append({"role": role, "content": content})
            texto = chamar_openrouter(or_messages)

        # se OpenRouter falhar, usa as respostas locais
        if not texto:
            texto = get_resposta(ultima_msg)
            print(f"  >> Resposta local: {texto[:60]}...")
        else:
            print(f"  >> OpenRouter OK: {texto[:60]}...")

        self._json({"content": [{"type": "text", "text": texto}]})

    def do_GET(self):
        if self.path in ("/", "/karkara.htm"):
            html_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "karkara.htm")
            if os.path.exists(html_path):
                with open(html_path, "rb") as f:
                    content = f.read()
                self.send_response(200)
                self._add_cors()
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(content)
                return
        self._json({"error": "Nao encontrado."}, 404)

    def _cors(self, code=200):
        self.send_response(code)
        self._add_cors()
        self.end_headers()

    def _add_cors(self):
        self.send_header("Access-Control-Allow-Origin",  "*")
        self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def _json(self, data, code=200):
        body = json.dumps(data, ensure_ascii=False).encode()
        self.send_response(code)
        self._add_cors()
        self.send_header("Content-Type",   "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


if __name__ == "__main__":
    print("=" * 54)
    print("  Karkara IA - Servidor Local")
    print("=" * 54)
    if not API_KEY:
        print("  Modo local (sem OpenRouter)")
    else:
        print("  OpenRouter ativo!")
    print(f"  Acesse: http://{HOST}:{PORT}")
    print("  Para parar: Ctrl + C")
    print("=" * 54)
    server = HTTPServer((HOST, PORT), KarkaraHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n  Servidor encerrado.")
