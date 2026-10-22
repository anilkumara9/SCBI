#!/bin/bash
# EXP151 run supervisor (third watcher lane, 2026-10-09).
# Survives agent death: keeps exp151_run.py alive until the registered complete set exists.
# One writer at a time: never launches a second exp151_run.py while one is alive.
DIR=~/workspace/SCBI/experiments/runs/EXP151
LOG=$DIR/exp151_supervisor.log
TARGET=2280
cd "$DIR"
echo "[sup] started $(date -u +%F_%T)" >> "$LOG"
while true; do
  N=$(grep -c . exp151_per_item.jsonl 2>/dev/null || echo 0)
  if [ "$N" -ge "$TARGET" ]; then
    echo "[sup] complete set reached ($N records) at $(date -u +%F_%T)" >> "$LOG"
    exit 0
  fi
  if pgrep -f "exp151_run\.py" > /dev/null; then
    echo "[sup] alive, records=$N at $(date -u +%F_%T)" >> "$LOG"
  else
    echo "[sup] process dead at $(date -u +%F_%T), records=$N — validating tail" >> "$LOG"
    python3 - <<'EOF' >> "$LOG" 2>&1
import json
path = 'exp151_per_item.jsonl'
lines = open(path).read().splitlines()
ok = sum(1 for l in lines if l.strip())
bad = 0
for i, l in enumerate(lines):
    if not l.strip(): continue
    try: json.loads(l)
    except Exception:
        bad += 1
        # truncate partial tail
        open(path, 'w').write('\n'.join(lines[:i]) + ('\n' if i else ''))
        print(f'[sup] truncated partial line at {i}')
        break
print(f'[sup] validation: {ok} lines, {bad} partial')
EOF
    setsid /home/hatch/workspace/.venv-exp111/bin/python exp151_run.py >> "$LOG" 2>&1 < /dev/null &
    echo "[sup] relaunched pid $! at $(date -u +%F_%T)" >> "$LOG"
    sleep 120
  fi
  sleep 600
done
