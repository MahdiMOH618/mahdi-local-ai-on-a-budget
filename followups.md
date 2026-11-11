# Local follow-ups

The user cron entry is daily at 20: 00 in the workstation's verified Asia/Kuwait timezone. The script performs GitHub polling only when the three-day due timestamp is reached. This gives an actual three-day interval across month boundaries, rather than using every-third-day-of-month cron syntax.

Only public repository stars, issues/pull requests and comments are collected. Strata Discussions are disabled and no external issue is part of this successful-only release. There is no automated reply/posting operation: the code uses explicit GET requests only.

Summaries and suggested replies are saved locally in `~/publish-benchmarks/followups/YYYY-MM-DD.md`, with matching numbered draft JSON. The directory is excluded from Git. A desktop notification appears only if there are new or updated items. After reviewing a file, tell the assistant `send` or `send 1 and 3` to authorize those exact replies, with your edits if supplied.

Pause:

```bash
python3 ~/publish-benchmarks/scripts/manage_followups.py pause
```

Resume:

```bash
python3 ~/publish-benchmarks/scripts/manage_followups.py resume
```

Remove:

```bash
python3 ~/publish-benchmarks/scripts/manage_followups.py remove
```

Status:

```bash
python3 ~/publish-benchmarks/scripts/manage_followups.py status
```
