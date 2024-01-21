git pull origin main
pip3 install -r requirements.txt
python app.py &
APP_PID=$!
echo app is running successfully
kill $APP_PID