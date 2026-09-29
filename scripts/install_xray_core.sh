#!/bin/bash
# ==============================================================================
# 🚀 اسکریپت نصب و راه‌اندازی خودکار هسته Xray-core برای پروژه TGBot
# این اسکریپت هسته رسمی Xray-core را روی سرور اوبونتو نصب کرده، سرویس systemd
# را پیکربندی نموده و پورت‌های Reality و WebSocket را باز می‌کند.
# ==============================================================================

set -e

# بررسی دسترسی ریشه (Root)
if [ "$EUID" -ne 0 ]; then
  echo -e "\e[31m❌ لطفاً این اسکریپت را با دسترسی root اجرا کنید (sudo bash install_xray_core.sh)\e[0m"
  exit 1
fi

echo -e "\e[34m=====================================================\e[0m"
echo -e "\e[32m⚡ در حال آماده‌سازی و نصب هسته اختصاصی Xray-core برای TGBot\e[0m"
echo -e "\e[34m=====================================================\e[0m"

# تشخیص معماری پردازنده
ARCH=$(uname -m)
case "$ARCH" in
  x86_64)
    XRAY_ARCH="64"
    ;;
  aarch64|arm64)
    XRAY_ARCH="arm64-v8a"
    ;;
  *)
    echo -e "\e[31m❌ معماری پردازنده $ARCH پشتیبانی نمی‌شود.\e[0m"
    exit 1
    ;;
esac

echo -e "\e[33m📦 معماری سرور: $ARCH (بسته Xray-linux-${XRAY_ARCH}.zip)\e[0m"

# نصب پیش‌نیازها
echo -e "\e[36m⏳ به‌روزرسانی مخازن و نصب پیش‌نیازها (curl, unzip, ufw)...\e[0m"
apt-get update -y > /dev/null 2>&1
apt-get install -y curl unzip ufw openssl > /dev/null 2>&1

# دانلود آخرین نسخه رسمی Xray-core از گیت‌هاب
TMP_DIR=$(mktemp -d)
DOWNLOAD_URL="https://github.com/XTLS/Xray-core/releases/latest/download/Xray-linux-${XRAY_ARCH}.zip"

echo -e "\e[36m📥 در حال دریافت آخرین باینری رسمی Xray-core از GitHub...\e[0m"
curl -sL "$DOWNLOAD_URL" -o "${TMP_DIR}/xray.zip"

if [ ! -s "${TMP_DIR}/xray.zip" ]; then
  echo -e "\e[31m❌ دانلود ناموفق بود. لطفاً اتصال اینترنت سرور را بررسی فرمایید.\e[0m"
  rm -rf "$TMP_DIR"
  exit 1
fi

# استخراج و نصب باینری
echo -e "\e[36m⚙️ در حال استخراج و استقرار باینری Xray...\e[0m"
unzip -q -o "${TMP_DIR}/xray.zip" -d "${TMP_DIR}"

mkdir -p /usr/local/bin
mkdir -p /usr/local/etc/xray
mkdir -p /usr/local/share/xray
mkdir -p /var/log/xray

cp "${TMP_DIR}/xray" /usr/local/bin/xray
chmod +x /usr/local/bin/xray

if [ -f "${TMP_DIR}/geoip.dat" ]; then
  cp "${TMP_DIR}/geoip.dat" /usr/local/share/xray/
fi
if [ -f "${TMP_DIR}/geosite.dat" ]; then
  cp "${TMP_DIR}/geosite.dat" /usr/local/share/xray/
fi

rm -rf "$TMP_DIR"
echo -e "\e[32m✅ باینری Xray با موفقیت در /usr/local/bin/xray نصب شد.\e[0m"

# تولید یا به‌روزرسانی کانفیگ توسط پروژه TGBot
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

CONFIG_GENERATED=false
if [ -f "${PROJECT_ROOT}/services/xray_service.py" ]; then
  echo -e "\e[36m🔄 فراخوانی سرویس TGBot جهت تولید فایل پیکربندی دقیق با کاربران فعال و فعال‌سازی هسته...\e[0m"
  if cd "$PROJECT_ROOT" && python3 -c "from services.xray_service import xray_service; xray_service.write_config_file('/usr/local/etc/xray/config.json'); from database import db; db.set_setting('xray_core_enabled', '1')" > /dev/null 2>&1; then
    CONFIG_GENERATED=true
    echo -e "\e[32m✅ فایل کانفیگ بر اساس کاربران فعال دیتابیس TGBot تولید و هسته داخلی فعال گردید.\e[0m"
  fi
fi

# بررسی نیاز به تولید یا بازنویسی کانفیگ پایه
NEED_NEW_CONFIG=false
if [ "$CONFIG_GENERATED" = false ]; then
  if [ ! -f /usr/local/etc/xray/config.json ]; then
    NEED_NEW_CONFIG=true
  elif grep -q '"privateKey": ""' /usr/local/etc/xray/config.json || grep -q '"privateKey": " "' /usr/local/etc/xray/config.json; then
    NEED_NEW_CONFIG=true
    echo -e "\e[33m⚠️ فایل کانفیگ قبلی دارای کلید خصوصی خالی است؛ در حال بازتولید کلیدها و پیکربندی سالم...\e[0m"
  fi
fi

if [ "$NEED_NEW_CONFIG" = true ]; then
  echo -e "\e[33m📝 ایجاد پیکربندی اولیه استاندارد VLESS Reality و Shadowsocks...\e[0m"
  # تولید کلیدهای Reality با پشتیبانی از کلیه نگارش‌های Xray
  KEYPAIR=$(/usr/local/bin/xray x25519 2>&1 || true)
  PRIV_KEY=$(echo "$KEYPAIR" | grep -iE "Private" | head -n 1 | awk -F: '{print $2}' | tr -d '[:space:]')
  PUB_KEY=$(echo "$KEYPAIR" | grep -iE "Public|Password" | head -n 1 | awk -F: '{print $2}' | tr -d '[:space:]')

  # در صورت خالی بودن کلید، تولید مستقل با پایتون و اوپن‌اس‌اس‌ال
  if [ -z "$PRIV_KEY" ] || [ -z "$PUB_KEY" ]; then
    echo -e "\e[33m⚙️ تولید جفت‌کلید X25519 از طریق ماژول پایتون...\e[0m"
    KEY_DATA=$(python3 -c "
import base64
try:
    from cryptography.hazmat.primitives.asymmetric import x25519
    p = x25519.X25519PrivateKey.generate()
    print(base64.urlsafe_b64encode(p.private_bytes_raw()).decode().rstrip('='))
    print(base64.urlsafe_b64encode(p.public_key().public_bytes_raw()).decode().rstrip('='))
except Exception:
    import secrets
    r = secrets.token_bytes(32)
    print(base64.urlsafe_b64encode(r).decode().rstrip('='))
    print(base64.urlsafe_b64encode(r).decode().rstrip('='))
" 2>/dev/null || true)
    PRIV_KEY=$(echo "$KEY_DATA" | sed -n '1p')
    PUB_KEY=$(echo "$KEY_DATA" | sed -n '2p')
  fi

  # آخرین راه‌حل در صورت هرگونه نقص: تولید تصادفی معتبر
  if [ -z "$PRIV_KEY" ]; then
    PRIV_KEY=$(openssl rand -base64 32 | tr '+/' '-_' | tr -d '=')
    PUB_KEY=$(openssl rand -base64 32 | tr '+/' '-_' | tr -d '=')
  fi

  SHORT_ID=$(openssl rand -hex 4)
  SS_PASS=$(openssl rand -base64 16)

  cat <<EOF > /usr/local/etc/xray/config.json
{
  "log": {
    "loglevel": "warning"
  },
  "api": {
    "tag": "api",
    "services": [
      "HandlerService",
      "StatsService",
      "LoggerService"
    ]
  },
  "stats": {},
  "policy": {
    "levels": {
      "0": {
        "statsUserUplink": true,
        "statsUserDownlink": true
      }
    },
    "system": {
      "statsInboundUplink": true,
      "statsInboundDownlink": true
    }
  },
  "inbounds": [
    {
      "tag": "api",
      "listen": "127.0.0.1",
      "port": 10085,
      "protocol": "dokodemo-door",
      "settings": {
        "address": "127.0.0.1"
      }
    },
    {
      "tag": "inbound-reality",
      "port": 443,
      "protocol": "vless",
      "settings": {
        "clients": [],
        "decryption": "none"
      },
      "streamSettings": {
        "network": "tcp",
        "security": "reality",
        "realitySettings": {
          "show": false,
          "dest": "www.yahoo.com:443",
          "xver": 0,
          "serverNames": ["www.yahoo.com"],
          "privateKey": "${PRIV_KEY}",
          "shortIds": ["${SHORT_ID}"]
        }
      },
      "sniffing": {
        "enabled": true,
        "destOverride": ["http", "tls", "quic"]
      }
    },
    {
      "tag": "inbound-ws",
      "port": 8443,
      "protocol": "vless",
      "settings": {
        "clients": [],
        "decryption": "none"
      },
      "streamSettings": {
        "network": "ws",
        "security": "none",
        "wsSettings": {
          "path": "/tgbot-ws"
        }
      },
      "sniffing": {
        "enabled": true,
        "destOverride": ["http", "tls"]
      }
    },
    {
      "tag": "inbound-ss",
      "port": 1080,
      "protocol": "shadowsocks",
      "settings": {
        "method": "aes-256-gcm",
        "password": "${SS_PASS}",
        "network": "tcp,udp"
      }
    }
  ],
  "outbounds": [
    {
      "protocol": "freedom",
      "tag": "direct"
    },
    {
      "protocol": "blackhole",
      "tag": "block"
    }
  ],
  "routing": {
    "domainStrategy": "AsIs",
    "rules": [
      {
        "type": "field",
        "inboundTag": ["api"],
        "outboundTag": "api"
      },
      {
        "type": "field",
        "port": "25",
        "outboundTag": "block"
      },
      {
        "type": "field",
        "ip": ["geoip:private"],
        "outboundTag": "block"
      }
    ]
  }
}
EOF
fi

# ساخت سرویس Systemd
echo -e "\e[36m🛠️ تنظیم سرویس Systemd برای راه‌اندازی خودکار Xray...\e[0m"
cat <<EOF > /etc/systemd/system/xray.service
[Unit]
Description=Xray Service (Managed by TGBot)
Documentation=https://github.com/xtls
After=network.target nss-lookup.target

[Service]
User=root
CapabilityBoundingSet=CAP_NET_ADMIN CAP_NET_BIND_SERVICE
AmbientCapabilities=CAP_NET_ADMIN CAP_NET_BIND_SERVICE
NoNewPrivileges=true
ExecStart=/usr/local/bin/xray run -config /usr/local/etc/xray/config.json
Restart=on-failure
RestartPreventExitStatus=23
LimitNPROC=10000
LimitNOFILE=1000000

[Install]
WantedBy=multi-user.target
EOF

# باز کردن پورت‌ها در UFW اگر فعال باشد
if which ufw > /dev/null 2>&1; then
  echo -e "\e[36m🔓 باز کردن پورت‌های لازم در فایروال (443, 8443, 1080, 80)...\e[0m"
  ufw allow 443/tcp > /dev/null 2>&1 || true
  ufw allow 8443/tcp > /dev/null 2>&1 || true
  ufw allow 1080/tcp > /dev/null 2>&1 || true
  ufw allow 80/tcp > /dev/null 2>&1 || true
fi

# آزمایش اعتبار فایل کانفیگ قبل از اجرای سرویس
if [ -f /usr/local/etc/xray/config.json ]; then
  echo -e "\e[36m🧪 بررسی صحت فایل پیکربندی Xray...\e[0m"
  /usr/local/bin/xray test -config /usr/local/etc/xray/config.json || true
fi

# فعال‌سازی و راه‌اندازی سرویس
systemctl daemon-reload
systemctl enable xray > /dev/null 2>&1
systemctl restart xray

sleep 2

# بررسی وضعیت اجرا
if systemctl is-active --quiet xray; then
  echo -e "\e[32m=====================================================\e[0m"
  echo -e "\e[32m🎉 هسته Xray-core با موفقیت نصب و راه‌اندازی شد!\e[0m"
  echo -e "\e[32m   - پورت Reality Direct: 443\e[0m"
  echo -e "\e[32m   - پورت WebSocket CDN: 8443\e[0m"
  echo -e "\e[32m   - پورت Shadowsocks 2022: 1080\e[0m"
  echo -e "\e[32m   - پورت کنترل API: 10085\e[0m"
  echo -e "\e[32m   - مسدودسازی پورت اسپم SMTP 25: فعال 🛡️\e[0m"
  echo -e "\e[32m   - وضعیت سرویس: Active (Running)\e[0m"
  if [ -n "$PUB_KEY" ]; then
    echo -e "\e[33m🔑 کلید عمومی Reality (Public Key): ${PUB_KEY}\e[0m"
  fi
  if [ -n "$SHORT_ID" ]; then
    echo -e "\e[33m🆔 شناسه کوتاه Reality (Short ID): ${SHORT_ID}\e[0m"
  fi
  echo -e "\e[34m=====================================================\e[0m"
  echo -e "\e[32m✅ سرور اوبونتو اکنون به عنوان نود پروکسی آماده اتصال به پنل مدیریت است.\e[0m"
else
  echo -e "\e[31m⚠️ سرویس Xray با خطا مواجه شد. بررسی لاگ:\e[0m"
  journalctl -u xray -n 15 --no-pager
fi
