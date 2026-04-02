# Firewall & Network Hardening

> Source: 로봇 보안취약점 점검 체크리스트 해설서 (KISA)
> Checklist refs: DFR-02, RA-01, RA-08

---

## 1. Host Firewall (iptables)

### 1.1 MQTT / HTTPS Only (DFR-02 Protocol Filtering)

```bash
# MQTT 및 HTTPS 외의 포트 차단
sudo iptables -A INPUT -p tcp --dport 443 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 1883 -j ACCEPT
sudo iptables -A INPUT -j DROP
```

### 1.2 SSH + HTTPS Only (RA-01 DoS Prevention)

```bash
sudo iptables -A INPUT -p tcp --dport 22 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 443 -j ACCEPT
sudo iptables -A INPUT -j DROP
```

### 1.3 Unnecessary Port Blocking (RA-08 Service Restriction)

```bash
# 외부 포트 스캔 (TCP 포트 확인)
nmap -sS 192.168.0.10

# 불필요한 포트(예: FTP 21, Telnet 23, TFTP 69) 차단
sudo iptables -A INPUT -p tcp --dport 21 -j DROP
sudo iptables -A INPUT -p tcp --dport 23 -j DROP
sudo iptables -A INPUT -p udp --dport 69 -j DROP
```

---

## 2. Service Hardening (RA-08)

```bash
# 현재 활성화된 포트 및 프로세스 확인
sudo ss -tulnp
sudo netstat -tulnp

# 서비스 상태 확인 및 비활성화
sudo systemctl status telnet
sudo systemctl disable telnet
sudo systemctl stop telnet
```

---

## 3. VLAN Network Segmentation (RA-01 L2)

Control network and sensor network separation via VLAN.

```bash
# 제어 망 (VLAN ID 10)
sudo ip link add link eth0 name eth0.10 type vlan id 10
# 센서 망 (VLAN ID 20)
sudo ip link add link eth0 name eth0.20 type vlan id 20

sudo ip link set eth0.10 up
sudo ip link set eth0.20 up
```

---

## 4. sysctl Network Tuning (RA-01)

```bash
sudo sysctl -w net.core.somaxconn=128
sudo sysctl -w net.ipv4.tcp_max_syn_backlog=256
ulimit -n 1024
```

---

## 5. Nginx Rate Limiting (RA-01)

```nginx
# /etc/nginx/nginx.conf
http {
    limit_req_zone $binary_remote_addr zone=req_limit_per_ip:10m rate=10r/s;
    server {
        listen 443 ssl;
        server_name example.com;
        location / {
            limit_req zone=req_limit_per_ip burst=5 nodelay;
            limit_conn conn_limit_per_ip 10;
        }
    }
}
```

---

## 6. Suricata IDS Rule (RA-01 L2 DoS Detection)

```yaml
alert tcp any any -> $HOME_NET any (msg:"TCP SYN Flood"; flags:S; threshold: type both, track by_src,
count 50, seconds 1; classtype:attempted-dos; sid:100001;)
```
