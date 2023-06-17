# General config.
# Paths should be relative to the parent directory. All paths are addressed as ../PATH
DEFAULT_HOST = "example.com"
DEFAULT_VHOST_TEXT = 'proxy_set_header Upgrade $http_upgrade;\nproxy_set_header Connection "upgrade";\nproxy_http_version 1.1;'
LOG_FILE_PATH = "vhost_pop_logs.log"
TIMESTAMP_FORMAT = "%Y/%m/%d %H:%M: "
CONTAINERS_PATH = "containers"
VHOSTD_PATH = "containers/nginx/vhost.d"
LINODE_INTEGRATION = False

# Linode integration config. Only applies if LINODE_INTEGRATION == True.
if LINODE_INTEGRATION == True:
    API_KEY = ""  # Your personal access token from Linode
    DOMAIN_ID = 2278333  # You can find this in the url on the domains page for a domain: https://cloud.linode.com/domains/#######
    TARGET_IP = "139.144.25.238"  # The IP of the target host
