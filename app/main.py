from fastapi import FastAPI
from app.omada import Omada
import random, os

def generate_random_password() -> str:
    charset = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!$&()*+,-.<=>?@[]^_{|}~'
    return ''.join(random.SystemRandom().choice(charset) for _ in range(16))

def set_omada_psk(ssid: str, psk: str) -> None:
    omada = Omada('app/omada.cfg')
    omada.login()
    groups = omada.getWirelessGroups() or {}
    for group in groups.get('data',[]):
        site, group_id = group['site'], group['id']
        networks = omada.getWirelessNetworks(group=group_id) or {}
        existing = [item for item in networks.get('data',[]) if item['name'] == ssid]
        if not existing:
            continue
        current_settings = existing[0]
        current_settings['pskSetting']['securityKey'] = psk
        ssid_id = current_settings['id']
        omada.updateWirelessNetwork(group=group_id, ssid=ssid_id, site=site, data=current_settings)
    omada.logout()

def get_omada_psk(ssid: str) -> str:
    psk = ''
    omada = Omada('app/omada.cfg')
    omada.login()
    groups = omada.getWirelessGroups() or {}
    for group in groups.get('data',[]):
        site, group_id = group['site'], group['id']
        networks = omada.getWirelessNetworks(group=group_id) or {}
        existing = [item for item in networks.get('data',[]) if item['name'] == ssid]
        if existing:
            psk = existing[0]['pskSetting']['securityKey']
            break
    omada.logout()
    return psk

app = FastAPI()

@app.get('/todays-wifi/reset')
async def reset_wifi_psk():
    new_password = generate_random_password()
    ssid = os.environ['SSID']
    set_omada_psk(ssid=ssid, psk=new_password)
    ssid_qr = f'WIFI:T:WPA;S:{ssid};P:{new_password};;'
    return ssid_qr

@app.get('/todays-wifi')
async def get_wifi_psk():
    ssid = os.environ['SSID']
    password = get_omada_psk(ssid=ssid)
    ssid_qr = f'WIFI:T:WPA;S:{ssid};P:{password};;'
    return ssid_qr
