#!/usr/bin/env python3
import asyncio
import base64
import json
import os
import urllib.request
from datetime import datetime

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp import types

server = Server("google-tts")

VOICES_FR = {
    "fr-FR-Neural2-A": "Femme - Naturelle (recommandée)",
    "fr-FR-Neural2-B": "Homme - Professionnel",
    "fr-FR-Neural2-C": "Femme - Expressive",
    "fr-FR-Neural2-D": "Homme - Chaleureux",
    "fr-FR-Neural2-E": "Femme - Dynamique",
    "fr-FR-Wavenet-A": "Femme - WaveNet",
    "fr-FR-Wavenet-B": "Homme - WaveNet",
    "fr-FR-Wavenet-C": "Femme - WaveNet expressive",
    "fr-FR-Wavenet-D": "Homme - WaveNet chaleureux",
}


@server.list_tools()
async def list_tools():
    return [
        types.Tool(
            name="generate_voiceover",
            description="Génère une voix off en français (MP3) via Google Cloud TTS Neural2",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "Texte à convertir en voix off"
                    },
                    "voice": {
                        "type": "string",
                        "description": "Voix à utiliser (défaut: fr-FR-Neural2-A)",
                        "default": "fr-FR-Neural2-A",
                        "enum": list(VOICES_FR.keys())
                    },
                    "output_file": {
                        "type": "string",
                        "description": "Nom du fichier de sortie (optionnel)"
                    },
                    "speaking_rate": {
                        "type": "number",
                        "description": "Vitesse de parole: 0.5 (lent) à 2.0 (rapide), défaut 1.0",
                        "default": 1.0
                    },
                    "pitch": {
                        "type": "number",
                        "description": "Tonalité: -20 (grave) à +20 (aigu), défaut 0",
                        "default": 0
                    }
                },
                "required": ["text"]
            }
        ),
        types.Tool(
            name="list_voices",
            description="Liste toutes les voix françaises disponibles",
            inputSchema={"type": "object", "properties": {}}
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "list_voices":
        lines = ["Voix françaises disponibles:\n"]
        for voice_id, description in VOICES_FR.items():
            lines.append(f"• {voice_id} — {description}")
        return [types.TextContent(type="text", text="\n".join(lines))]

    if name != "generate_voiceover":
        raise ValueError(f"Outil inconnu: {name}")

    api_key = os.environ.get("GOOGLE_CLOUD_API_KEY")
    if not api_key:
        return [types.TextContent(
            type="text",
            text="Erreur: variable GOOGLE_CLOUD_API_KEY non définie. "
                 "Ajoutez votre clé API Google Cloud dans les secrets Claude Code."
        )]

    text = arguments["text"]
    voice = arguments.get("voice", "fr-FR-Neural2-A")
    speaking_rate = float(arguments.get("speaking_rate", 1.0))
    pitch = float(arguments.get("pitch", 0))

    lang_code = "-".join(voice.split("-")[:2])
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = arguments.get("output_file", f"voiceovers/voiceover_{timestamp}.mp3")

    os.makedirs(os.path.dirname(output_file) if os.path.dirname(output_file) else ".", exist_ok=True)

    payload = {
        "input": {"text": text},
        "voice": {"languageCode": lang_code, "name": voice},
        "audioConfig": {
            "audioEncoding": "MP3",
            "speakingRate": speaking_rate,
            "pitch": pitch
        }
    }

    url = f"https://texttospeech.googleapis.com/v1/text:synthesize?key={api_key}"
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url, data=data,
        headers={"Content-Type": "application/json"}
    )

    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read())

        audio_bytes = base64.b64decode(result["audioContent"])

        with open(output_file, "wb") as f:
            f.write(audio_bytes)

        size_kb = len(audio_bytes) // 1024
        return [types.TextContent(
            type="text",
            text=f"Voix off générée avec succès !\n"
                 f"Fichier : {output_file}\n"
                 f"Voix : {voice} ({VOICES_FR.get(voice, '')})\n"
                 f"Taille : {size_kb} KB"
        )]

    except urllib.error.HTTPError as e:
        error_body = e.read().decode()
        return [types.TextContent(type="text", text=f"Erreur API Google: {e.code} — {error_body}")]
    except Exception as e:
        return [types.TextContent(type="text", text=f"Erreur: {str(e)}")]


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
