from pathlib import Path
import json
import os
import platform
import subprocess
import sys
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]


def capture(args: list[str]) -> str:
    env = dict(os.environ, PYTHONIOENCODING='utf-8')
    result = subprocess.run(args, cwd=ROOT, capture_output=True,
                            text=True, encoding='utf-8', env=env)
    if result.returncode:
        raise RuntimeError(result.stdout + result.stderr)
    return result.stdout + result.stderr


def image(name: str, command: str, output: str) -> None:
    folder = ROOT / 'docs/screenshots'
    folder.mkdir(parents=True, exist_ok=True)
    font = ImageFont.truetype('C:/Windows/Fonts/consola.ttf', 19)
    lines = (command + '\n\n' + output).expandtabs(4).splitlines()
    width = max(1100, int(max(font.getlength(line) for line in lines)) + 48)
    canvas = Image.new('RGB', (width, len(lines) * 26 + 48), '#16202b')
    draw = ImageDraw.Draw(canvas)
    for index, line in enumerate(lines):
        draw.text((24, 24 + index * 26), line, font=font, fill='#edf2f7')
    canvas.save(folder / (name + '.png'))


def main() -> None:
    folder = ROOT / 'docs/results'
    folder.mkdir(parents=True, exist_ok=True)
    python = str(ROOT / '.venv/Scripts/python.exe')
    if not Path(python).exists():
        python = sys.executable
    # Take the Git snapshot before creating new evidence files.
    status = capture(['git', 'status'])
    log = capture(['git', 'log', '--oneline', '-6'])
    demo = capture([python, '-m', 'book_manager'])
    tests = capture([python, '-m', 'unittest', 'discover', '-s', 'tests', '-v'])
    bench = capture([python, '-m', 'book_manager', '--benchmark',
                     '--benchmark-output', 'docs/results/benchmark.json'])
    capture([python, '-m', 'book_manager', '--export', 'docs/results/summary.json'])
    for name, content in [('application', demo), ('tests', tests), ('benchmark', bench),
                          ('git_status_lab02', status), ('git_log_lab02', log)]:
        (folder / (name + '.txt')).write_text(content, encoding='utf-8')
    lines = demo.splitlines()
    for number, start in enumerate(range(0, len(lines), 18), 1):
        image(f'lab02_application_{number}', 'python -m book_manager',
              '\n'.join(lines[start:start + 18]))
    image('lab02_benchmark', 'python -m book_manager --benchmark', bench)
    image('lab02_tests', 'python -m unittest discover -s tests -v', tests)
    image('lab02_git_status', 'git status (до підготовки звіту)', status)
    (folder / 'environment.json').write_text(json.dumps({
        'date': '2026-11-07', 'python': sys.version, 'platform': platform.platform(),
        'processor': platform.processor(), 'queries': 200, 'repeats': 5,
        'method': 'median of repeated batches; seconds per lookup',
    }, ensure_ascii=False, indent=2), encoding='utf-8')


if __name__ == '__main__':
    main()
