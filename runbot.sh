pip uninstall -y poetry
ps aux | grep python | grep -v "grep python" | awk '{print $2}' | xargs kill -9
pip install -r requirements.txt
python bot/run.py
while true
do
	sleep 1
done