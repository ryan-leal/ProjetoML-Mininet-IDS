from mininet.net import Mininet
from mininet.node import OVSBridge
from mininet.cli import CLI
from mininet.log import setLogLevel, info

def start_net():
    net = Mininet(controller=None,
                  switch=OVSBridge,
                  autoSetMacs=True,
                  autoStaticArp=True)

    h1 = net.addHost('h1', ip='10.0.0.1/24')  # servidor
    h2 = net.addHost('h2', ip='10.0.0.2/24')  # cliente legítimo
    h3 = net.addHost('h3', ip='10.0.0.3/24')  # atacante

    s1 = net.addSwitch('s1')

    net.addLink(h1, s1)
    net.addLink(h2, s1)
    net.addLink(h3, s1)

    net.start()

    info('*** Testando conectividade\n')
    net.pingAll()

    info('*** Iniciando servidor HTTP em h1:8080\n')
    h1.cmd('python3 -m http.server 8080 &')

    info('*** Rede pronta. h2=cliente, h3=atacante\n')
    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    start_net()
