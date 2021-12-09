#!/bin/bash
# 在仓库的根目录下运行命令
git add . -u
git commit -m "Saving files before refreshing line endings"
git rm --cached -r .
git reset --hard
git add .
git commit -m "Normalize all the line endings"
git push

