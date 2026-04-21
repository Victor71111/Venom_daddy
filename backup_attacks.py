ATTACKS = {
    "UDP_FLOOD": "Basic UDP packet flood",
    "HTTP_FLOOD": "HTTP GET/POST requests",
    "SLOWLORIS": "Slowloris attack",
    "SYN_FLOOD": "TCP SYN flood",
    "ICMP_FLOOD": "ICMP ping flood"
}

def get_attack(name):
    return ATTACKS.get(name, "UDP_FLOOD")
