#!/bin/zsh
set -e
film_dir="${0:A:h}/OpenFilm工程"
node '/Applications/OpenFilm.app/Contents/Resources/app.asar.unpacked/node_modules/openfilm/bin/openfilm.mjs' open "$film_dir"
