@echo off

cd ..

start "COMRADE: coh2-api" python -m api.api
start "COMRADE: BattleServer" python -m battleserver.server