from pathlib import Path
import urllib.request
import urllib.error
import shutil
import tempfile
import zipfile

REMOTE_VERSION_URL = "https://hlkprvkrsfzamphemlut.supabase.co/storage/v1/object/public/UserCode/Current/version.txt"
REMOTE_EXE_URL = "https://hlkprvkrsfzamphemlut.supabase.co/storage/v1/object/public/UserCode/Current/Oblique%20Orthographic%20Conduit.exe"
REMOTE_INTERNAL_ZIP_URL = "https://hlkprvkrsfzamphemlut.supabase.co/storage/v1/object/public/UserCode/Current/_internal.zip"
GITHUB_RELEASES_URL = "https://github.com/Fap1bit/Oblique-Orthographic-Conduit/releases"

INTERNAL_DIR = Path("_internal")
WIN32_DIR = INTERNAL_DIR / "win32"
LOCAL_VERSION_PATH = WIN32_DIR / "version.txt"

EXE_NAME = "Oblique Orthographic Conduit.exe"
LOCAL_EXE_PATH = Path(EXE_NAME)


def parse_version(v: str):
    v = (v or "").strip()
    parts = [p.strip() for p in v.split(".") if p.strip()]
    nums = []
    for p in parts:
        num = ""
        for ch in p:
            if ch.isdigit():
                num += ch
            else:
                break
        nums.append(int(num) if num else 0)
    return tuple(nums)


def safe_read_text(path: Path) -> str | None:
    if not path.exists():
        return None
    try:
        return path.read_text(encoding="utf-8").strip()
    except UnicodeDecodeError:
        return path.read_text(encoding="gbk", errors="ignore").strip()
    except Exception:
        return None


def fetch_text_url(url: str, timeout: int = 15) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "Python-urllib-updater/1.0"}, method="GET")
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        data = resp.read()
    try:
        return data.decode("utf-8").strip()
    except UnicodeDecodeError:
        return data.decode("latin1", errors="ignore").strip()


def write_local_version(text: str):
    WIN32_DIR.mkdir(parents=True, exist_ok=True)
    LOCAL_VERSION_PATH.write_text(text.strip() + "\n", encoding="utf-8")


def download_file(url: str, dst: Path, timeout: int = 60):
    tmp = dst.with_suffix(dst.suffix + ".download_tmp")
    if tmp.exists():
        try:
            tmp.unlink()
        except Exception:
            pass

    req = urllib.request.Request(url, headers={"User-Agent": "Python-urllib-updater/1.0"}, method="GET")
    with urllib.request.urlopen(req, timeout=timeout) as resp, open(tmp, "wb") as f:
        while True:
            chunk = resp.read(256 * 1024)
            if not chunk:
                break
            f.write(chunk)

    if dst.exists():
        dst.unlink()
    tmp.rename(dst)


def update_internal_from_zip(url: str):
    print("Updating _internal from cloud package...")
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        zip_path = tmpdir_path / "_internal.zip"
        download_file(url, zip_path, timeout=120)

        extract_root = tmpdir_path / "extract"
        extract_root.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(zip_path, "r") as zf:
            zf.extractall(extract_root)

        inner_dir = extract_root / "_internal"
        src_dir = inner_dir if inner_dir.exists() else extract_root
        if not src_dir.exists():
            raise RuntimeError("internal package missing after extract")
        if not any(src_dir.iterdir()):
            raise RuntimeError("internal package is empty")

        if INTERNAL_DIR.exists():
            shutil.rmtree(INTERNAL_DIR)
        shutil.move(str(src_dir), str(INTERNAL_DIR))
    print("Internal update complete.")


def main():
    print("== 更新检测 ==")

    if not INTERNAL_DIR.exists():
        print("缺少 _internal 文件夹：程序缺失文件。")
        return

    local_raw = safe_read_text(LOCAL_VERSION_PATH)
    if local_raw is None:
        print("本地 version.txt 不存在。")
    else:
        print(f"本地版本：{local_raw}")

    try:
        remote_raw = fetch_text_url(REMOTE_VERSION_URL)
    except urllib.error.URLError as e:
        print(f"获取云端版本失败：{e}")
        return

    #git
    remote_raw = remote_raw.strip()
    need_github = "#git" in remote_raw.lower()
    need_internal = "#int" in remote_raw.lower()

    # 比较的版本号
    remote_ver_str = remote_raw.split()[0] if remote_raw else ""
    remote_ver = parse_version(remote_ver_str)

    if need_internal:
        try:
            update_internal_from_zip(REMOTE_INTERNAL_ZIP_URL)
        except Exception as e:
            print(f"Internal update failed: {e}")
            return

    if need_github:
        # 提示去 github
        print(f"云端版本标记为 GitHub 发布：{remote_raw}")
        # 写入 version.txt
        write_local_version(remote_raw)
        print(f"请前往 GitHub 下载更新：{GITHUB_RELEASES_URL}")
        print(f"已同步版本信息到：{remote_ver_str}")
        return

    # 不带 git
    local_ver = parse_version((local_raw or "").split()[0] if local_raw else "")
    if local_raw is None:
        # version.txt 不存在 -> 按云端写
        write_local_version(remote_raw)
        print(f"已写入版本文件：{remote_ver_str}")
        print(f"更新信息：{GITHUB_RELEASES_URL}")
        return

    if local_ver < remote_ver:
        print(f"发现新版本：{remote_ver_str}，开始更新程序...")
        try:
            if LOCAL_EXE_PATH.exists():
                LOCAL_EXE_PATH.unlink()
            download_file(REMOTE_EXE_URL, LOCAL_EXE_PATH)
            write_local_version(remote_raw)
        except PermissionError:
            print("更新失败：exe 可能正在运行或权限不足，请关闭程序后重试。")
            return
        except Exception as e:
            print(f"更新失败：{e}")
            return

        print(f"更新完成：已更新到 {remote_ver_str}")
        print(f"版本发布页：{GITHUB_RELEASES_URL}")
        return

    if local_ver > remote_ver:
        # 高于云端 -> 按云端覆盖写
        write_local_version(remote_raw)
        print(f"本地版本高于云端，已按云端覆盖 version.txt：{remote_ver_str}")
        print(f"版本发布页：{GITHUB_RELEASES_URL}")
        return

    # 相等
    print("当前已是最新版本，无需更新。")
    print(f"版本发布页：{GITHUB_RELEASES_URL}")


if __name__ == "__main__":
    main()
