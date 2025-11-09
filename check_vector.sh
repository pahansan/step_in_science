#!/bin/bash

cd ~/code/nirs/riscv-compilers/llvm-project
grep -R "RegisterClass" -n llvm/lib/Target | grep -E "v[0-9]+i[0-9]+" > ~/code/nirs/step_in_science/vector.txt
