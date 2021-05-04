-- nuke DB

DROP TABLE IF EXISTS levelupapi_event;
DROP TABLE IF EXISTS levelupapi_eventgamer;
DROP TABLE IF EXISTS levelupapi_game;
DROP TABLE IF EXISTS levelupapi_gamer;
DROP TABLE IF EXISTS levelupapi_gametype;
DELETE FROM django_migrations WHERE app = 'levelupapi'


-- test

select * from levelupapi_event