# Civis Analytics Assignment

## Disclaimer

This setup is not meant to be used in production. It is simply for demonstration purposes.

## Pre-requsities

* [Vagrant](https://www.vagrantup.com/)
* [Ansible](https://www.ansible.com/)

You don't need Docker for this, as Docker will be installed on the VM.

## Stack

* *App*: A simple "Task Manager" web application built with Flask
* *MongoDB*: Database tier for the app
* *ELK stack*: Monitoring
* *Vagrant*: Provisioning VM + entire stack

## Quickstart

Issuing this command will bring up the entire infrastructure:
```bash
vagrant up
```

## Services

After `vagrant up` has successfully completed, run this to see how you can access the app as well as Kibana on your browser:

```bash
IP=`grep "^vagrant_ip" Vagrantfile | awk -F '=' '{print $2}' | tr -d ' "'` && \
echo "Webapp: http://$IP:80" && \
echo "Kibana: http://$IP:5601"
```

In order to login to Kibana, you can use these credentials:
* Username: *elastic*
* Password: *changeme*

Filebeat, Metricbeat and Packetbeat are all configured to push metrics to Logstash and Elasticsearch. You will need to create indexes via Kibana to visualize and discover metrics.

## Known issues

* Log messages are garbled in Logstash, mostly due to encoding issues

## References

* Official Elastic Ansible role for Beats: https://github.com/elastic/ansible-beats
* Awesome docker-compose-based ELK stack: https://github.com/deviantony/docker-elk
* geerlingguy's Docker install Ansible role: https://galaxy.ansible.com/geerlingguy/docker
