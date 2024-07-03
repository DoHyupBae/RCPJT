from Raspi_MotorHAT import Raspi_MotorHAT, Raspi_DCMotor
from Raspi_PWM_Servo_Driver import PWM
import mysql.connector
from threading import Timer, Lock
from time import sleep
import signal
import sys
from sense_hat import SenseHat
from time import sleep
import datetime
import smbus
import math
from gpiozero import DistanceSensor
from gpiozero.pins.pigpio import PiGPIOFactory
import socket

HOST = '0.0.0.0'
PORT = 8080
# 서버 소켓 생성
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(2)  # 클라이언트 연결 대기

print("서버가 시작되었습니다.")

# 클라이언트 연결 수락
client_socket, client_address = server_socket.accept()
print(f"클라이언트 {client_address}가 연결되었습니다.")
client_socket.settimeout(1.0)  # 수신 타임아웃 설정


def closeDB(signal, frame):
    print("BYE")
    mh.getMotor(2).run(Raspi_MotorHAT.RELEASE)
    cur.close()
    db.close()
    timer.cancel()
    timer2.cancel()
    sys.exit(0)


def polling():
    global cur, db, ready

    lock.acquire()
    cur.execute("select * from command order by time desc limit 1")
    for (id, time, cmd_string, arg_string, is_finish) in cur:
        if is_finish == 1: break
        ready = (cmd_string, arg_string)
        cur.execute("update command set is_finish=1 where is_finish=0")

    db.commit()
    lock.release()

    global timer
    timer = Timer(0.1, polling)
    timer.start()


def sensing():
    global cur, db, sense, bus

    time = datetime.datetime.now()
    accel_data = bus.read_i2c_block_data(mpu, mpu_reg_accel_xout_h, 6)
    accel_x_raw = accel_data[0] << 8 | accel_data[1]
    accel_y_raw = accel_data[2] << 8 | accel_data[3]
    accel_z_raw = accel_data[4] << 8 | accel_data[5]
    if accel_x_raw > 32767:
        accel_x_raw -= 65536
    if accel_y_raw > 32767:
        accel_y_raw -= 65536
    if accel_z_raw > 32767:
        accel_z_raw -= 65536

    # 가속도 값 해석
    accel_x = accel_x_raw / g_const
    accel_y = accel_y_raw / g_const
    accel_z = accel_z_raw / g_const

    # 기울기 계산
    pitch_value = math.atan2(accel_x, math.sqrt(accel_y ** 2 + accel_z ** 2)) * 180.0 / math.pi
    roll_value = math.atan2(accel_y, math.sqrt(accel_x ** 2 + accel_z ** 2)) * 180.0 / math.pi

    meta_string = '0|0|0'
    is_finish = 0

    isAccident = 0
    # 기울기 출력
    print("Pitch: {:.2f} degrees, Roll: {:.2f} degrees".format(pitch_value, roll_value))

    # 초음파 센서로 거리 측정
    US_range_value = usensor.distance * 100
    print("{:.2f} cm".format(US_range_value))
    # 조건 확인 및 flag 설정(사고 발생)
    if roll_value >= 30 or roll_value < -30:
        isAccident = 1
        print("전복 사고 주의!")
        stop()
        client_socket.sendall('accident'.encode())
        print("주변 차량에 추돌 사고 메시지를 전송하였습니다")

    if US_range_value <= 15 and US_range_value >= 2:
        isAccident = 2
        print("추돌 사고 주의!")
        stop()
        client_socket.sendall('accident'.encode())
        print("주변 차량에 사고 메시지를 전송하였습니다")

    try:
        data = client_socket.recv(1024)
        message = data.decode()

        if message == 'accident':
            print("사고가 발생하여 차를 정지합니다")
            print("stop")
            stop()
    except socket.timeout:
        pass

    # 1초 대기

    query = "insert into sensing(time, pitch_value, roll_value, US_range_value, meta_string, is_finish, isAccident) values (%s, %s, %s, %s, %s, %s, %s)"
    value = (time, pitch_value, roll_value, US_range_value, meta_string, is_finish, isAccident)

    lock.acquire()
    cur.execute(query, value)
    db.commit()
    lock.release()

    global timer2
    timer2 = Timer(1, sensing)
    timer2.start()


def go():
    myMotor.setSpeed(400)
    myMotor.run(Raspi_MotorHAT.BACKWARD)


def back():
    myMotor.setSpeed(200)
    myMotor.run(Raspi_MotorHAT.FORWARD)


def stop():
    myMotor.setSpeed(200)
    myMotor.run(Raspi_MotorHAT.RELEASE)


def left():
    pwm.setPWM(0, 0, 250)


def mid():
    pwm.setPWM(0, 0, 370)


def right():
    pwm.setPWM(0, 0, 450)


# init
db = mysql.connector.connect(host='43.201.27.44', user='kanghyorin', password='1234', database='minDB',
                             auth_plugin='mysql_native_password')
cur = db.cursor()
ready = None
timer = None

mh = Raspi_MotorHAT(addr=0x6f)
myMotor = mh.getMotor(2)
pwm = PWM(0x6F)
pwm.setPWMFreq(60)

mpu = 0x68
# mpu register's addr
mpu_reg_pwr_mgmt_1 = 0x6b
mpu_reg_accel_xout_h = 0x3b

g_const = 16384.0

bus = smbus.SMBus(1)
# below are for initiating mpu, us sensor
bus.write_byte_data(mpu, mpu_reg_pwr_mgmt_1, 0)

usensor = DistanceSensor(echo=15, trigger=14)

timer2 = None
lock = Lock()

signal.signal(signal.SIGINT, closeDB)
polling()
sensing()

# main thread
while True:
    sleep(0.1)
    if ready == None: continue

    cmd, arg = ready
    ready = None

    if cmd == "go": go()
    if cmd == "back": back()
    if cmd == "stop": stop()
    if cmd == "left": left()
    if cmd == "mid": mid()
    if cmd == "right": right()

