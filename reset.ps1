git checkout --orphan latest_branch
git rm -rf --cached .
git add -A
git commit -m "reset"
git branch -D master
git branch -m master
git push -f -u origin master