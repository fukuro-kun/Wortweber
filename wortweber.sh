#!/bin/bash
eval "$(conda shell.bash hook)"
conda activate wortweber
python -m src.wortweber
conda deactivate
