# miracle_asic

1. Создать пользователя
2. Установить питон
3. Установить virtualenvwrapper под питон3
	sudo pip3 install virtualenvwrapper
	export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3
	source /usr/local/bin/virtualenvwrapper.sh
4. git clone miracle_asic
5. pip3 install -r requirements.txt
6. установить nodejs
	sudo apt remove --purge nodejs npm
	sudo apt clean
	sudo apt autoclean
	sudo apt install -f
	sudo apt autoremove
	sudo apt install curl
	curl -sL https://deb.nodesource.com/setup_10.x | sudo -E bash -
	sudo apt-get install -y nodejs
	curl -sL https://dl.yarnpkg.com/debian/pubkey.gpg | sudo apt-key add -
	sudo apt-get update && sudo apt-get install yarn

7. установить nginx
8. Установить supervisor
8. cp deploy/supervisord.conf /etc/supervisor/conf.d/miracle_asic.conf
	supervisorctl reread
	supervisorctl update
9. cp deploy/miracle_asic.conf /etc/nginx/conf.d/
10. cp deploy/flower.conf /etc/nginx/conf.d/
11. Установить rabbitmq и redis-tools для админского интерфейса
	sudo apt install rabbitmq-server
	sudo rabbitmq-plugins enable rabbitmq_management
	localhost:15672
	rabbitmqctl add_user <username> <password>
	rabbitmqctl set_user_tags <username> administrator
	rabbitmqctl set_permissions -p / <username> ".*" ".*" ".*"

12. Установить postgres, создать пользователя и БД
13. python manage.py migrate
14. npm install
15. uwsgi поправить настройки на корректные (пользователь, пути до скриптов и тд)
16. python manage.py collectstatic
17. Поиск асиков через nmap (некорректный)
18. Указать верную информацию в frontend/src/api/serverUrl.js и src/store/modules/auth.js
19. Изменить assetsPublicPath на http://<hostname> в frontend/config/index.js
20. Изменить host на 0.0.0.0 в frontend/config/index.js
19. Скопировать БД
20. Указать в local_Settings верные настройки