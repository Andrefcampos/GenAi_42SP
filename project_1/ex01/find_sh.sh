#! /bin/zsh

find ./* -type f -name "*.sh" -exec bash -c 'for f; do basename "$f" .sh; done' _ {} +
