#!/bin/bash

# Usage: ./rend_no_poetry.sh -l|-m|-h class_name (without 'Example_', case-insensitive)
# Example: ./rend_no_poetry.sh -l code_block

set -e

if [ $# -ne 2 ]; then
    echo "Usage: $0 -l|-m|-h ClassName"
    exit 1
fi

case "$1" in
    -l)
        QUALITY="pql"
        OUTDIR="low_quality"
        RESDIR="480p15"
        ;;
    -m)
        QUALITY="pqm"
        OUTDIR="medium_quality"
        RESDIR="720p30"
        ;;
    -h)
        QUALITY="pqh"
        OUTDIR="high_quality"
        RESDIR="1080p60"
        ;;
    *)
        echo "Error: Quality must be -l (low), -m (medium), or -h (high)"
        exit 1
        ;;
esac

# Format class name: Example_ + name_snake_case
CLASS="Example_$(echo "$2" | tr '[:upper:]' '[:lower:]')"

if ! grep -q "class $CLASS(" examples.py; then
    echo "Error: Class '$CLASS' not found in examples.py"
    exit 1
fi

python -m manim -"${QUALITY}" examples.py "$CLASS"

OUTFILE="media/videos/examples/${RESDIR}/${CLASS}.mp4"
if [ ! -f "$OUTFILE" ]; then
    echo "Error: Output file '$OUTFILE' not found"
    exit 1
fi

mv "$OUTFILE" "video_output/${OUTDIR}/${ARG_LOWER}.mp4"
rm -rf media __pycache__

