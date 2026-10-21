"""Saves downloads to ~/Downloads without keeping any download history."""
from pathlib import Path


def _unique_path(path: Path) -> Path:
    if not path.exists():
        return path
    i = 1
    while True:
        candidate = path.with_name(f"{path.stem} ({i}){path.suffix}")
        if not candidate.exists():
            return candidate
        i += 1


def attach_download_handler(profile):
    def on_download(request):
        folder = Path.home() / "Downloads"
        folder.mkdir(exist_ok=True)
        target = _unique_path(folder / (request.downloadFileName() or "download"))
        request.setDownloadDirectory(str(folder))
        request.setDownloadFileName(target.name)
        request.accept()          # file is saved, but no list of downloads is kept

    profile.downloadRequested.connect(on_download)
