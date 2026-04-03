# Zero Trust Network & Microsegmentation Check

> Source: 제로트러스트 가이드라인 2.0 (KISA), NIST SP 800-207
> Checklist refs: Network/System elements, KISA ZT 8 elements

---

## 1. Network Segmentation Audit

```bash
# List all network interfaces and their zones
ip addr show
firewall-cmd --get-active-zones 2>/dev/null

# Check iptables/nftables rules for segmentation
iptables -L -n -v 2>/dev/null | head -40
nft list ruleset 2>/dev/null | head -40

# Check for default ACCEPT policies (should be DROP)
iptables -L -n 2>/dev/null | grep "policy ACCEPT" && echo "WARNING: Default ACCEPT policy found"
```

---

## 2. Microsegmentation Verification

```bash
# Check container network policies (Kubernetes)
kubectl get networkpolicies --all-namespaces 2>/dev/null

# Verify pod-to-pod communication restrictions
kubectl get pods -o wide --all-namespaces 2>/dev/null | head -20

# Check Docker network isolation
docker network ls 2>/dev/null
docker network inspect bridge 2>/dev/null | python3 -c "
import sys, json
data = json.load(sys.stdin)
for net in data:
    containers = net.get('Containers', {})
    if len(containers) > 1:
        print(f'WARNING: {len(containers)} containers on bridge network')
" 2>/dev/null
```

---

## 3. Encrypted Traffic Verification

```bash
# Check for unencrypted internal traffic
ss -tlnp | while read line; do
  port=$(echo "$line" | awk '{print $4}' | rev | cut -d: -f1 | rev)
  case $port in
    80|8080|21|23|25|110|143)
      echo "WARNING: Plaintext port $port is open"
      ;;
  esac
done

# Verify internal service TLS
for host in <SERVICE_1> <SERVICE_2>; do
  echo | openssl s_client -connect "$host":443 2>/dev/null | \
    grep -E "Protocol|Cipher" && echo "TLS OK: $host" || echo "FAIL: $host"
done
```

---

## 4. DNS Security Check

```bash
# Check DNS configuration
cat /etc/resolv.conf

# Verify DNS-over-HTTPS/TLS is configured
grep -rn "dns-over-tls\|dns-over-https\|DoT\|DoH" /etc/systemd/resolved.conf 2>/dev/null
resolvectl status 2>/dev/null | grep -i "dnssec\|dns over tls"

# Check for DNS leak (should use internal DNS only)
nslookup example.com 2>/dev/null | head -5
```

---

## 5. VPN & ZTNA Configuration Check

```bash
# Check VPN configuration
systemctl status openvpn 2>/dev/null || systemctl status wireguard 2>/dev/null

# Verify split tunneling is disabled
grep -n "redirect-gateway\|AllowedIPs = 0.0.0.0/0" \
  /etc/openvpn/*.conf /etc/wireguard/*.conf 2>/dev/null

# Check for ZTNA agent
systemctl status zscaler 2>/dev/null
systemctl status cloudflared 2>/dev/null
systemctl status netskope 2>/dev/null
```

---

## 6. Lateral Movement Prevention

```bash
# Check for unnecessary open ports between segments
ss -tlnp | awk '{print $4}' | sort -u

# Verify SSH is restricted to jump hosts
grep -n "AllowUsers\|AllowGroups\|Match" /etc/ssh/sshd_config

# Check for SMB/RDP exposure (common lateral movement vectors)
ss -tlnp | grep -E ":445|:3389|:135|:139" && \
  echo "WARNING: SMB/RDP ports exposed"

# Check for inter-VLAN routing restrictions
ip route show | grep -v default
```

---

## 7. Network Monitoring & Logging

```bash
# Check network flow logging
systemctl status auditd 2>/dev/null
grep -c "type=SOCKADDR" /var/log/audit/audit.log 2>/dev/null

# Verify syslog/SIEM forwarding
grep -rn "remote\|forward\|@" /etc/rsyslog.conf /etc/rsyslog.d/ 2>/dev/null
systemctl status filebeat 2>/dev/null || systemctl status fluentd 2>/dev/null

# Check for IDS/IPS
systemctl status suricata 2>/dev/null || systemctl status snort 2>/dev/null
```

---

## Verification Checklist

| Item | Check | Expected |
|------|-------|----------|
| Default policy | `iptables -L` | DROP (not ACCEPT) |
| Network policies | K8s NetworkPolicy | Applied per namespace |
| No plaintext ports | `ss -tlnp` | No 80/21/23/25 internally |
| Internal TLS | `openssl s_client` | TLS 1.2+ on all services |
| Split tunneling | VPN config | Disabled (full tunnel) |
| SSH restricted | `sshd_config` | AllowUsers/AllowGroups set |
| No SMB/RDP | Port check | 445/3389 not exposed |
| Log forwarding | Syslog/SIEM check | Active and configured |
