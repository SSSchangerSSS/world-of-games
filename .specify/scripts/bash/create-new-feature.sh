#!/usr/bin/env bash
# ساخت پوشه فیچر جدید طبق الگوی spec-kit — استفاده: ./create-new-feature.sh "عنوان"
set -euo pipefail
TITLE="${1:?usage: create-new-feature.sh \"title\"}"
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
NUM=$(ls "$REPO_ROOT/specs" 2>/dev/null | grep -E '^[0-9]{3}-' | sort -n | tail -1 | cut -d- -f1)
NUM=$(printf "%03d" $(( ${NUM:-000} + 1 )))
SLUG=$(echo "$TITLE" | tr ' ' '-' | tr -cd 'a-z0-9-' | head -c 40)
DIR="$REPO_ROOT/specs/$NUM-$SLUG"
mkdir -p "$DIR"
cp "$REPO_ROOT/.specify/templates/spec-template.md"  "$DIR/spec.md"
cp "$REPO_ROOT/.specify/templates/plan-template.md"  "$DIR/plan.md"
cp "$REPO_ROOT/.specify/templates/tasks-template.md" "$DIR/tasks.md"
echo "created: specs/$NUM-$SLUG  → حالا Clarify و سپس تکمیل spec.md"
