import serial

# 配置串口参数
port = 'COM1'  # 根据实际情况修改串口号
baudrate = 9600  # 波特率
bytesize = serial.EIGHTBITS  # 数据位
parity = serial.PARITY_NONE  # 校验位
stopbits = serial.STOPBITS_ONE  # 停止位



def connect(control_command):
    # 打开串口
    ser = serial.Serial(port, baudrate, bytesize, parity, stopbits, timeout=1)
    print(f"开始连接串口 {port}")
    # 检查串口是否打开
    if ser.is_open:
        print(f"串口 {port} 已打开")
        # 确保 control_command 是一个字符串
        control_command = str(control_command)
        # 发送控制指令
        # control_command = "MOVE_ARM 100 200 300\n"  # 示例控制指令，根据实际需求修改
        ser.write(control_command.encode('utf-8'))

        print(f"已发送指令: {control_command}")

        # 关闭串口
        ser.close()
        print(f"串口 {port} 已关闭")
    else:
        print(f"无法打开串口 {port}")
        # 关闭串口
        ser.close()


# 接收到反馈
def receive_feedback():
    # 打开串口
    ser = serial.Serial(port, baudrate, bytesize, parity, stopbits, timeout=1)
    # 监听串口，接收数据
    try:
        while True:
            if ser.in_waiting > 0:  # 检查是否有数据可读
                received_data = ser.readline().decode().strip()  # 读取数据
                print(f"接收到: {received_data}")
                return received_data
    except KeyboardInterrupt:
        print("结束监听")
    finally:
        ser.close()  # 关闭串口

