from sys import platform
import subprocess as sp

if platform == 'win32':
    import winapps
    import winreg
import psutil as p
import pyspeedtest


class ComputerConfigMixin:

    def cpu_count(self) -> int:
        result = p.cpu_count()
        return result

    def cpu_max_speed(self) -> int:
        result = int(max(p.cpu_freq()[0:3]))
        return result

    def ram(self) -> float:
        result = float('{0:.2f}'.format(p.virtual_memory().total / 1024 ** 3))
        return result

    def programs(self) -> tuple:
        if platform == 'win32':
            chrome_version, \
            node_version, \
            vsc_version, \
            dot_net_version = 'НЕ НАЙДЕНО', 'НЕ НАЙДЕНО', 'НЕ НАЙДЕНО', self.dot_net()
            for app in winapps.list_installed():
                if 'Google Chrome' in app.name:
                    chrome_version = app.version
                if 'Node.js' in app.name:
                    node_version = app.version
                if 'Visual Studio Code' in app.name:
                    vsc_version = app.version
            result = {'chrome': chrome_version,
                      'node.js': node_version,
                      'vsc': vsc_version,
                      'dot_net': dot_net_version
                      }
        else:
            def get_apt() -> list:
                cmd = ['/usr/bin/dpkg', '-l']
                process = sp.Popen(cmd, stdout=sp.PIPE, stderr=sp.PIPE)
                stdout, stderr = process.communicate()
                return stdout.decode().replace('\t', ' ').split('\n')

            chrome_version, node_version, vsc_version = 'НЕ НАЙДЕНО', 'НЕ НАЙДЕНО', 'НЕ НАЙДЕНО'
            result = {'chrome': chrome_version,
                      'node.js': node_version,
                      'vsc': vsc_version,
                      }

            pkgs = get_apt()
            for pkg in pkgs:
                try:
                    if 'chrome' in pkg.split()[1]:
                        chrome_version = pkg.split()[2]
                        result['chrome'] = chrome_version
                    if 'nodejs' in pkg.split()[1]:
                        node_version = pkg.split()[2]
                        result['node.js'] = node_version
                    if 'code' in pkg.split()[1]:
                        vsc_version = pkg.split()[2]
                        result['vsc'] = vsc_version
                except:
                    continue

        flag = True
        not_find = []
        if platform == 'win32':
            if 'НЕ НАЙДЕНО' in (chrome_version, node_version, vsc_version, dot_net_version):
                flag = False
        else:
            if 'НЕ НАЙДЕНО' in (chrome_version, node_version, vsc_version):
                flag = False
        response = ''
        for key, value in result.items():
            response += f'{key} : {value}\n'
            if value == 'НЕ НАЙДЕНО':
                not_find.append(key)
        return response, flag, not_find

    def dot_net(self) -> str:
        dot_net_version = 'НЕ НАЙДЕНО'
        try:
            registry_key = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE, )
            access_key = winreg.OpenKey(registry_key, r"SOFTWARE\Microsoft\NET Framework Setup\NDP\v4\Full")
            dot_net_version = float(winreg.EnumValue(access_key, 6)[1][:3])
        except:
            pass
        return dot_net_version

    @staticmethod
    def get_network_speed() -> tuple:
        st = pyspeedtest.SpeedTest('google.ru')
        latency_list = [st.ping() for _ in range(5)]
        jitter = 0
        for i in range(0, 3):
            jitter += abs(latency_list[i] - latency_list[i + 1])
        jitter /= 5
        download1 = float('{:5.2f}'.format(st.download() / 1024 / 1024))
        download2 = float('{:5.2f}'.format(st.download() / 1024 / 1024))
        download3 = float('{:5.2f}'.format(st.download() / 1024 / 1024))
        download = format(((download1 + download2 + download3) / 3), '.2f')
        return download, round(jitter)

    def requirements(self) -> tuple:
        requirements = (3.8, 2000, 2,)
        names_conf = ('ram', 'max_cpu_speed', 'count_cpu_core',)
        names_dict_conf = {'ram': 'Объём оперативной памяти',
                           'max_cpu_speed': 'Частота процессора',
                           'count_cpu_core': 'Количество ядер процессора',
                           }
        func = (self.ram, self.cpu_max_speed, self.cpu_count,)

        result = ''
        flag = True
        for i in range(3):
            if func[i]() >= requirements[i]:
                result += f'{names_dict_conf[names_conf[i]]}:' \
                          f' Требуется {requirements[i]},' \
                          f' текущее значение {func[i]()}\n'
                continue
            flag = False
            result += f'{names_dict_conf[names_conf[i]]}:' \
                      f' Требуется {requirements[i]},' \
                      f' текущее значение {func[i]()}\n'
        return result, flag
