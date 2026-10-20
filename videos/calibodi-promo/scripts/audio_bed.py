#!/usr/bin/env python3
"""Procedural music bed + SFX for the CaliBodi promo, ducked under the voiceover.

Writes assets/audio/music.wav, assets/audio/sfx.wav and assets/audio/bed.wav (48 kHz stereo).
Everything is seeded, so re-running produces the same audio.
"""
import json
import os
import subprocess

import numpy as np
from scipy.ndimage import maximum_filter1d, uniform_filter1d
from scipy.signal import butter, sosfilt, fftconvolve

PROJECT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TL = json.load(open(os.path.join(PROJECT, "timeline.json")))
SR = 48000
TOTAL = TL["total"]
N = int(TOTAL * SR)
BEAT = 60.0 / TL["bpm"]
BAR0 = TL["bar_offset"]
rng = np.random.default_rng(42)


# ---------------------------------------------------------------- helpers
def t_arr(dur):
    return np.arange(int(dur * SR)) / SR


def lp(x, f, order=2):
    return sosfilt(butter(order, min(f, SR / 2 - 100), "low", fs=SR, output="sos"), x)


def hp(x, f, order=2):
    return sosfilt(butter(order, f, "high", fs=SR, output="sos"), x)


def bp(x, lo, hi, order=2):
    return sosfilt(butter(order, [lo, hi], "band", fs=SR, output="sos"), x)


def saw(f, dur, n=None, phase=0.0):
    t = t_arr(dur)
    n = n or max(1, min(40, int(16000 / f)))
    out = np.zeros_like(t)
    for k in range(1, n + 1):
        out += np.sin(2 * np.pi * k * f * t + phase * k) / k
    return out * (2 / np.pi)


def env_adsr(n, a=0.005, d=0.1, s=0.6, r=0.1):
    e = np.ones(n) * s
    na, nd, nr = int(a * SR), int(d * SR), int(r * SR)
    na = min(na, n)
    e[:na] = np.linspace(0, 1, na, endpoint=False)
    nd = min(nd, n - na)
    e[na:na + nd] = np.linspace(1, s, nd, endpoint=False)
    if nr > 0 and nr < n:
        e[-nr:] *= np.linspace(1, 0, nr)
    return e


def exp_env(n, tau):
    return np.exp(-np.arange(n) / (tau * SR))


def place(buf, sig, t, gain=1.0, pan=0.0):
    i = int(round(t * SR))
    if i >= buf.shape[1] or i + len(sig) <= 0:
        return
    s0 = max(0, -i)
    sig = sig[s0:]
    i = max(0, i)
    n = min(len(sig), buf.shape[1] - i)
    l = np.cos((pan + 1) * np.pi / 4)
    r = np.sin((pan + 1) * np.pi / 4)
    buf[0, i:i + n] += sig[:n] * gain * l * 1.414
    buf[1, i:i + n] += sig[:n] * gain * r * 1.414


def noise(dur):
    return rng.standard_normal(int(dur * SR))


# ---------------------------------------------------------------- instruments
CACHE = {}


def kick(strength=1.0):
    key = ("kick", strength)
    if key not in CACHE:
        t = t_arr(0.45)
        f = 46 + 110 * np.exp(-t / 0.035)
        ph = 2 * np.pi * np.cumsum(f) / SR
        body = np.sin(ph) * exp_env(len(t), 0.16)
        click = hp(noise(0.006), 2500) * 0.35
        body[: len(click)] += click
        CACHE[key] = np.tanh(body * 1.6 * strength) * 0.9
    return CACHE[key]


def clap():
    if "clap" not in CACHE:
        n = noise(0.3)
        e = np.zeros(len(n))
        for off in (0.0, 0.011, 0.022):
            i = int(off * SR)
            e[i:] += exp_env(len(n) - i, 0.008 if off < 0.02 else 0.09)
        CACHE["clap"] = bp(n * e, 900, 5000) * 0.9
    return CACHE["clap"]


def hat(open_=False):
    key = ("hat", open_)
    if key not in CACHE:
        d = 0.32 if open_ else 0.05
        n = hp(noise(d), 7000, 4)
        CACHE[key] = n * exp_env(len(n), 0.09 if open_ else 0.014) * (0.55 if open_ else 0.5)
    return CACHE[key]


def bass(f, dur):
    key = ("bass", round(f, 2), dur)
    if key not in CACHE:
        n = int(dur * SR)
        s = lp(saw(f, dur, 24), 420, 2) * 0.7 + np.sin(2 * np.pi * f * t_arr(dur)) * 0.6
        CACHE[key] = s * env_adsr(n, 0.004, 0.08, 0.7, 0.04)
    return CACHE[key]


def sub(f, dur):
    key = ("sub", round(f, 2), dur)
    if key not in CACHE:
        n = int(dur * SR)
        CACHE[key] = np.sin(2 * np.pi * f * t_arr(dur)) * env_adsr(n, 0.02, 0.2, 0.85, 0.3)
    return CACHE[key]


def supersaw(freqs, dur, cutoff, detune=(-0.18, -0.08, 0, 0.08, 0.18), a=0.004, d=0.12, s=0.35, r=0.08):
    key = ("ss", tuple(round(f, 2) for f in freqs), dur, cutoff, a, d, s, r)
    if key not in CACHE:
        n = int(dur * SR)
        out = np.zeros(n)
        for f in freqs:
            for j, dt in enumerate(detune):
                ff = f * 2 ** (dt / 12)
                out += saw(ff, dur, 18, phase=j * 1.3)
        out = lp(out / (len(freqs) * len(detune)) * 2.2, cutoff, 2)
        CACHE[key] = out * env_adsr(n, a, d, s, r)
    return CACHE[key]


def pluck(f, dur=0.32, bright=4500):
    key = ("pl", round(f, 2), dur, bright)
    if key not in CACHE:
        n = int(dur * SR)
        s = saw(f, dur, 14) * 0.6 + np.sin(2 * np.pi * 2 * f * t_arr(dur)) * 0.25
        CACHE[key] = lp(s, bright, 2) * exp_env(n, 0.08)
    return CACHE[key]


def pad(freqs, dur, cutoff=1400):
    n = int(dur * SR)
    out = np.zeros(n)
    for f in freqs:
        for j, dt in enumerate((-0.1, 0.0, 0.1)):
            out += saw(f * 2 ** (dt / 12), dur, 12, phase=j * 2.1)
    out = lp(out / (len(freqs) * 3) * 2.0, cutoff, 2)
    return out * env_adsr(n, 0.6, 0.5, 0.85, min(0.8, dur * 0.4))


def crash(dur=2.6):
    n = noise(dur)
    return hp(n, 4500, 2) * exp_env(len(n), 0.7) * 0.5


def boom(dur=1.8, f0=48):
    t = t_arr(dur)
    f = f0 + 70 * np.exp(-t / 0.08)
    ph = 2 * np.pi * np.cumsum(f) / SR
    return np.tanh(np.sin(ph) * exp_env(len(t), 0.55) * 1.8) * 0.95


def riser(dur, f0=200, f1=2400, noise_amt=0.6):
    t = t_arr(dur)
    n = noise(dur)
    sweep = np.zeros_like(n)
    blocks = 64
    for b in range(blocks):
        i0, i1 = b * len(n) // blocks, (b + 1) * len(n) // blocks
        fc = 600 * (8000 / 600) ** (b / blocks)
        sweep[i0:i1] = bp(n[max(0, i0 - 400):i1], fc * 0.6, min(fc * 1.6, 20000))[-(i1 - i0):]
    f = f0 * (f1 / f0) ** (t / dur)
    tone = np.sin(2 * np.pi * np.cumsum(f) / SR) * 0.25
    e = (t / dur) ** 2.2
    return (sweep * noise_amt + tone) * e


def whoosh(dur=0.5, lo=300, hi=6000, rev=False):
    n = noise(dur)
    t = t_arr(dur)
    out = np.zeros_like(n)
    blocks = 32
    for b in range(blocks):
        i0, i1 = b * len(n) // blocks, (b + 1) * len(n) // blocks
        x = b / blocks
        fc = lo * (hi / lo) ** (np.sin(np.pi * x) if not rev else x)
        out[i0:i1] = bp(n[max(0, i0 - 300):i1], max(60, fc * 0.5), min(fc * 1.8, 20000))[-(i1 - i0):]
    e = np.sin(np.pi * np.clip(t / dur, 0, 1)) ** 2 if not rev else (t / dur) ** 3
    return out * e * 0.8


def ping(f=1568, dur=0.5):
    t = t_arr(dur)
    s = (np.sin(2 * np.pi * f * t) + 0.5 * np.sin(2 * np.pi * f * 1.5 * t)) * exp_env(len(t), 0.11)
    s2 = np.zeros_like(s)
    i = int(0.07 * SR)
    s2[i:] = (np.sin(2 * np.pi * f * 1.335 * t[: len(t) - i])) * exp_env(len(t) - i, 0.14)
    return (s + s2 * 0.8) * 0.35


def pop(f=600, dur=0.12):
    t = t_arr(dur)
    ff = f * (1 + 1.4 * np.exp(-t / 0.012))
    return np.sin(2 * np.pi * np.cumsum(ff) / SR) * exp_env(len(t), 0.03) * 0.6


def tick(f=2600):
    t = t_arr(0.03)
    return np.sin(2 * np.pi * f * t) * exp_env(len(t), 0.005) * 0.5


def blip(f=1800, dur=0.09):
    t = t_arr(dur)
    return np.sign(np.sin(2 * np.pi * f * t)) * exp_env(len(t), 0.025) * 0.18


def shutter():
    a = hp(noise(0.05), 1500) * exp_env(int(0.05 * SR), 0.006)
    out = np.zeros(int(0.16 * SR))
    out[: len(a)] += a
    i = int(0.075 * SR)
    out[i:i + len(a)] += a * 0.8
    return out * 0.9


def bloop(f0=280, f1=900, dur=0.14):
    t = t_arr(dur)
    f = f0 * (f1 / f0) ** (t / dur)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * t / dur) * 0.5


def glitch(dur=0.25):
    n = noise(dur)
    steps = np.repeat(n[::180], 180)[: len(n)]
    gate = (np.floor(t_arr(dur) * 40) % 2).astype(float)
    return bp(steps * gate, 300, 4000) * 0.4


def chime(freqs, dur=1.2):
    t = t_arr(dur)
    out = np.zeros_like(t)
    for k, f in enumerate(freqs):
        i = int(k * 0.06 * SR)
        out[i:] += np.sin(2 * np.pi * f * t[: len(t) - i]) * exp_env(len(t) - i, 0.35)
    return out * 0.22


def shimmer(dur=0.9):
    t = t_arr(dur)
    out = np.zeros_like(t)
    for f in (2637, 3136, 3951, 4699):
        out += np.sin(2 * np.pi * f * t + f) * (0.5 + 0.5 * np.sin(2 * np.pi * 14 * t + f))
    return out * np.sin(np.pi * t / dur) ** 2 * 0.06


def reverb_ir(dur=2.4, decay=0.55):
    n = int(dur * SR)
    ir = np.stack([rng.standard_normal(n), rng.standard_normal(n)]) * exp_env(n, decay)
    ir = np.stack([lp(ir[0], 6000), lp(ir[1], 6000)])
    pre = np.zeros((2, int(0.02 * SR)))
    ir = np.concatenate([pre, ir], axis=1)
    return ir / np.sqrt(np.sum(ir ** 2, axis=1, keepdims=True))


def stereo_reverb(buf, ir, wet):
    out = np.zeros_like(buf)
    mono = buf.mean(axis=0)
    for c in range(2):
        out[c] = fftconvolve(mono, ir[c])[: buf.shape[1]]
    return out * wet


# ---------------------------------------------------------------- arrangement
A2, C3, E3 = 110.0, 130.81, 164.81
CHORDS = [
    {"name": "Am", "stab": [220.0, 261.63, 329.63], "root": 55.0, "arp": [440.0, 523.25, 659.25, 880.0]},
    {"name": "F", "stab": [174.61, 220.0, 261.63], "root": 43.65, "arp": [349.23, 440.0, 523.25, 698.46]},
    {"name": "C", "stab": [196.0, 261.63, 329.63], "root": 65.41, "arp": [392.0, 523.25, 659.25, 783.99]},
    {"name": "G", "stab": [196.0, 246.94, 293.66], "root": 49.0, "arp": [392.0, 493.88, 587.33, 783.99]},
]


def chord_at(t):
    k = int(np.floor((t - BAR0) / (4 * BEAT)))
    return CHORDS[k % 4]


def section(t):
    if t < 7.6:
        return "hook"
    if t < 11.0:
        return "declic"
    if t < 35.0:
        return "groove"
    if t < 41.5:
        return "recup"
    if t < 46.5:
        return "hydra"
    if t < 61.0:
        return "final"
    return "end"


drums = np.zeros((2, N))
bassbus = np.zeros((2, N))
synth = np.zeros((2, N))
padbus = np.zeros((2, N))
fxm = np.zeros((2, N))
kick_times = []

grid = np.arange(0.0, TOTAL, BEAT / 4)  # 16th notes
for i, t in enumerate(grid):
    sec = section(t)
    pos16 = int(round((t - BAR0) / (BEAT / 4))) % 16
    beat_pos = pos16 % 4 == 0
    beat_idx = (pos16 // 4)
    ch = chord_at(t)

    if sec == "hook" and t >= 0.6:
        if beat_pos and beat_idx in (0, 2):
            place(drums, kick(0.55), t, 0.55)
            kick_times.append(t)
        if pos16 % 2 == 0:
            place(drums, hat(), t, 0.22 + (0.12 if t > 5.2 else 0), pan=0.3)
        if t > 5.2 and pos16 % 2 == 1:
            place(drums, hat(), t, 0.16, pan=-0.3)
        if pos16 % 2 == 1:
            place(bassbus, bass(55.0, 0.11), t, 0.45)
    elif sec == "declic":
        if 10.0 <= t < 11.0:
            sub_steps = 1 if t < 10.5 else 2
            place(drums, clap(), t, 0.10 + 0.5 * (t - 10.0), pan=0.0)
            if sub_steps == 2:
                place(drums, clap(), t + BEAT / 8, 0.12 + 0.5 * (t - 10.0))
    elif sec in ("groove", "final"):
        if beat_pos:
            place(drums, kick(1.0), t, 0.72)
            kick_times.append(t)
            if beat_idx in (1, 3):
                place(drums, clap(), t, 0.55)
        vel = [0.32, 0.14, 0.24, 0.14][pos16 % 4]
        place(drums, hat(), t, vel, pan=0.25)
        if pos16 % 4 == 2:
            place(drums, hat(True), t, 0.22, pan=-0.25)
        if pos16 % 4 == 2:
            place(bassbus, bass(ch["root"] * 2, BEAT / 2 * 0.9), t, 0.36)
        if pos16 in (0, 3, 6, 10, 12):
            place(synth, supersaw(ch["stab"], 0.24, 4200), t, 0.52, pan=-0.15 if pos16 % 2 else 0.15)
        arp_on = (t >= 25.0 and sec == "groove") or (sec == "final" and t >= 46.5)
        if arp_on:
            note = ch["arp"][[0, 1, 2, 3, 2, 1, 0, 2][pos16 % 8]]
            place(synth, pluck(note, 0.28, 5200), t, 0.22, pan=0.45 if pos16 % 2 else -0.45)
    elif sec == "recup":
        if pos16 % 4 == 2:
            place(drums, hat(), t, 0.10, pan=0.25)
        if pos16 == 0:
            place(drums, kick(0.5), t, 0.28)
        if pos16 % 2 == 0:
            note = ch["arp"][[0, 2, 1, 3][(pos16 // 2) % 4]]
            place(synth, pluck(note, 0.5, 2600), t, 0.12, pan=0.4 if pos16 % 4 else -0.4)
    elif sec == "hydra":
        if beat_pos and beat_idx in (0, 2):
            place(drums, kick(0.8), t, 0.7)
            kick_times.append(t)
        if t >= 43.5 and beat_pos and beat_idx in (1, 3):
            place(drums, kick(0.8), t, 0.6)
            kick_times.append(t)
        vel = [0.22, 0.1, 0.18, 0.1][pos16 % 4]
        place(drums, hat(), t, vel, pan=0.25)
        note = ch["arp"][[0, 1, 2, 3, 2, 1, 0, 2][pos16 % 8]] * 2
        place(synth, pluck(note, 0.22, 6500), t, 0.11, pan=0.5 if pos16 % 2 else -0.5)
        if pos16 % 4 == 2:
            place(bassbus, bass(ch["root"] * 2, BEAT / 2 * 0.8), t, 0.35)

# pads + subs per bar
bar_starts = np.arange(BAR0 - 4 * BEAT, TOTAL, 4 * BEAT)
for b in bar_starts:
    if b < 0:
        continue
    sec = section(b + 0.01)
    ch = chord_at(b + 0.01)
    dur = 4 * BEAT + 0.6
    if sec == "hook":
        place(padbus, pad([A2, C3, E3], dur, 700), b, 0.22)
    elif sec in ("declic",):
        place(padbus, pad([A2, E3], dur, 500), b, 0.2)
    elif sec in ("groove", "final"):
        place(padbus, pad(ch["stab"], dur, 2200), b, 0.26)
        place(bassbus, sub(ch["root"], 4 * BEAT), b, 0.17)
    elif sec == "recup":
        place(padbus, pad([f for f in ch["stab"]] + [ch["stab"][0] * 2], dur, 1100), b, 0.32)
        place(bassbus, sub(ch["root"], 4 * BEAT), b, 0.22)
    elif sec == "hydra":
        place(padbus, pad(ch["stab"], dur, 1500), b, 0.22)
        place(bassbus, sub(ch["root"], 4 * BEAT), b, 0.17)

# structural hits / risers in the music
place(fxm, riser(0.6, 120, 900, 0.4), 0.0, 0.25)
place(fxm, whoosh(0.45, 6000, 200, rev=True), 7.55, 0.7)
place(fxm, boom(1.4, 42), 8.0, 0.55)
place(fxm, riser(2.0, 180, 2600), 9.0, 0.55)
for t in (11.0, 46.5, 54.5):
    place(fxm, boom(1.8, 44), t, 0.9)
    place(fxm, crash(2.8), t, 0.55, pan=0.0)
place(fxm, riser(1.5, 220, 2400), 45.0, 0.45)
place(fxm, riser(1.5, 220, 3000), 53.0, 0.5)
# final chord + tail
place(padbus, pad([220.0, 261.63, 329.63, 440.0], 2.2, 2400), 61.0, 0.45)
place(synth, supersaw([220.0, 261.63, 329.63], 2.0, 3000, a=0.002, d=0.4, s=0.4, r=1.2), 61.0, 0.5)
place(drums, kick(1.0), 61.0, 0.9)
place(fxm, crash(2.0), 61.0, 0.45)
place(fxm, boom(1.9, 44), 61.0, 0.8)

# sidechain pump on bass/synth/pad
pump = np.ones(N)
for kt in kick_times:
    i = int(kt * SR)
    L = min(int(0.3 * SR), N - i)
    pump[i:i + L] = np.minimum(pump[i:i + L], 1 - 0.55 * np.exp(-np.arange(L) / (0.09 * SR)))
for bus in (bassbus, synth, padbus):
    bus *= pump

ir = reverb_ir()
music = drums + bassbus * 0.9 + synth + padbus + fxm
music += stereo_reverb(synth * 0.6 + padbus * 0.5 + fxm * 0.3 + drums * 0.08, ir, 0.35)
music = np.stack([hp(c, 32, 2) - 0.45 * lp(c, 110, 2) for c in music])
music[:, int(62.2 * SR):] *= np.linspace(1, 0, N - int(62.2 * SR)) ** 1.5

# ---------------------------------------------------------------- SFX cues (absolute seconds)
sfx = np.zeros((2, N))
S = {s["id"]: s["start"] for s in TL["scenes"]}


def at(scene, local):
    return S[scene] + local


cues = []
# 01 chaos
for t, f in ((0.62, 1568), (2.08, 1760), (3.56, 1976)):
    cues += [(at("01-chaos", t), pop(220, 0.14), 0.6, 0.3), (at("01-chaos", t + 0.08), ping(f), 0.55, 0.35)]
cues += [(at("01-chaos", 4.3), ping(2093), 0.5, 0.4), (at("01-chaos", 5.36), glitch(0.3), 0.6, 0.2)]
for k, t in enumerate((6.32, 6.46, 6.6)):
    cues.append((at("01-chaos", t), ping(1568 * 2 ** (k * 2 / 12)), 0.42, 0.5 - k * 0.4))
for k, t in enumerate((6.38, 6.62, 6.86, 7.08)):
    cues.append((at("01-chaos", t), ping(1760 * 2 ** ((k % 3) * 3 / 12)), 0.42, -0.4 + k * 0.3))
cues += [(at("01-chaos", 6.3), glitch(0.5), 0.35, 0.0), (at("01-chaos", 6.9), glitch(0.4), 0.4, 0.2)]
# 02 declic
cues += [(at("02-declic", 0.0), whoosh(1.6, 200, 1200), 0.25, 0.3), (at("02-declic", 1.96), kick(1.0), 0.8, 0.0),
         (at("02-declic", 1.96), clap(), 0.6, 0.0), (at("02-declic", 1.97), tick(4200), 0.6, 0.0)]
# 03 reveal
cues += [(at("03-reveal", 0.02), whoosh(0.8, 300, 8000), 0.35, 0.0), (at("03-reveal", 0.95), shimmer(0.9), 1.0, 0.2)]
for k in range(10):
    cues.append((at("03-reveal", 1.98 + k * 0.085), tick(2400 + 200 * (k % 3)), 0.25, 0.3))
for k, t in enumerate((3.98, 4.09, 4.2, 4.31)):
    cues.append((at("03-reveal", t), pop(700 * 2 ** (k * 4 / 12), 0.1), 0.45, -0.6 + 0.4 * k))
# wipes
for b in (16.5, 25.0, 35.0, 41.5):
    cues.append((b - 0.42, whoosh(0.85, 200, 7000), 0.75, 0.0))
# 04 sport
cues += [(at("04-sport", 0.3), whoosh(0.7, 150, 1500), 0.3, 0.3)]
for k, t in enumerate((0.9, 1.15, 1.4)):
    cues.append((at("04-sport", t), pop(500 + 120 * k, 0.12), 0.45, [-0.3, 0.5, 0.6][k]))
for t in (1.82, 2.43, 3.2):
    cues.append((at("04-sport", t), blip(1400, 0.07), 0.6, -0.4))
cues += [(at("04-sport", 4.4), whoosh(0.6, 400, 5000), 0.35, 0.2), (at("04-sport", 4.55), pop(820, 0.14), 0.5, 0.5)]
for k, t in enumerate((6.28, 6.62, 7.0)):
    cues.append((at("04-sport", t), blip(1047 * 2 ** (k * 2 / 12), 0.1), 0.7, -0.3))
cues.append((at("04-sport", 7.15), chime([1047, 1319, 1568, 2093]), 1.0, 0.0))
# 05 nutrition
cues += [(at("05-nutrition", 1.04), shutter(), 0.9, -0.3), (at("05-nutrition", 1.45), whoosh(1.0, 1200, 4000), 0.18, -0.3)]
for k, t in enumerate((2.0, 2.36, 2.68)):
    cues.append((at("05-nutrition", t), blip(1760 + 220 * k, 0.08), 0.7, -0.4))
for k in range(9):
    cues.append((at("05-nutrition", 3.6 + k * 0.08), tick(3000), 0.22, 0.4))
cues.append((at("05-nutrition", 5.0), whoosh(0.5, 300, 5000), 0.35, 0.0))
for k in range(9):
    cues.append((at("05-nutrition", 5.23 + k * 0.08), tick(2600 + 60 * k), 0.24, -0.4))
cues.append((at("05-nutrition", 6.95), chime([1319, 1760]), 0.9, 0.0))
for k, t in enumerate((8.05, 8.25, 8.45, 8.65)):
    cues += [(at("05-nutrition", t), pop(600 + 60 * k, 0.1), 0.4, -0.5), (at("05-nutrition", t + 0.3), tick(3400), 0.4, -0.5)]
# 06 recup
cues += [(at("06-recup", 1.15), whoosh(0.9, 300, 1800), 0.18, 0.3)]
t6 = t_arr(0.9)
glide = np.sin(2 * np.pi * np.cumsum(880 * (0.6 ** (t6 / 0.9))) / SR) * np.sin(np.pi * t6 / 0.9) * 0.15
cues += [(at("06-recup", 2.7), glide, 0.8, 0.4), (at("06-recup", 3.5), pop(700, 0.12), 0.4, 0.4)]
# 07 hydratation
cues += [(at("07-hydratation", 0.45), bloop(260, 700), 0.6, -0.5), (at("07-hydratation", 1.8), bloop(300, 900), 0.55, -0.5),
         (at("07-hydratation", 3.05), pop(760, 0.12), 0.5, 0.0), (at("07-hydratation", 3.15), bloop(340, 1100), 0.6, -0.5)]
for k, (t, f0) in enumerate(((0.95, 500), (1.5, 620), (2.3, 560), (2.9, 700), (3.5, 650), (3.9, 800))):
    cues.append((at("07-hydratation", t), bloop(f0, f0 * 2.2, 0.08), 0.25, -0.6 + 0.2 * k))
# 08 connecte
for k, t in enumerate((0.32, 1.12, 2.08, 3.24)):
    f = [440.0, 523.25, 659.25, 880.0][k]
    cues += [(at("08-connecte", t), supersaw([f, f * 1.5], 0.6, 5000, a=0.002, d=0.25, s=0.2, r=0.2), 0.42, [-0.5, 0.5, 0.5, -0.5][k]),
             (at("08-connecte", t), pop(500, 0.1), 0.35, 0.0)]
cues += [(at("08-connecte", 4.28), whoosh(0.7, 800, 9000), 0.3, 0.0), (at("08-connecte", 5.2), whoosh(0.5, 6000, 300, rev=True), 0.5, 0.0),
         (at("08-connecte", 5.62), boom(1.0, 60), 0.4, 0.0), (at("08-connecte", 5.75), shimmer(1.0), 1.0, 0.0)]
for k in range(10):
    cues.append((at("08-connecte", 5.85 + k * 0.09), tick(2800 + 40 * k), 0.2, 0.0))
for k in range(7):
    cues.append((at("08-connecte", 6.88 + k * 0.09), blip(880 * 2 ** ([0, 2, 4, 5, 7, 9, 12][k] / 12), 0.07), 0.45, -0.6 + 0.2 * k))
# 09 cta
cues += [(at("09-cta", 0.15), pop(520, 0.16), 0.5, -0.4), (at("09-cta", 0.8), shimmer(0.8), 1.0, -0.4),
         (at("09-cta", 3.0), pop(700, 0.12), 0.45, -0.4), (at("09-cta", 4.22), pop(900, 0.12), 0.45, -0.4),
         (at("09-cta", 5.08), chime([1568, 2093]), 0.6, -0.5), (at("09-cta", 5.68), chime([1760, 2349]), 0.6, -0.3), (at("09-cta", 6.4), shimmer(0.8), 0.9, -0.4)]

for t, sig, g, pan in cues:
    place(sfx, sig, t, g, pan)
sfx += stereo_reverb(sfx, ir, 0.22)

# ---------------------------------------------------------------- duck music under voice
vo_env = np.zeros(N)
for s in TL["scenes"]:
    data = subprocess.run(["ffmpeg", "-v", "error", "-i", os.path.join(PROJECT, s["vo_file"]), "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"],
                          capture_output=True, check=True).stdout
    v = np.frombuffer(data, dtype=np.float32)
    i = int(s["vo_start"] * SR)
    n = min(len(v), N - i)
    vo_env[i:i + n] = np.maximum(vo_env[i:i + n], np.abs(v[:n]))
win = int(0.05 * SR)
vo_env = uniform_filter1d(vo_env, size=win)
active = (vo_env > 0.01).astype(float)
held = maximum_filter1d(active, size=int(0.3 * SR))
duck = 1 - 0.62 * uniform_filter1d(held, size=int(0.12 * SR))
music *= duck


def write(path, x, target_peak=0.89):
    x = x / max(1e-9, np.max(np.abs(x))) * target_peak
    pcm = (np.clip(x, -1, 1) * 32767).astype(np.int16).T.copy()
    raw = path + ".raw"
    pcm.tofile(raw)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "s16le", "-ar", str(SR), "-ac", "2", "-i", raw, path], check=True)
    os.remove(raw)


out_dir = os.path.join(PROJECT, "assets", "audio")
os.makedirs(out_dir, exist_ok=True)
music = np.tanh(music * 0.9)
write(os.path.join(out_dir, "music.wav"), music)
write(os.path.join(out_dir, "sfx.wav"), sfx)

# bed = music (loudness-normalised, under the voice) + sfx
mpath, spath, bpath = (os.path.join(out_dir, f) for f in ("music.wav", "sfx.wav", "bed.wav"))
meas = subprocess.run(["ffmpeg", "-i", mpath, "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
lufs = float([l for l in meas.splitlines() if l.strip().startswith("I:")][-1].split()[1])
gain_db = -22.5 - lufs
subprocess.run([
    "ffmpeg", "-v", "error", "-y", "-i", mpath, "-i", spath, "-filter_complex",
    f"[0]volume={gain_db:.2f}dB[m];[1]volume=0.55[s];[m][s]amix=inputs=2:normalize=0:duration=first,alimiter=limit=0.89:level=false[o]",
    "-map", "[o]", "-ar", str(SR), "-ac", "2", bpath,
], check=True)
print("wrote", mpath, spath, bpath, f"{TOTAL}s, {len(kick_times)} kicks, {len(cues)} sfx cues")
