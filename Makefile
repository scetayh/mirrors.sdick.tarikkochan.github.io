SOURCE_SITE_ROOT = docs/
SDICK_SITE_REPO_SOURCE = ../sdick.tarikkochan.github.io/source/

.PHONY: deploy clean copy git-commit git-push git

deploy:
	make clean
	make copy
	make git

clean:
	rm -rf ${SOURCE_SITE_ROOT}/*

copy:
	mkdir -p ${SOURCE_SITE_ROOT}/
	cp -R ${SDICK_SITE_REPO_SOURCE}/* ${SOURCE_SITE_ROOT}/

git-commit:
	git add .
	-git commit -a -m `date +%Y%m%dT%H%M%SZ`

git-push:
	git push --set-upstream origin main

git:
	make git-commit
	make git-push
