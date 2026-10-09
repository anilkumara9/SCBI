#!/bin/bash
# EXP151 supervisor: relaunches exp151_run.py if it dies before reaching a
# terminal summary outcome. Survives agent death (run under setsid).
# Terminal outcomes (break, no relaunch): HELD, RUN-INVALID, INCONCLUSIVE,
# PROCEED_TO_VERDICT, or 2280 records complete. Anything else -> relaunch.
cd ~/workspace/SCBI/experiments/runs/EXP151
PY=/home/hatch/workspace/.venv-exp111/bin/python
ATTEMPT=0
while true; do
  ATTEMPT=$((ATTEMPT + 1))
  echo "[supervise-151] attempt $ATTEMPT starting $(date -u +%FT%TZ)" >> exp151_supervise.log
  "$PY" exp151_run.py >> exp151_run_stdout.log 2>&1
  code=$?
  echo "[supervise-151] attempt $ATTEMPT exited code=$code $(date -u +%FT%TZ)" >> exp151_supervise.log
  n=$(wc -l < exp151_per_item.jsonl)
  outcome=$(python3 -c "import json; print(json.load(open('exp151_run_summary.json')).get('outcome',''))" 2>/dev/null)
  echo "[supervise-151] records=$n outcome=$outcome" >> exp151_supervise.log
  if [ "$n" -ge 2280 ]; then
    echo "[supervise-151] complete set reached; stopping" >> exp151_supervise.log
    break
  fi
  case "$outcome" in
    HELD|RUN-INVALID|INCONCLUSIVE|PROCEED_TO_VERDICT)
      echo "[supervise-151] terminal outcome $outcome; stopping" >> exp151_supervise.log
      break
      ;;
  esac
  echo "[supervise-151] non-terminal (code=$code records=$n outcome=$outcome); sleeping 60s then relaunch" >> exp151_supervise.log
  sleep 60
done
