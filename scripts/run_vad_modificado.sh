#!/bin/bash

alpha0=${1:-5}

set -o pipefail

DIR_P2=$HOME/PAV/P2
filewav="$DIR_P2/audio.wav"

if [[ ! -f $filewav ]]; then
    echo "Wav file not found: $filewav" >&2
    exit 1
fi

filevad="${filewav/.wav/.vad}"
CMD="$DIR_P2/bin/vad --alpha1=$alpha0"

echo "**************** Procesando $filewav con alpha=$alpha0 ****************"
$CMD -i $filewav -o $filevad || exit 1

# Extraemos la línea que contiene el porcentaje total y la imprimimos junto al alpha
echo -ne "$alpha0\t"
scripts/vad_evaluation.pl "${filewav/.wav/.lab}" | grep '===>' | awk -F': ' '{print $2}'

exit 0
