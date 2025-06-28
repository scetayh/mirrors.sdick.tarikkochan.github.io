SDICK_SITE_REPO_SOURCE = ../sdick.tarikkochan.github.io/source/

.PHONY: deploy clean copy git-commit git-push git

deploy:
	make clean
	make copy
	make git

clean:
	rm -rf source/*

copy:
	mkdir -p source/
	cp -R ${SDICK_SITE_REPO_SOURCE}/* source/

git-commit:
	git add .
	-git commit -a -m `date +%Y%m%dT%H%M%SZ`

git-push:
	git push --set-upstream origin main

git:
	make git-commit
	make git-push
