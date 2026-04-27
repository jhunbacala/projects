# Ubuntu Desktop: 802.1X EAP-TLS Wi-Fi Certificate Authentication Setup

This guide walks you through generating a Certificate Signing Request (CSR), obtaining the signed certificate, and configuring your Wi-Fi on Ubuntu Desktop using **EAP-TLS**.

**Important**: Confirm the exact CSR subject requirements (especially Common Name / CN) with your network administrator before starting.

## Step 1: Generate Private Key and CSR

Open a terminal (`Ctrl + Alt + T`) and run:

```bash
mkdir ~/wifi-certs && cd ~/wifi-certs

# Generate 2048-bit key + CSR (no passphrase)
openssl req -new -newkey rsa:2048 -nodes -keyout client.key -out client.csr
```

Fill in the fields exactly as instructed by your admin.
Common Name (CN) is usually the most critical field (e.g., your username or username@domain).

Secure the private key:
```bash
chmod 600 client.key
```

You now have:

client.key — Private key (keep this secret!)
client.csr — Certificate Signing Request (send this to your CA)

## Step 2: Get the Signed Certificate

Send client.csr to your network/security team or upload it to your organization's CA portal.
Request the following back in PEM format:
Signed client certificate → save as client.crt (or client.pem)
CA / Root certificate → save as ca.crt (or ca.pem)


Place all files in ~/wifi-certs/.

## Step 3: Configure Wi-Fi (GUI Method – Recommended)

1. Click the Wi-Fi icon in the top bar → Wi-Fi Settings (or go to Settings → Wi-Fi).
2. Click the gear icon next to your corporate SSID.
3. Set:
Security: WPA & WPA2 Enterprise (or WPA3-Enterprise)
Authentication: TLS

4. Fill in:
Identity: Your username or as instructed (sometimes left blank or set to anonymous).
CA certificate: Select ca.crt
User certificate: Select client.crt
Private key: Select client.key
Private key password: Leave blank (if you used -nodes)

5. Click Apply and connect.

Alternative: Configure with nmcli (CLI)
Replace placeholders with your actual values:
```bash
nmcli connection add type wifi \
  con-name "YourCorpWiFi" \
  ifname wlan0 \                    # Check your interface with: nmcli device
  ssid "YOUR-SSID-NAME" \
  802-11-wireless-security.key-mgmt wpa-eap \
  802-1x.eap tls \
  802-1x.identity "your-username-or-cn" \
  802-1x.ca-cert "/home/$USER/wifi-certs/ca.crt" \
  802-1x.client-cert "/home/$USER/wifi-certs/client.crt" \
  802-1x.private-key "/home/$USER/wifi-certs/client.key" \
  802-1x.private-key-password ""

nmcli connection up "YourCorpWiFi"
```

Use absolute paths for the certificate files.
If You Received a PKCS#12 (.p12 / .pfx) Bundle Instead
You can use the single .p12 file directly in the GUI or with nmcli:
```bash
802-1x.client-cert "/path/to/client.p12"
802-1x.private-key "/path/to/client.p12"
802-1x.private-key-password "your-p12-password"
```
Troubleshooting

Connection fails — Verify the CN in your certificate matches what the RADIUS server expects:
```bash
openssl x509 -in client.crt -text -noout
```

Certificate format issues — Convert if needed:
```bash
openssl x509 -inform der -in cert.der -out cert.pem
```

Restart NetworkManager:
```bash 
sudo systemctl restart NetworkManager
```

Check logs while connecting:
```bash
journalctl -u NetworkManager -f
```

Tips

Keep your client.key secure (chmod 600).
Store all certificate files in a safe location.
If you encounter errors, share the exact message + your Ubuntu version (lsb_release -a).