#!/usr/bin/env python2.7
# Copyright

import ipaddr

def render(self, **kwargs):
    policy = self.data
    config_blob = []

    layer_map = {"l3": "hosts",
                 "l4": "ports"
                 }

    def embed_includes(ast_element, direction, layer):
        if "include" in ast_element[direction][layer]:
            include_file = open("etc/objects/" +
                                ast_element[direction][layer]["include"]
                                + "." + layer_map[layer])
            elements = []
            for line in include_file.readlines():
                elements.append(line.strip())
            return elements
        elif "ip" in ast_element[direction][layer]:
            return [ast_element[direction][layer]["ip"]]
        elif "ports" in ast_element[direction][layer]:
            return ast_element[direction][layer]["ports"]

    for rule in policy:
        rule = rule[0]
        # FIXME
        #   - remove hardcoded paths
        s_hosts = embed_includes(rule, "source", "l3")
        s_ports = embed_includes(rule, "source", "l4")
        d_hosts = embed_includes(rule, "destination", "l3")
        d_ports = embed_includes(rule, "destination", "l4")

        for s_port in s_ports:
            for d_port in d_ports:
                for s_host in s_hosts:
                    for d_host in d_hosts:
                        line = "ip access-list %s " % self.name
                        if rule['action'] == "allow":
                            action = "permit "
                        else:
                            action = "deny "
                        line += action
                        line += rule['protocol'] + " "
                        if ipaddr.IPNetwork(s_host).prefixlen in [32, 128]:
                            line += "host %s " % s_host
                        else:
                            line += s_host + " "
                        line += str(s_port) + " "
                        if ipaddr.IPNetwork(d_host).prefixlen in [32, 128]:
                            line += "host %s " % d_host
                        else:
                            line += d_host + " "
                        line += str(d_port) + " "
                        if line not in config_blob:
                            config_blob.append(line)
    return config_blob

