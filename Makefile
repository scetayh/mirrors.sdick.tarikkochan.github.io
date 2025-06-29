export ROOT = docs/
export SDICK_REPO_SOURCES = /Users/scetayh/repo/sdick.tarikkochan.github.io/source/
CNAME = mirrors.sdick.tarikkochan.top
export GIT_REPO = git@github.com:scetayh/mirrors.sdick.tarikkochan.github.io.git
SERVER_PORT = 20943

.PHONY: all clean cname_write sdick_sources cname_write index_clean index_generate serve git

all:
	make index_clean
	make sdick_sources
	make cname_write
	make index_generate

clean:
	@echo "it is dangerous to run \`make clean'"
	@echo "this will remove all the files in \`${ROOT}'"
	@echo "press ENTER to continue, or CTRL-C to pause"
	@read
	rm -rf ${ROOT}/*
	mkdir -p ${ROOT}

sdick_sources:
	make -f Makefile.sdick_sources clean
	make -f Makefile.sdick_sources cp
	make -f Makefile.sdick_sources data_rename
	make -f Makefile.sdick_sources posts_rename

cname_write:
	echo ${CNAME} > ${ROOT}/CNAME

index_clean:
	gfind -type f -name "index.html" -exec rm -f {} \;

index_generate:
	python3 generate_index.py

serve:
	python3 -m http.server ${SERVER_PORT} --directory docs

git:
	make -f Makefile.git add
	make -f Makefile.git commit
	make -f Makefile.git remote_origin_remove
	make -f Makefile.git remote_origin_add
	make -f Makefile.git push
