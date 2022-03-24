# rhul-attendance
This project was made for signing into online classes automatically at Royal Holloway University. This program will automatically fetch your timetable and will mark your attendance.

## Setup
This has only been tested on an Ubuntu server.

### Prerequisites
- python 3
- selenium
- linux server (optional)

### Install
```shell
cd ~
git clone https://github.com/member87/rhul-attendance/

crontab -e
# replace <username> with your username
0 0 * * 1-5 cd /home/<username>/rhul-attendance/ &&  /usr/bin/python3 timetable.py
10 9-18 * * 1-5 cd /home/<username>/rhul-attendance/ && /usr/bin/python3 attendance.py
```

You will also need to edit the file "CONFIG.py" and fill in both your username and password
