# Resource Management & Monitoring

> Source: 로봇 보안취약점 점검 체크리스트 해설서 (KISA)
> Checklist refs: RA-02, RA-03

---

## 1. cgroups - Security Agent Resource Limits (RA-02)

Restrict CPU and memory usage for security processes so they do not interfere with real-time robot control.

```bash
# cgroup 생성 (cpu + memory)
sudo cgcreate -g cpu,memory:/robot_security

# CPU 할당 제한 (20000us = 20% of 1 core at default 100000us period)
echo 20000 | sudo tee /sys/fs/cgroup/cpu/robot_security/cpu.cfs_quota_us

# 메모리 제한 (256MB)
echo 256M | sudo tee /sys/fs/cgroup/memory/robot_security/memory.limit_in_bytes

# 실행 중인 보안 에이전트를 cgroup에 할당
sudo cgclassify -g cpu,memory:/robot_security $(pidof security_agent)
```

---

## 2. OpenSSL Hardware Acceleration Check (RA-02)

Offload crypto operations to hardware to reduce CPU overhead.

```bash
openssl engine -t
# Expected output:
# (dynamic) Dynamic engine loading support
# (rdrand) Intel RDRAND engine
# (aesni)  Intel AES-NI engine
```

---

## 3. logrotate Configuration (RA-02)

Prevent audit/operational logs from exhausting disk space.

```bash
# /etc/logrotate.d/robot_security
/var/log/robot/security.log {
    size 50M
    rotate 5
    compress
    missingok
    notifempty
}
```

---

## 4. System Resource Monitoring (RA-03)

Dashboard or CLI-based monitoring of CPU, memory, disk, and network utilization. The robot system should provide a user interface for operators to view resource status in real-time.

Key resource metrics to monitor:
- CPU usage per core / per process
- Memory (RSS / swap) usage
- Disk I/O and capacity
- Network interface throughput and error rates

---

## 5. ROS Publisher Rate Limiting (RA-01 L2)

Limit sensor data publish rate to prevent communication overload.

```cpp
ros::Publisher pub = nh.advertise<std_msgs::String>("sensor_data", 10);
ros::Rate loop_rate(5);  // 초당 5회 전송 제한
while (ros::ok()) {
    std_msgs::String msg;
    msg.data = "sensor data";
    pub.publish(msg);
    loop_rate.sleep();
}
```

---

## 6. ROS2 QoS Security Profile (RA-01 L2)

```yaml
QoSProfile:
    reliability: RELIABLE
    durability: TRANSIENT_LOCAL
    history: KEEP_LAST
    depth: 10
```
