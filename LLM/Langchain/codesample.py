
from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import EC2
from diagrams.aws.network import ELB, Route53
from diagrams.aws.security import WAF
from diagrams.onprem.client import User
from diagrams.onprem.network import Nginx
from diagrams.programming.framework import Django, Angular

with Diagram("Human Resource Management System Architecture", show=False, outformat="svg"):
    user = User("User")

    with Cluster("AWS"):
        firewall = WAF("Firewall")
        load_balancer = ELB("Load Balancer")

        with Cluster("Backend"):
            django_app = Django("Django App")
            db = EC2("Database")

        with Cluster("Frontend"):
            angular_app = Angular("Angular App")
            nginx = Nginx("Nginx")

    user >> Edge(color="darkgreen", label="Access") >> angular_app
    angular_app >> Edge(color="darkblue", label="API Calls") >> nginx
    nginx >> Edge(color="darkorange", label="Reverse Proxy") >> load_balancer
    load_balancer >> Edge(color="darkred", label="Load Balancing") >> django_app
    django_app >> Edge(color="darkpurple", label="Database") >> db

    firewall >> Edge(color="darkgray", label="Security") >> load_balancer
    load_balancer >> Edge(color="darkgray", label="Security") >> django_app
    django_app >> Edge(color="darkgray", label="Security") >> db