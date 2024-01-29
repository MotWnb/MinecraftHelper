import dns.resolver


def srv_resolve(domain):
    # 查询SRV记录
    try:
        srv_records = dns.resolver.resolve("_minecraft._tcp." + domain, 'SRV')
        for record in srv_records:
            return "Priority:" + str(record.priority) + "\nWeight:" + str(record.weight) + "\nPort:" + str(
                record.port) + "\nTarget:" + str(record.target).rstrip(".")

    except dns.resolver.NoAnswer:
        print("No SRV records found for", domain)
        return False
    except dns.resolver.NXDOMAIN:
        print("Domain", domain, "does not exist")
        return False
