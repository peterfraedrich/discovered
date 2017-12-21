# DiscoveRed
Python service discovery using Redis

### Why?
Because there's no real lightweight service discovery mechanisms for Python that I could find, so I wrote my own.

### How does it work?
DiscoveRed uses Redis as a k/v store to hold service information

## API
```python

discovered.ServiceDiscovery(redis_host, redis_port, redis_db, redis_auth, ttl, auto)
    
    redis_host (default: localhost) : redis host to connect to
    redis_port (default: 6379) : redis port
    redis_db (default: 0) : redis db index for the service discovery information
    redis_auth (default: None) : redis auth string if required
    ttl (default: -1) : set a TTL on nodes, requiring them to re-register to stay enabled
    auto (default: True) : auto-discover node details on registration

    Instantiates a new connection to the Redis service discovery keys.

    Returns: None


    register_service(service_name, endpoint, [endpoint_type, auth_type, auth_credentials, backend, description])

        service_name : the service name for the new service
        endpoint : the endpoint of whatever service this service is offering
        endpoint_type (default: '') : descriptive type for endpoint
        auth_type (default: None) : type of auth required for endpoint
        auth_credentials (default: None) : credentials for the endpoint
        backend (default: '') : descriptive label for the backend service
        description (default: '') : human-readable description of the service

        Registers a new service with discovery.

        Returns: dict


    register_node(service_name, node_name, [ ip, fqdn, os, platform_name, arch, cpu_count, memory, last_boot, auto])

        service_name : the service the node belongs to
        node_name : friendly name for the node; must be unique
        ip (default: None) : IP address of the node
        fqdn (default: None) : the FQDN of the node
        os (default: None) : the operating system of the node
        platform_name (default: None) : the OS type of the system (Windows, Linux, Darwin, etc.)
        arch (default: None) : system architecture of the node (ex. x86_64, i386, etc.)
        cpu_count (default: None) : number of cores for the node
        memory (default: None) : amount of available virtual memory, in MB
        last_boot (default: None) : timestamp of the node's last restart
        auto (default: True) : auto-discover node info, can override __init__'s auto setting

        Registers a new node and associates it with a service

        Returns: dict


    get_service(service_name)

        service_name : name of the service info to get

        Gets information about a service

        Returns: dict


    get_nodes(service_name)

        service_name : the service to get the node information about

        Gets information about registered nodes for a service

        Returns: list


    list_services()

        Lists all services in the configured service group

        Returns: list


    list_service_groups()

        Lists all service groups on the Redis host

        Returns: list


    remove_node(service_name, node_name)

        service_name : name of the service the node belongs to
        node_name : the friendly name of the node to remove

        Removes a node from a service

        Returns: str


    remove_service(service_name)

        service_name : name of the service to remove

        Removes a service from the service group

        Returns: str


    remove_service_group(service_group)

        service_group : name of the service group to remove

        Removes an entire service group from the service discovery.

        Returns: str
```

#### TODO
* Redis Sentinel integration