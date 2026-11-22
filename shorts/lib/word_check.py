#!/usr/bin/env python3
"""Ancien contrôle mot par mot (remplacé par lib/voice_audit.py : réécoute de TOUTE la voix, fenêtres mot + mot suivant, détection de la
lettre lue seule). Gardé pour les anciennes habitudes : appelle voice_audit.py. usage: word_check.py <episode_dir>"""
import os, subprocess, sys
sys.exit(subprocess.call([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), "voice_audit.py")] + sys.argv[1:2]))
