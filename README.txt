============
Demo Accounts
============

Manager:
	Username: cmsmanager

Key Decision Maker:
	Username: cmskdm:

Operator:
	Username: cmsoperator

ALL PASSWORDS: cmsdemo


============
Installation/Running
============

Highly Recommended: 
	Use our deployed server.
	Frontend: http://cms.h5.io/
	Backend: http://cms.h5.io:8000/

Self Install [Not Recommended]:
	Clone the TBC-CMS and TBC-CMS-Front git repositories from the following links:
		Backend: https://github.com/Xia-Minghong/TBC-CMS
		Frontend: https://github.com/Xia-Minghong/TBC-CMS-Front
	In TBC-CMS-Front, run commands: (require npm, bower, karma, grunt-cli)
		npm install
		bower install
	To run the frontend server: (you can edit Gruntfile.json to change port)
		grunt serve
	To run the backend server (require redis, djangorestframewor and multiple other dependencies, you may have to use pip to install what you are lacking based on the error messages
		python2 runserver 0.0.0.0:8000 (current frontend points to cms.h5.io:8000, you can change in TBC-CMS-Front/scripts/app.coffee, and recompile the coffeescripts with "grunt build")

Is you have any issue in deploying the server, please contact:
	Name: Xia Minghong
	Email: mxia001@e.ntu.edu.sg
	WhatsApp: +65 85445660

==========
DB Import
==========

After the django server is up and running, run the following commands to import database:
python2 manage.py loaddata *.json

replace * with any of the json file in TBC-CMS
Warning***: you might run into integrity issue. Therefore, it is highly recommended that you use our deployed server
