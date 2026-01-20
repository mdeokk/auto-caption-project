"""
import os
import subprocess
from pathlib import Path

def download_audio(youtube_url: str) -> str:
    # 1) 저장 폴더 준비
    audio_dir = Path("input") / "audio"
    audio_dir.mkdir(parents=True, exist_ok=True)

    # 2) 출력 템플릿(확장자는 yt-dlp가 결정 → mp3 변환 후 mp3로 저장)
    outtmpl = str(audio_dir / "audio.%(ext)s")

    command = [
        "yt-dlp",
        "--no-playlist",
        "-x",
        "--audio-format", "mp3",
        "-o", outtmpl,
        youtube_url
    ]

    # 3) 실행 및 오류 처리
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(
            "yt-dlp 실행 실패입니다.\n"
            "ffmpeg 미설치/경로 문제이거나 URL이 잘못되었을 수 있습니다.\n"
            f"{result.stderr}"
        )

    # 4) 최종 mp3 경로 반환
    mp3_path = audio_dir / "audio.mp3"
    if not mp3_path.exists():
        raise FileNotFoundError(f"mp3 파일이 생성되지 않았습니다: {mp3_path}")

    return str(mp3_path)

if __name__ == "__main__" :
    download_audio("https://www.youtube.com/watch?v=0-q1KafFCLU")
"""



import os
import subprocess
from pathlib import Path

FFMPEG_PATH = r"C:\ffmpeg\bin"  # ffmpeg.exe, ffprobe.exe 위치
JS_RUNTIME = "deno"  # 또는 "node"

def download_audio(youtube_url: str) -> str:
    audio_dir = Path("input") / "audio"
    audio_dir.mkdir(parents=True, exist_ok=True)

    # 영상 제목 기반 파일명 생성
    outtmpl = str(audio_dir / "%(title)s.%(ext)s")

    command = [
        "yt-dlp",
        "--no-playlist",

        # 오디오 추출
        "-x", "--audio-format", "mp3",

        # ffmpeg 위치 지정
        f"--ffmpeg-location={FFMPEG_PATH}",

        # EJS 대응: JS 런타임 설정
        "--extractor-args", f"youtube:js-runtimes={JS_RUNTIME}",

        # 출력 템플릿
        "-o", outtmpl,

        youtube_url,
    ]

    result = subprocess.run(command, capture_output=True, text=True)

    if result.returncode != 0:
        print("\n=== yt-dlp stderr ===")
        print(result.stderr)
        raise RuntimeError("yt-dlp 실행 실패: 위 stderr 로그 참고")

    # mp3 파일 탐색
    mp3_files = list(audio_dir.glob("*.mp3"))

    if not mp3_files:
        raise FileNotFoundError("mp3 파일이 생성되지 않았습니다.")

    return str(mp3_files[0])


if __name__ == "__main__":
    path = download_audio("https://www.youtube.com/watch?v=0-q1KafFCLU")
    print("다운로드 완료:", path)
