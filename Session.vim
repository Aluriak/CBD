let SessionLoad = 1
if &cp | set nocp | endif
let s:so_save = &so | let s:siso_save = &siso | set so=0 siso=0
let v:this_session=expand("<sfile>:p")
silent only
exe "cd " . escape(expand("<sfile>:p:h"), ' ')
if expand('%') == '' && !&modified && line('$') <= 1 && getline(1) == ''
  let s:wipebuf = bufnr('%')
endif
set shortmess=aoO
badd +1 cbd/__main__.py
badd +1 cbd/database/database.py
badd +1 data/create_database.sql
badd +1 data/example_data_insertion.sql
badd +1 data/example_table_join.sql
badd +10 ~/test.py
badd +0 doc/report.tex
argglobal
silent! argdel *
argadd ~/Programmation/Cours/BIG_M1/CBD/cbd/__main__.py
set stal=2
edit cbd/__main__.py
set splitbelow splitright
wincmd _ | wincmd |
vsplit
1wincmd h
wincmd w
set nosplitbelow
set nosplitright
wincmd t
set winheight=1 winwidth=1
exe 'vert 1resize ' . ((&columns * 117 + 119) / 239)
exe 'vert 2resize ' . ((&columns * 121 + 119) / 239)
argglobal
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
silent! normal! zE
let s:l = 135 - ((13 * winheight(0) + 28) / 56)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
135
normal! 017|
lcd ~/Programmation/Cours/BIG_M1/CBD
wincmd w
argglobal
edit ~/Programmation/Cours/BIG_M1/CBD/cbd/database/database.py
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
silent! normal! zE
let s:l = 10 - ((9 * winheight(0) + 28) / 56)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
10
normal! 0
lcd ~/Programmation/Cours/BIG_M1/CBD
wincmd w
exe 'vert 1resize ' . ((&columns * 117 + 119) / 239)
exe 'vert 2resize ' . ((&columns * 121 + 119) / 239)
tabedit ~/Programmation/Cours/BIG_M1/CBD/data/example_data_insertion.sql
set splitbelow splitright
wincmd _ | wincmd |
vsplit
1wincmd h
wincmd w
wincmd _ | wincmd |
split
1wincmd k
wincmd w
set nosplitbelow
set nosplitright
wincmd t
set winheight=1 winwidth=1
exe 'vert 1resize ' . ((&columns * 120 + 119) / 239)
exe '2resize ' . ((&lines * 28 + 29) / 59)
exe 'vert 2resize ' . ((&columns * 118 + 119) / 239)
exe '3resize ' . ((&lines * 27 + 29) / 59)
exe 'vert 3resize ' . ((&columns * 118 + 119) / 239)
argglobal
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
silent! normal! zE
let s:l = 7 - ((6 * winheight(0) + 28) / 56)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
7
normal! 0
lcd ~/Programmation/Cours/BIG_M1/CBD
wincmd w
argglobal
edit ~/Programmation/Cours/BIG_M1/CBD/data/example_table_join.sql
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
silent! normal! zE
let s:l = 5 - ((4 * winheight(0) + 14) / 28)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
5
normal! 022|
lcd ~/Programmation/Cours/BIG_M1/CBD
wincmd w
argglobal
edit ~/Programmation/Cours/BIG_M1/CBD/data/create_database.sql
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
silent! normal! zE
let s:l = 34 - ((26 * winheight(0) + 13) / 27)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
34
normal! 0
lcd ~/Programmation/Cours/BIG_M1/CBD
wincmd w
exe 'vert 1resize ' . ((&columns * 120 + 119) / 239)
exe '2resize ' . ((&lines * 28 + 29) / 59)
exe 'vert 2resize ' . ((&columns * 118 + 119) / 239)
exe '3resize ' . ((&lines * 27 + 29) / 59)
exe 'vert 3resize ' . ((&columns * 118 + 119) / 239)
tabedit ~/Programmation/Cours/BIG_M1/CBD/doc/report.tex
set splitbelow splitright
set nosplitbelow
set nosplitright
wincmd t
set winheight=1 winwidth=1
argglobal
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
silent! normal! zE
let s:l = 1 - ((0 * winheight(0) + 28) / 56)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1
normal! 0
lcd ~/Programmation/Cours/BIG_M1/CBD
tabnext 3
set stal=1
if exists('s:wipebuf')
  silent exe 'bwipe ' . s:wipebuf
endif
unlet! s:wipebuf
set winheight=1 winwidth=20 shortmess=filnxtToO
let s:sx = expand("<sfile>:p:r")."x.vim"
if file_readable(s:sx)
  exe "source " . fnameescape(s:sx)
endif
let &so = s:so_save | let &siso = s:siso_save
doautoall SessionLoadPost
unlet SessionLoad
" vim: set ft=vim :
