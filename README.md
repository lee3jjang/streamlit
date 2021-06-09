# 배포하는 법(GCP)
* gcp에 접속해서 console로 들어온다
* `git clone` 으로 소스를 새로 만들거나, `git pull`로 땡겨온다.
* 폴더에 들어 가서 gcloud app deploy`
  - Dockerfile이랑, app.yaml 필요

# 배포하는 법(Heroku)
* (로그인(console에서)) `heroku login`
* (app 생성) `heroku create ins-comp-dashboard(appname)`
* (heroku remote로 push) `git push heroku master`

## 참고사항
* (heroku remote repository의 url 확인) `git remote get-url heroku`
* (heroku remote repository의 url 변경) `git remote set-url heroku https://git.heroku.com/ins-comp-dashboard.git(url)`
* heroku 배포하다 오류났었는데 `heroku buildpacks:clear`랑 `heroku ps:scale web=1` 명령어로 해결함