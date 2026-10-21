#!/usr/bin/env python3
"""
ai-team guard — PreToolUse hook (v1.4).

Quyền ghi theo vai trò
| Vai trò  | Được ghi                                   | Bị chặn                                               |
|----------|--------------------------------------------|-------------------------------------------------------|
| teamlead | docs/sdd/**                                | mọi file khác; Bash ghi/xóa file                      |
| dev      | code production                            | test, testcase, SDD, .ai-team/; Bash ghi/xóa file,    |
|          |                                            | thêm/bớt thư viện                                     |
| tester   | file test, docs/testcases/**               | mọi file khác; Bash ghi/xóa file, đổi dependency      |
| cả ba    |                                            | .ai-team/; git commit/push/reset --hard/clean/merge   |

Khi có task đang chạy (.ai-team/active.json) — chặn theo giai đoạn:
| Vai trò | Chỉ được ghi khi phase là     | Thêm điều kiện                                        |
|---------|-------------------------------|-------------------------------------------------------|
| dev     | IMPLEMENT, FIX                | file nằm trong mục DEV-xx / ADD-xx đã [x] ở checklist |
| tester  | PLAN_REVIEW (testcase)        |                                                       |
|         | TEST (file test)              |                                                       |
Không có task đang chạy: chỉ áp quyền theo vai trò (trừ khi .ai-team/config.json có "strict": true).
Phiên chính (anh / người điều phối) không bị chặn.
"""
import json
import os
import re
import sys

ROLES = ("teamlead", "dev", "tester")
DEV_PHASES = ("IMPLEMENT", "FIX")

TEST_DIRS = (
    "test/", "tests/", "integration_test/", "test_driver/",
    "src/test/", "src/androidtest/", "__tests__/",
)
TEST_FILE_RE = re.compile(r"(_test\.dart|Tests?\.(kt|java)|\.test\.[jt]sx?|\.spec\.[jt]sx?)$")

GIT_FORBIDDEN_RE = re.compile(
    r"\bgit\s+(commit|push|reset\s+--hard|clean|rebase|merge|branch\s+-[dD])\b"
)

FILE_WRITE_BASH = [
    (re.compile(r"(^|[;&|\s])(rm|mv|cp|rmdir|truncate|dd|tee|touch|chmod|ln)\s"), "ghi/xóa/di chuyển file"),
    (re.compile(r"\b(sed|perl)\s+(-[a-zA-Z]*i|--in-place)"), "sửa file tại chỗ"),
    (re.compile(r"\bgit\s+(checkout|restore|stash|apply|am|cherry-pick|revert|rm|mv|add|switch)\b"), "thao tác git làm đổi file"),
]
DEPENDENCY_BASH = [
    (re.compile(r"\b(flutter|dart)\s+pub\s+(add|remove|upgrade|downgrade)\b"), "thêm/bớt/nâng thư viện"),
    (re.compile(r"\b(npm|yarn|pnpm)\s+(install|add|remove|uninstall|upgrade|i)\s+\S"), "thêm/bớt thư viện"),
]
FORMAT_BASH = [
    (re.compile(r"\bdart\s+fix\s+--apply\b|\bdart\s+format\b|\bflutter\s+format\b"), "tự sửa source hàng loạt"),
]

CHECKED_ITEM_RE = re.compile(r"^\s*-\s*\[[xX]\]\s*\*{0,2}((DEV|ADD)-\d+)\*{0,2}(.*)$")
BACKTICK_RE = re.compile(r"`([^`]+)`")


# ---------- helpers ----------

def role_of(agent_type: str) -> str:
    name = (agent_type or "").split(":")[-1].strip().lower()
    return name if name in ROLES else ""


def rel_path(path: str, cwd: str) -> str:
    full = os.path.normpath(os.path.join(cwd or "", path))
    rel = os.path.relpath(full, cwd) if cwd else full
    return rel.replace("\\", "/")


def inside_project(rel: str) -> bool:
    return not (rel == ".." or rel.startswith("../"))


def _has(rel: str, segment: str) -> bool:
    return ("/" + rel.lower()).find(segment) != -1


def is_test_path(rel: str) -> bool:
    low = "/" + rel.lower()
    return any("/" + d in low for d in TEST_DIRS) or bool(TEST_FILE_RE.search(rel))


def is_sdd_path(rel: str) -> bool:
    return _has(rel, "/docs/sdd/")


def is_testcase_path(rel: str) -> bool:
    return _has(rel, "/docs/testcases/")


def is_history_path(rel: str) -> bool:
    return _has(rel, "/.ai-team/")


def has_redirect_write(cmd: str) -> bool:
    cleaned = re.sub(r"\d*>&\d", " ", cmd)                   # 2>&1
    cleaned = re.sub(r"&?\d*>>?\s*/dev/null", " ", cleaned)  # > /dev/null
    return ">" in cleaned


def load_json(path: str):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def active_task(cwd: str):
    """Trả về (state, task_dir) hoặc (None, None)."""
    state = load_json(os.path.join(cwd, ".ai-team", "active.json"))
    if not isinstance(state, dict) or not state.get("task"):
        return None, None
    if str(state.get("phase", "")).upper() == "DONE":
        return None, None
    return state, os.path.join(cwd, ".ai-team", "history", state["task"])


def strict_mode(cwd: str) -> bool:
    cfg = load_json(os.path.join(cwd, ".ai-team", "config.json"))
    return bool(isinstance(cfg, dict) and cfg.get("strict"))


def approved_paths(task_dir: str):
    """Đọc checklist.md: lấy đường dẫn trong các mục DEV-xx / ADD-xx đã [x]."""
    files, dirs = set(), set()
    try:
        with open(os.path.join(task_dir, "checklist.md"), encoding="utf-8") as f:
            lines = f.readlines()
    except Exception:
        return files, dirs
    for line in lines:
        m = CHECKED_ITEM_RE.match(line)
        if not m:
            continue
        for raw in BACKTICK_RE.findall(m.group(3)):
            p = raw.strip()
            p = re.sub(r"\s*\[.*?\]\s*$", "", p)    # bỏ [MỚI]
            p = re.sub(r":\d+(-\d+)?$", "", p)      # bỏ :dòng
            p = p.lstrip("./").replace("\\", "/")
            if not p or (" " in p) or ("/" not in p and "." not in p):
                continue
            (dirs if p.endswith("/") else files).add(p)
    return files, dirs


def deny(reason: str) -> None:
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": "[ai-team guard] " + reason,
        }
    }, ensure_ascii=False))
    sys.exit(0)


# ---------- rules ----------

def check_write(role: str, path: str, cwd: str) -> None:
    rel = rel_path(path, cwd)
    if not inside_project(rel):
        deny(f"{role} không được ghi ngoài project: {path}")
    if is_history_path(rel):
        deny("Lịch sử .ai-team/ chỉ do người điều phối ghi. Hãy trả nội dung trong báo cáo.")

    state, task_dir = active_task(cwd)
    phase = str(state.get("phase", "")).upper() if state else ""

    if role == "teamlead":
        if not is_sdd_path(rel):
            deny(f"Teamlead chỉ được ghi SDD trong docs/sdd/. Bị chặn: {path}.")
        return

    if role == "tester":
        if is_testcase_path(rel):
            if state and phase != "PLAN_REVIEW":
                deny(f"Giai đoạn hiện tại là {phase}. Tester chỉ được lập/sửa testcase ở PLAN_REVIEW. "
                     "Cần sửa testcase → đưa vào 🙋 CẦN ANH DUYỆT.")
            return
        if is_test_path(rel):
            if state and phase != "TEST":
                deny(f"Giai đoạn hiện tại là {phase}. Tester chỉ được viết unit test ở TEST.")
            return
        deny(f"Tester chỉ được ghi file test và docs/testcases/. Bị chặn: {path}. "
             "Nếu đây là lỗi code, ghi vào phần 🐞 Lỗi gửi Dev.")

    # dev
    if is_test_path(rel):
        deny(f"Dev không được sửa file test: {path}. Nếu cho rằng test sai, đưa vào 🙋 CẦN ANH DUYỆT.")
    if is_testcase_path(rel):
        deny(f"Dev không được sửa testcase: {path}. Testcase thuộc tester.")
    if is_sdd_path(rel):
        deny(f"Dev không được sửa SDD: {path}. Góp ý SDD đưa vào 🙋 CẦN ANH DUYỆT.")
    if not state:
        if strict_mode(cwd):
            deny("Chưa có task đang chạy (strict mode). Dùng /ship hoặc /resume trước khi dev sửa code.")
        return
    if phase not in DEV_PHASES:
        deny(f"Giai đoạn hiện tại là {phase}. Dev chỉ được sửa code ở IMPLEMENT hoặc FIX, "
             "sau khi anh đã duyệt checklist.")
    files, dirs = approved_paths(task_dir)
    norm = rel.lstrip("./")
    if norm in files or any(norm.startswith(d) for d in dirs):
        return
    deny(f"File {rel} không có trong mục DEV-xx / ADD-xx đã duyệt ở checklist.md. "
         "Cần sửa file này → đưa vào 🙋 CẦN ANH DUYỆT (loại: File ngoài checklist).")


def check_bash(role: str, cmd: str) -> None:
    if GIT_FORBIDDEN_RE.search(cmd):
        deny("Agent không được commit/push/reset/merge/rebase. Việc này anh tự làm.")
    if ".ai-team/" in cmd and has_redirect_write(cmd):
        deny("Lịch sử .ai-team/ chỉ do người điều phối ghi.")
    for pattern, why in DEPENDENCY_BASH:
        if pattern.search(cmd):
            deny(f"{role} không được {why}. Đưa vào 🙋 CẦN ANH DUYỆT; người điều phối sẽ chạy sau khi anh đồng ý.")
    if has_redirect_write(cmd):
        deny(f"{role} không được ghi file bằng redirect (>). Dùng Write/Edit cho file được phép.")
    for pattern, why in FILE_WRITE_BASH + FORMAT_BASH:
        if pattern.search(cmd):
            deny(f"{role} không được {why} bằng Bash: {cmd[:120]}")


def main() -> None:
    try:
        data = json.load(sys.stdin)
    except Exception:
        sys.exit(0)

    role = role_of(data.get("agent_type", ""))
    if not role:
        sys.exit(0)  # phiên chính hoặc agent khác: không can thiệp

    tool = data.get("tool_name", "")
    ti = data.get("tool_input", {}) or {}
    cwd = data.get("cwd", "") or os.getcwd()

    if tool in ("Edit", "Write", "MultiEdit", "NotebookEdit"):
        check_write(role, ti.get("file_path") or ti.get("notebook_path") or "", cwd)
    elif tool == "Bash":
        check_bash(role, ti.get("command", "") or "")
    sys.exit(0)


if __name__ == "__main__":
    main()
