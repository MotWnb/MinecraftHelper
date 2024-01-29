import asyncio
import socket
import dns.resolver
import mcstatus

port_list = []


async def scan_port(ip, port, sem):
    port = port + 1
    for i in range(10):
        async with sem:  # 使用async with来申请一个Semaphore许可
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                await asyncio.wait_for(asyncio.get_event_loop().sock_connect(s, (ip, port)), timeout=5.0)  # 增加超时时间
                port_list.append(port)
                server = mcstatus.JavaServer.lookup(ip + ":" + str(port))
                status = server.status()
                server_name = " ".join(part['text'] for part in status.motd.raw['extra']).strip().replace(" ", "")
                print(ip + ":" + str(port))
                print(
                    f"这个服务器有 {status.players.online} 玩家在线，延时为 {status.latency} ms，服务器名称为:{server_name}，服务器版本为{status.version.name}")
                break
            except Exception as e:
                pass
            finally:
                s.close()


async def scan_ip(ip):
    max_concurrency = 1000  # 限制并发数量为100
    sem = asyncio.Semaphore(max_concurrency)  # 创建Semaphore
    tasks = [scan_port(ip, port, sem) for port in range(65534)]
    await asyncio.gather(*tasks)  # 等待所有任务完成
    port_list.sort()
    print(port_list)


async def get_ip(host_or_ip):
    srv_records = dns.resolver.resolve("_minecraft._tcp." + host_or_ip, 'SRV')
    for record in srv_records:
        host_or_ip = str(record.target).rstrip(".")
    host_or_ip = socket.gethostbyname(host_or_ip)
    await scan_ip(host_or_ip)


async def main(host):
    await asyncio.create_task(get_ip(host))

# asyncio.run(main())



