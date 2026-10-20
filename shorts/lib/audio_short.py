#!/usr/bin/env python3
"""Music bed + sound effects for a Calix short, mixed under the voice (Signature CaliBodi).

usage: audio_short.py <episode_dir>

Reads  plan.json ("science" ranges, "sfx" cues, "blocks") and assets/voice/voice.wav.
Writes assets/audio/music.wav, assets/audio/sfx.wav (48 kHz stereo) and renders/mix-preview.wav,
then prints a loudness / masking report.

Rules applied:
- instrumental only, quiet, carved out of the 1-4 kHz speech band and ducked whenever Calix talks;
- extra reduction inside plan["science"] ranges (and no drums there);
- every effect is band-limited to < 150 Hz or > 2.5 kHz, nudged into the nearest breath, and its gain is
  capped against the voice around it; an effect that lands on a word attack is lowered further.
  If it still cannot stay under the voice it is dropped (absolute rule: a word always wins).
Everything is seeded, so re-running gives the same audio.
"""
import json
import os
import subprocess
import sys

import numpy as np
from scipy.ndimage import maximum_filter1d, uniform_filter1d
from scipy.signal import butter, fftconvolve, sosfilt

EP = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else ".")
plan = json.load(open(os.path.join(EP, "plan.json")))
words = json.load(open(os.path.join(EP, "assets/voice/words.json")))
SR = 48000
D = round(words["duration"] + plan.get("tail", 0.6), 2)          # same length as build_short.py
blocks = plan["blocks"]
N = int(D * SR)
BPM = plan.get("bpm", 90)
BEAT = 60.0 / BPM
rng = np.random.default_rng(7)

MUSIC_LUFS = plan.get("music_lufs", -29.5)   # ducked bed, integrated
DUCK_DB = plan.get("duck_db", -7.0)          # extra drop while Calix speaks
SCIENCE_DB = plan.get("science_db", -5.0)    # extra drop during scientific explanations


# ---------------------------------------------------------------- dsp helpers
def t_arr(d):
    return np.arange(int(d * SR)) / SR


def lp(x, f, o=2):
    return sosfilt(butter(o, min(f, SR / 2 - 100), "low", fs=SR, output="sos"), x)


def hp(x, f, o=2):
    return sosfilt(butter(o, f, "high", fs=SR, output="sos"), x)


def bp(x, lo, hi, o=2):
    return sosfilt(butter(o, [lo, hi], "band", fs=SR, output="sos"), x)


def out_of_voice_band(x):
    """Keep only < 150 Hz and > 2.5 kHz (speech intelligibility lives in between)."""
    return lp(x, 150, 4) + hp(x, 2500, 4)


def expd(n, tau):
    return np.exp(-np.arange(n) / (tau * SR))


def adsr(n, a, d, s, r):
    e = np.full(n, float(s))
    na = min(int(a * SR), n)
    e[:na] = np.linspace(0, 1, na, endpoint=False)
    nd = min(int(d * SR), n - na)
    e[na:na + nd] = np.linspace(1, s, nd, endpoint=False)
    nr = min(int(r * SR), n)
    if nr:
        e[-nr:] *= np.linspace(1, 0, nr)
    return e


def place(buf, sig, t, gain=1.0, pan=0.0):
    i = int(round(t * SR))
    if i >= buf.shape[1] or i + len(sig) <= 0:
        return
    s0 = max(0, -i)
    sig = sig[s0:]
    i = max(0, i)
    n = min(len(sig), buf.shape[1] - i)
    buf[0, i:i + n] += sig[:n] * gain * np.cos((pan + 1) * np.pi / 4) * 1.414
    buf[1, i:i + n] += sig[:n] * gain * np.sin((pan + 1) * np.pi / 4) * 1.414


def noise(d):
    return rng.standard_normal(int(d * SR))


def reverb_ir(d=1.8, decay=0.45):
    n = int(d * SR)
    ir = np.stack([lp(rng.standard_normal(n) * expd(n, decay), 5000) for _ in range(2)])
    ir = np.concatenate([np.zeros((2, int(0.015 * SR))), ir], axis=1)
    return ir / np.sqrt(np.sum(ir ** 2, axis=1, keepdims=True))


def reverb(buf, ir, wet):
    m = buf.mean(axis=0)
    return np.stack([fftconvolve(m, ir[c])[:buf.shape[1]] for c in range(2)]) * wet


def lufs(x):
    x = np.atleast_2d(x).astype(np.float32)
    err = subprocess.run(["ffmpeg", "-f", "f32le", "-ar", str(SR), "-ac", str(x.shape[0]), "-i", "-", "-af", "ebur128", "-f", "null", "-"],
                         input=x.T.copy().tobytes(), capture_output=True).stderr.decode()
    return float([l for l in err.splitlines() if l.strip().startswith("I:")][-1].split()[1])


def write(path, x):
    x = np.atleast_2d(x)
    if x.shape[0] == 1:
        x = np.vstack([x, x])
    pcm = (np.clip(x, -1, 1) * 32767).astype(np.int16).T.copy()
    raw = path + ".raw"
    pcm.tofile(raw)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "s16le", "-ar", str(SR), "-ac", "2", "-i", raw, path], check=True)
    os.remove(raw)


# ---------------------------------------------------------------- voice analysis
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", os.path.join(EP, "assets/voice/voice.wav"), "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"],
                     capture_output=True, check=True).stdout
voice = np.zeros(N)
v = np.frombuffer(raw, np.float32)
voice[:min(len(v), N)] = v[:N]
HOP = int(0.01 * SR)  # 10 ms frames


def frame_rms(x, win=0.03):
    p = uniform_filter1d(x ** 2, size=int(win * SR))
    return np.sqrt(p[::HOP] + 1e-12)


v_rms = frame_rms(voice)
v_hi = frame_rms(hp(voice, 2500, 4))
speech_ref = np.percentile(v_rms[v_rms > 0.01], 70)
active = v_rms > speech_ref * 0.12                      # Calix is talking in this frame
# word attacks: waveform onsets (fast energy rise) + transcript word starts
rise = np.diff(np.log(v_rms + 1e-4), prepend=0)
onsets = set(np.where((rise > 0.9) & active)[0].tolist())
onsets |= {int(w["start"] * 100) for w in words["words"]}
onsets = np.array(sorted(onsets))


# ---------------------------------------------------------------- music: chill lo-fi, 90 bpm
def ep_note(f, d, bright=1.0):
    """Electric-piano-ish note: sine body, soft 2nd partial, quick tine."""
    t = t_arr(d)
    n = len(t)
    s = np.sin(2 * np.pi * f * t) * expd(n, 1.6)
    s += 0.22 * np.sin(2 * np.pi * 2 * f * t) * expd(n, 0.45)
    s += 0.05 * bright * np.sin(2 * np.pi * 7.1 * f * t) * expd(n, 0.04)
    s *= 1 + 0.08 * np.sin(2 * np.pi * 4.6 * t)
    return s * adsr(n, 0.006, 0.2, 0.9, 0.35)


def pad_chord(freqs, d, cut=900):
    t = t_arr(d)
    out = np.zeros(len(t))
    for f in freqs:
        for j, dt in enumerate((-0.07, 0.0, 0.07)):
            ff = f * 2 ** (dt / 12)
            out += sum(np.sin(2 * np.pi * k * ff * t + j * k) / k for k in range(1, 7))
    out = lp(out / (len(freqs) * 3), cut, 2)
    return out * adsr(len(t), 0.8, 0.4, 0.9, min(0.9, d * 0.4))


def sub_note(f, d):
    t = t_arr(d)
    s = np.sin(2 * np.pi * f * t) + 0.18 * np.sin(2 * np.pi * 2 * f * t)
    return s * adsr(len(t), 0.03, 0.3, 0.8, 0.25)


def kick():
    t = t_arr(0.32)
    f = 48 + 70 * np.exp(-t / 0.03)
    return np.tanh(np.sin(2 * np.pi * np.cumsum(f) / SR) * expd(len(t), 0.11) * 1.4) * 0.9


def snap():
    n = hp(noise(0.12), 2600, 2)
    return n * expd(len(n), 0.03) * 0.5


def hat(open_=False):
    d = 0.18 if open_ else 0.04
    n = hp(noise(d), 7500, 4)
    return n * expd(len(n), 0.06 if open_ else 0.012) * 0.45


def bell(f, d=0.9):
    t = t_arr(d)
    s = np.sin(2 * np.pi * f * t) + 0.3 * np.sin(2 * np.pi * 2.76 * f * t) * expd(len(t), 0.12)
    return s * expd(len(t), 0.35) * adsr(len(t), 0.003, 0.05, 1, 0.1)


# Am9 - Fmaj7 - Cmaj7 - Em7, voiced low so the voice keeps the mids
CHORDS = [
    {"ep": [220.0, 261.63, 329.63, 392.0], "root": 55.0, "bell": [1760.0, 2093.0, 2637.0]},
    {"ep": [174.61, 220.0, 261.63, 329.63], "root": 43.65, "bell": [1397.0, 1760.0, 2093.0]},
    {"ep": [196.0, 261.63, 329.63, 392.0], "root": 65.41, "bell": [1568.0, 2093.0, 2637.0]},
    {"ep": [164.81, 196.0, 246.94, 293.66], "root": 41.2, "bell": [1319.0, 1568.0, 1976.0]},
]
science = plan.get("science", [])
outro_t = next((b["start"] for b in blocks if b["type"] == "outro"), D)
first_groove = next((b["start"] for b in blocks if b["type"] != "myth"), 4.0)


def in_science(t):
    return any(a <= t < b for a, b in science)


keys = np.zeros((2, N))
padb = np.zeros((2, N))
low = np.zeros((2, N))
drums = np.zeros((2, N))
bells = np.zeros((2, N))
bar = 4 * BEAT
kick_times = []
for k, b0 in enumerate(np.arange(0, D, bar)):
    ch = CHORDS[k % 4]
    sci = in_science(b0 + 0.01)
    # keys: chord on 1, a softer re-voice on the "and" of 2 (lazy lo-fi comping)
    for j, f in enumerate(ch["ep"]):
        place(keys, ep_note(f, bar * 0.62, 0.8), b0 + j * 0.012, 0.16, pan=-0.25 + 0.17 * j)
        place(keys, ep_note(f * (2 if j == 0 else 1), bar * 0.4, 0.5), b0 + 1.5 * BEAT + 0.02 + j * 0.01, 0.07, pan=0.2 - 0.12 * j)
    place(padb, pad_chord(ch["ep"][:3], bar + 0.5, 700 if sci else 1000), b0, 0.12)
    place(low, sub_note(ch["root"], bar * 0.95), b0, 0.42)
    # bells only in the outro, sparse, above the speech band
    if b0 >= outro_t - 0.01:
        for j, step in enumerate((0, 3, 6, 10)):
            place(bells, bell(ch["bell"][j % 3]), b0 + step * BEAT / 4, 0.05, pan=0.5 if j % 2 else -0.5)
    # drums: none in the hook's first bar, none during science
    for s16 in range(16):
        t = b0 + s16 * BEAT / 4 + (0.035 if s16 % 4 == 2 else 0.0)  # light swing
        if t >= D or t < 0.2 or in_science(t):
            continue
        groove = t >= first_groove
        if groove and s16 in (0, 7, 10):
            place(drums, kick(), t, 0.55 if s16 == 0 else 0.4)
            kick_times.append(t)
        if groove and s16 in (4, 12):
            place(drums, snap(), t, 0.35, pan=0.1)
        if s16 % 2 == 0:
            place(drums, hat(), t, [0.2, 0.11][(s16 // 2) % 2], pan=0.3)
        if groove and s16 == 14:
            place(drums, hat(True), t, 0.1, pan=-0.3)

# gentle sidechain from the kick on keys/pad/sub
pump = np.ones(N)
for kt in kick_times:
    i = int(kt * SR)
    L = min(int(0.25 * SR), N - i)
    pump[i:i + L] = np.minimum(pump[i:i + L], 1 - 0.3 * np.exp(-np.arange(L) / (0.08 * SR)))
for bus in (keys, padb, low):
    bus *= pump

ir = reverb_ir()
music = keys + padb + low + drums * 0.9 + bells
music += reverb(keys * 0.7 + padb * 0.4 + bells, ir, 0.3)
# carve the speech band: -5 dB between 1 and 4 kHz, clean sub rumble
music = np.stack([hp(c, 35, 2) - 0.44 * bp(c, 1000, 4000, 2) for c in music])

# automation: duck under the voice, extra drop in science, fade at the very end
held = maximum_filter1d(active.astype(float), size=25)                 # hold 250 ms
duck_f = uniform_filter1d(held, size=8)                               # ~80 ms ramps
gain_db_f = DUCK_DB * duck_f
sci_f = np.zeros_like(duck_f)
for a, b in science:
    sci_f[int(a * 100):int(b * 100)] = 1
sci_f = uniform_filter1d(sci_f, size=40)                              # 400 ms ramps
gain_db_f += SCIENCE_DB * sci_f
g = 10 ** (np.interp(np.arange(N) / SR, np.arange(len(gain_db_f)) * HOP / SR, gain_db_f) / 20)
music *= g
fade0 = D - 1.6
music[:, int(fade0 * SR):] *= np.linspace(1, 0, N - int(fade0 * SR)) ** 1.6
music[:, :int(0.25 * SR)] *= np.linspace(0, 1, int(0.25 * SR))
music = np.tanh(music * 1.0)
music *= 10 ** ((MUSIC_LUFS - lufs(music)) / 20)


# ---------------------------------------------------------------- sound effects (all out of the voice band)
def sfx_whoosh(d=0.45, up=True):
    n = noise(d)
    t = t_arr(d)
    out = np.zeros_like(n)
    nb = 24
    for k in range(nb):
        i0, i1 = k * len(n) // nb, (k + 1) * len(n) // nb
        x = k / nb if up else 1 - k / nb
        fc = 3000 * (11000 / 3000) ** x
        out[i0:i1] = bp(n[max(0, i0 - 300):i1], fc * 0.7, min(fc * 1.5, 20000))[-(i1 - i0):]
    rumble = lp(noise(d), 120, 4) * 2.5
    return (out + rumble) * np.sin(np.pi * t / d) ** 2


def sfx_thump(f0=52, d=0.6):
    t = t_arr(d)
    f = f0 + 60 * np.exp(-t / 0.04)
    return np.tanh(np.sin(2 * np.pi * np.cumsum(f) / SR) * expd(len(t), 0.18) * 1.6)


def sfx_click(f=3600, d=0.03):
    t = t_arr(d)
    return np.sin(2 * np.pi * f * t) * expd(len(t), 0.004) + hp(noise(d), 4000) * expd(len(t), 0.002) * 0.4


def sfx_stamp():
    s = sfx_thump(46, 0.7)
    c = sfx_click(3200, 0.05) * 0.8
    s[:len(c)] += c
    return s


def sfx_plinks():
    out = np.zeros(int(0.7 * SR))
    for k, f in enumerate((3520, 3136, 2794)):         # falling drops, above 2.5 kHz
        b = bell(f, 0.4) * 0.6
        i = int(k * 0.09 * SR)
        out[i:i + len(b)] += b[:len(out) - i]
    return out


def sfx_warn():
    t = t_arr(0.5)
    low_ = np.sin(2 * np.pi * 70 * t) * adsr(len(t), 0.01, 0.1, 0.8, 0.2)
    beep = np.zeros_like(t)
    for k in range(2):
        i0 = int(k * 0.16 * SR)
        tt = t[:int(0.1 * SR)]
        beep[i0:i0 + len(tt)] += np.sin(2 * np.pi * 2960 * tt) * adsr(len(tt), 0.004, 0.02, 0.8, 0.03)
    return low_ * 0.8 + beep * 0.35


def sfx_check():
    out = bell(2794, 0.35) * 0.5
    b2 = bell(3729, 0.35) * 0.5
    i = int(0.06 * SR)
    out[i:] += b2[:len(out) - i]
    return out


def sfx_shimmer(d=0.9):
    t = t_arr(d)
    out = sum(np.sin(2 * np.pi * f * t + f) * (0.5 + 0.5 * np.sin(2 * np.pi * 13 * t + f)) for f in (2637, 3136, 3951, 4699))
    return out * np.sin(np.pi * t / d) ** 2 * 0.25


def sfx_pop():
    t = t_arr(0.1)
    f = 2900 * (1 + 0.5 * np.exp(-t / 0.01))
    body = np.sin(2 * np.pi * 110 * t) * expd(len(t), 0.03)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * expd(len(t), 0.02) * 0.6 + body * 0.7


# name -> (generator, intended loudness relative to Calix's speech level, in dB, when it lands in a breath)
BANK = {
    "whoosh_in": (lambda: sfx_whoosh(0.5), -6), "whoosh": (lambda: sfx_whoosh(0.4), -6),
    "stamp": (sfx_stamp, 0), "thump": (lambda: sfx_thump(50, 0.6), -2), "plinks": (sfx_plinks, -6),
    "tick": (lambda: sfx_click(3400, 0.03), -10), "click": (lambda: sfx_click(3000, 0.04), -8),
    "warn": (sfx_warn, -6), "check": (sfx_check, -8), "shimmer": (sfx_shimmer, -8), "pop": (sfx_pop, -8),
}

sfx = np.zeros((2, N))
report = []
NUDGE = (-0.10, 0.15)
hi_global = np.percentile(v_hi[active], 80)            # typical consonant level (s, f, t, ch)
for name, t0 in plan.get("sfx", []):
    make, intent_db = BANK[name]
    raw_sig = make()
    lo_sig, hi_sig = lp(raw_sig, 150, 4), hp(raw_sig, 2500, 4)
    pk = np.max(np.abs(lo_sig + hi_sig)) + 1e-9
    lo_sig, hi_sig = lo_sig / pk, hi_sig / pk
    sig = lo_sig + hi_sig
    pad = np.zeros(HOP * 4)
    s_lo = frame_rms(np.concatenate([lo_sig, pad]))
    s_hi = frame_rms(np.concatenate([hi_sig, pad]))
    s_all = np.maximum(s_lo, s_hi)
    loud = np.where(s_all > s_all.max() * 0.25)[0]
    span = (loud[-1] + 1) if len(loud) else 1
    # 1) nudge into the quietest spot nearby (a breath), measured over the effect's audible span
    best, best_e = t0, None
    for dt in np.arange(NUDGE[0], NUDGE[1] + 1e-9, 0.01):
        f0 = int(round((t0 + dt) * 100))
        if f0 < 0:
            continue
        e = v_rms[f0:f0 + span].mean() + 0.002 * abs(dt)            # prefer staying on the cue
        if best_e is None or e < best_e:
            best, best_e = t0 + dt, e
    f0 = int(round(best * 100))
    seg = slice(f0, min(f0 + span, len(v_rms)))
    around = slice(max(0, f0 - 30), min(f0 + span + 30, len(v_rms)))
    act = active[around]
    talking = active[seg].mean() > 0.3
    # 2) caps against the voice around the effect
    if act.any():
        hi_ref = np.percentile(v_hi[around][act], 80)              # this sentence's consonants
        lo_ref = np.median(v_rms[around][act])
    else:
        hi_ref, lo_ref = hi_global, speech_ref
    nominal = speech_ref * 10 ** (intent_db / 20) / (s_all.max() + 1e-9)
    cap = nominal
    n_seg = seg.stop - seg.start
    act_seg = active[seg]
    sh, sl, sa = s_hi[:n_seg], s_lo[:n_seg], s_all[:n_seg]
    if act_seg.any():
        # only the part of the effect that overlaps speech is constrained, at its own level there:
        # its highs stay >= 6 dB under this sentence's consonants, its lows >= 3 dB under the voice
        cap = min(cap, float(np.min(0.5 * hi_ref / (sh[act_seg] + 1e-9))), float(np.min(0.7 * lo_ref / (sl[act_seg] + 1e-9))))
    # 3) a word attack where the effect is still loud -> a further 4 dB down
    on = onsets[(onsets >= seg.start) & (onsets < seg.stop)] - seg.start
    hits = [o for o in on if sa[o] > 0.5 * sa.max()]
    if hits:
        cap *= 0.63
    rel = 20 * np.log10(cap * s_all.max() / speech_ref + 1e-12)
    status = f"{rel:5.1f} dB vs voice"
    if cap < nominal * 10 ** (-15 / 20):                           # would need > 15 dB cut to stay clear: drop it
        status, cap = "dropped (would mask a word)", 0.0
    elif cap < nominal * 0.999:
        status += f" (lowered {20 * np.log10(cap / nominal):.1f} dB" + (", word attack)" if hits else ")")
    if cap > 0:
        place(sfx, sig, best, cap, pan=0.0)
    report.append((name, t0, best, status + ("" if talking else " · in a breath")))

sfx += reverb(sfx, ir, 0.12)

# ---------------------------------------------------------------- write + report
out = os.path.join(EP, "assets", "audio")
os.makedirs(out, exist_ok=True)
os.makedirs(os.path.join(EP, "renders"), exist_ok=True)
write(os.path.join(out, "music.wav"), music)
write(os.path.join(out, "sfx.wav"), sfx)
mix = music + sfx + np.vstack([voice, voice])
write(os.path.join(EP, "renders", "mix-preview.wav"), mix)

lines = [f"duration {D}s · bpm {BPM} · {len(kick_times)} kicks"]
lines += [f"  sfx {name:10s} {t0:6.2f} -> {t1:6.2f}  {st}" for name, t0, t1, st in report]


def band_db(x, lo, hi, mask):
    e = frame_rms(bp(x, lo, hi, 4))[:len(mask)]
    return 20 * np.log10(np.sqrt(np.mean(e[mask[:len(e)]] ** 2)) + 1e-12)


m_mono = music.mean(axis=0)
speech_band_gap = band_db(voice, 300, 3400, active) - band_db(m_mono, 300, 3400, active)
pauses = ~maximum_filter1d(active, size=15)
lines.append(f"voice {lufs(np.vstack([voice, voice])):.1f} LUFS · music {lufs(music):.1f} LUFS · sfx {lufs(sfx):.1f} LUFS · mix {lufs(mix):.1f} LUFS")
lines.append(f"speech band (300-3400 Hz) while talking: voice is {speech_band_gap:.1f} dB above the music")
if pauses.any():
    lines.append(f"music in pauses: {band_db(m_mono, 60, 8000, pauses):.1f} dBFS · voice while talking: {band_db(voice, 60, 8000, active):.1f} dBFS")
open(os.path.join(EP, "renders", "audio-report.txt"), "w").write("\n".join(lines) + "\n")
print("\n".join(lines))
