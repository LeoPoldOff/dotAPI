This project is a simple flask API for internal department of the bank.
Operating procedure:    1)execute file start.sh
			2)open new command console
			3)enter one of four commands into the console
Commands:
	1)curl -i http://localhost:5000/api/ping
	2)curl -i http://localhost:5000/api/status/<client`s uuid4 number>
	3)curl -i http://localhost:5000/api/add/<client`s uuid4 number>/<sum>
	4)curl -i http://localhost:5000/api/substract/<client`s uuid4 number>/<sum>

File db_creation.py creates an example of sqlite database.

At the beginning and every 10 minutes after the programme refreshes client`s holds.
Feedback is implemented through JSON packets.

P.S.: The creator had not at hand completely linux system and the docker refuses to cooperate
with Windows Ubuntu. Sorry for this fault, creator`s blame.
