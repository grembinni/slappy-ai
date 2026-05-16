import argparse
import pathlib
import shutil
import subprocess
import sys

from PIL import Image


def convert_ico(src: pathlib.Path, dst: pathlib.Path, size: int = 128) -> bool:
    try:
        dst.parent.mkdir(parents=True, exist_ok=True)
        img = Image.open(src).convert("RGBA").resize((size, size), Image.NEAREST)
        img.save(dst, "PNG")
        return True
    except (Image.UnidentifiedImageError, OSError) as exc:
        print(f"ERROR converting {src.name}: {exc}")
        return False


def convert_midi(
    midi_path: pathlib.Path, wav_path: pathlib.Path, soundfont_path: pathlib.Path
) -> bool:
    if shutil.which("fluidsynth") is None:
        print("ERROR: FluidSynth is not installed or not on PATH.")
        print("Install: winget install FluidSynth.FluidSynth  OR  conda install -c conda-forge fluidsynth")
        sys.exit(1)
    try:
        wav_path.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(
            [
                "fluidsynth",
                "-ni",
                str(soundfont_path),
                str(midi_path),
                "-F",
                str(wav_path),
                "-r",
                "44100",
            ],
            check=True,
        )
        return True
    except subprocess.CalledProcessError as exc:
        print(f"ERROR converting {midi_path.name}: {exc}")
        return False


def copy_wav(src: pathlib.Path, dst: pathlib.Path) -> bool:
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(str(src), str(dst))
    return True


def main():
    parser = argparse.ArgumentParser(description="Convert raw_assets/ to assets/")
    parser.add_argument(
        "--soundfont",
        type=pathlib.Path,
        default=pathlib.Path("tools/TimGM6mb.sf2"),
    )
    parser.add_argument("--skip-midi", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if not args.dry_run and not args.skip_midi:
        if not args.soundfont.exists():
            print(f"ERROR: Soundfont not found at {args.soundfont}")
            print("Place TimGM6mb.sf2 at tools/TimGM6mb.sf2 or pass --soundfont <path>")
            sys.exit(1)

    RAW_ICONS = pathlib.Path("raw_assets/icons")
    RAW_SOUNDS = pathlib.Path("raw_assets/sounds")
    OUT_SPRITES = pathlib.Path("assets/sprites")
    OUT_SOUNDS = pathlib.Path("assets/sounds")

    if not args.dry_run:
        OUT_SPRITES.mkdir(parents=True, exist_ok=True)
        OUT_SOUNDS.mkdir(parents=True, exist_ok=True)

    ico_count = 0
    seen: set = set()
    ico_files = sorted(RAW_ICONS.glob("*.ico")) + sorted(RAW_ICONS.glob("*.ICO"))
    for ico in ico_files:
        if ico.name.lower() in seen:
            continue
        seen.add(ico.name.lower())
        dst = OUT_SPRITES / (ico.stem.lower() + ".png")
        if args.dry_run:
            print(f"[DRY RUN] {ico} -> {dst}")
        else:
            convert_ico(ico, dst)
        ico_count += 1

    wav_count = 0
    seen_wav: set = set()
    wav_files = sorted(RAW_SOUNDS.glob("*.wav")) + sorted(RAW_SOUNDS.glob("*.WAV"))
    for wav in wav_files:
        if wav.name.lower() in seen_wav:
            continue
        seen_wav.add(wav.name.lower())
        dst = OUT_SOUNDS / (wav.stem.lower() + ".wav")
        if args.dry_run:
            print(f"[DRY RUN] {wav} -> {dst}")
        else:
            copy_wav(wav, dst)
        wav_count += 1

    midi_count = 0
    if args.skip_midi:
        print("SKIPPING MIDI: --skip-midi flag set")
    else:
        for mid in sorted(RAW_SOUNDS.glob("*.mid")):
            dst = OUT_SOUNDS / (mid.stem.lower() + ".wav")
            if args.dry_run:
                print(f"[DRY RUN] {mid} -> {dst}")
            else:
                convert_midi(mid, dst, args.soundfont)
            midi_count += 1

    if args.dry_run:
        print(f"[DRY RUN] Would convert {ico_count} ICO, {wav_count} WAV, {midi_count} MIDI files")
    else:
        print(f"Done. Converted {ico_count} ICO files, {wav_count} WAV files, {midi_count} MIDI files.")


if __name__ == "__main__":
    main()
