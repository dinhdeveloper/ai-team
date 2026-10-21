#!/usr/bin/env bash
# Phát hành phiên bản mới của plugin ai-team và cập nhật trên máy.
#
# Cách dùng:
#   ./scripts/release.sh patch "Sửa lỗi hook"          # 1.4.1 -> 1.4.2
#   ./scripts/release.sh minor "Thêm lệnh /status"     # 1.4.1 -> 1.5.0
#   ./scripts/release.sh major "Đổi quy trình"         # 1.4.1 -> 2.0.0
#   ./scripts/release.sh 1.6.0 "Đặt version cụ thể"
#   ./scripts/release.sh update                         # chỉ cập nhật plugin trên máy (không đổi version)
#
# Tùy chọn (đặt sau nội dung):
#   --no-push     commit + tag trên máy, không push, không cập nhật plugin
#   --dry-run     chỉ in ra sẽ làm gì, không thay đổi gì
set -euo pipefail

PLUGIN="ai-team"
MARKETPLACE="dinh-tools"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
MANIFEST="$ROOT/.claude-plugin/plugin.json"
CHANGELOG="$ROOT/CHANGELOG.md"

red()   { printf '\033[31m%s\033[0m\n' "$*"; }
green() { printf '\033[32m%s\033[0m\n' "$*"; }
blue()  { printf '\033[34m%s\033[0m\n' "$*"; }
die()   { red "✖ $*"; exit 1; }

update_local_plugin() {
  if ! command -v claude >/dev/null 2>&1; then
    red "Không tìm thấy lệnh 'claude' — bỏ qua bước cập nhật plugin trên máy."
    echo "Tự chạy sau: claude plugin update $PLUGIN@$MARKETPLACE"
    return
  fi
  blue "→ Cập nhật plugin trên máy"
  claude plugin marketplace update "$MARKETPLACE" || true
  if claude plugin list 2>/dev/null | grep -q "$PLUGIN@$MARKETPLACE"; then
    claude plugin update "$PLUGIN@$MARKETPLACE"
  else
    claude plugin install "$PLUGIN@$MARKETPLACE"
  fi
  claude plugin list 2>/dev/null | grep -A3 "$PLUGIN@$MARKETPLACE" || true
  green "✔ Xong. Mở phiên 'claude' mới (hoặc gõ /reload-plugins trong phiên đang mở)."
}

[ $# -ge 1 ] || { sed -n '2,15p' "$0"; exit 1; }
BUMP="$1"; shift

if [ "$BUMP" = "update" ]; then
  update_local_plugin
  exit 0
fi

MESSAGE="${1:-}"; [ $# -ge 1 ] && shift
[ -n "$MESSAGE" ] || die "Thiếu nội dung thay đổi. Vd: ./scripts/release.sh patch \"Sửa lỗi hook\""
PUSH=1; DRY=0
for opt in "$@"; do
  case "$opt" in
    --no-push) PUSH=0 ;;
    --dry-run) DRY=1 ;;
    *) die "Tùy chọn không hợp lệ: $opt" ;;
  esac
done

command -v python3 >/dev/null || die "Cần python3"
cd "$ROOT"
git rev-parse --is-inside-work-tree >/dev/null 2>&1 || die "Không phải git repo: $ROOT"

BRANCH="$(git branch --show-current)"
[ "$BRANCH" = "main" ] || die "Đang ở nhánh '$BRANCH'. Chuyển về main trước khi phát hành."

CURRENT="$(python3 -c 'import json,sys;print(json.load(open(sys.argv[1]))["version"])' "$MANIFEST")"
NEXT="$(python3 - "$CURRENT" "$BUMP" <<'PY'
import re, sys
cur, bump = sys.argv[1], sys.argv[2]
m = re.fullmatch(r"(\d+)\.(\d+)\.(\d+)", cur)
if not m:
    sys.exit(f"version hiện tại không hợp lệ: {cur}")
ma, mi, pa = map(int, m.groups())
if bump == "patch":   pa += 1
elif bump == "minor": mi, pa = mi + 1, 0
elif bump == "major": ma, mi, pa = ma + 1, 0, 0
elif re.fullmatch(r"\d+\.\d+\.\d+", bump):
    if tuple(map(int, bump.split("."))) <= (ma, mi, pa):
        sys.exit(f"version mới {bump} phải lớn hơn {cur}")
    print(bump); sys.exit()
else:
    sys.exit("loại nâng version phải là patch | minor | major | x.y.z")
print(f"{ma}.{mi}.{pa}")
PY
)" || die "Không tính được version mới"

git rev-parse "v$NEXT" >/dev/null 2>&1 && die "Tag v$NEXT đã tồn tại"

blue "→ Kiểm tra plugin"
for f in .claude-plugin/plugin.json .claude-plugin/marketplace.json hooks/hooks.json; do
  python3 -c 'import json,sys;json.load(open(sys.argv[1]))' "$f" || die "JSON lỗi: $f"
done
python3 -c 'import ast,sys;ast.parse(open(sys.argv[1]).read())' hooks/guard.py || die "hooks/guard.py lỗi cú pháp"
for f in agents/*.md commands/*.md; do
  head -1 "$f" | grep -q '^---$' || die "Thiếu frontmatter: $f"
done
green "✔ Plugin hợp lệ"

echo
blue "Phát hành: $CURRENT → $NEXT"
echo "  Nội dung : $MESSAGE"
echo "  Push     : $([ $PUSH = 1 ] && echo có || echo không)"
git status --short | sed 's/^/  /'
echo

if [ $DRY = 1 ]; then green "(dry-run) Không thay đổi gì."; exit 0; fi

python3 - "$MANIFEST" "$NEXT" <<'PY'
import json, sys
p, v = sys.argv[1], sys.argv[2]
d = json.load(open(p, encoding="utf-8"))
d["version"] = v
open(p, "w", encoding="utf-8").write(json.dumps(d, ensure_ascii=False, indent=2) + "\n")
PY

python3 - "$CHANGELOG" "$NEXT" "$MESSAGE" <<'PY'
import datetime, os, sys
p, v, msg = sys.argv[1:4]
head = "# Changelog\n\n"
body = open(p, encoding="utf-8").read() if os.path.exists(p) else head
if body.startswith(head):
    body = body[len(head):]
entry = f"## v{v} — {datetime.date.today():%Y-%m-%d}\n- {msg}\n\n"
open(p, "w", encoding="utf-8").write(head + entry + body)
PY

git add -A
git commit -m "ai-team v$NEXT: $MESSAGE"
git tag -a "v$NEXT" -m "ai-team v$NEXT: $MESSAGE"
green "✔ Đã commit + tag v$NEXT"

if [ $PUSH = 0 ]; then
  echo "Chưa push. Khi sẵn sàng: git push && git push origin v$NEXT && ./scripts/release.sh update"
  exit 0
fi

blue "→ Push lên GitHub"
git push origin main
git push origin "v$NEXT"
green "✔ Đã push v$NEXT"

update_local_plugin
