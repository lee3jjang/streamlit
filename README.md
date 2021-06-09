# 배포하는 법(GCP)
* gcp에 접속해서 console로 들어온다
* git clone 으로 소스를 새로 만들거나, git pull로 땡겨온다.
* 폴더에 들어 가서 gcloud app deploy
  - Dockerfile이랑, app.yaml 필요

# 배포하는 법(Heroku)
* 콘솔에서 heroku login
* heroku create ins-comp-dashboard(appname) (app 생성)
* git push heroku master (heroku remote로 push)