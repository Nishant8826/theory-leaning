curl -fsSL https://get.docker.com -o install-docker.sh
sudo sh install-docker.sh

docker run -d --restart unless-stopped --name win11react -p 3000:3000 blueedge/win11react:latest

gcloud compute instances create linuxfirst --project=nishant-learn --zone=us-central1-c --machine-type=e2-medium --network-interface=network-tier=PREMIUM,stack-type=IPV4_ONLY,subnet=default --metadata=enable-osconfig=TRUE --maintenance-policy=MIGRATE --provisioning-model=STANDARD --service-account=370978152656-compute@developer.gserviceaccount.com --scopes=https://www.googleapis.com/auth/devstorage.read_only,https://www.googleapis.com/auth/logging.write,https://www.googleapis.com/auth/monitoring.write,https://www.googleapis.com/auth/service.management.readonly,https://www.googleapis.com/auth/servicecontrol,https://www.googleapis.com/auth/trace.append --tags=http-server,https-server --create-disk=auto-delete=yes,boot=yes,device-name=linuxfirst,disk-resource-policy=projects/nishant-learn/regions/us-central1/resourcePolicies/default-schedule-1,image=projects/ubuntu-os-cloud/global/images/ubuntu-2404-noble-amd64-v20260316,mode=rw,size=10,type=pd-balanced --no-shielded-secure-boot --shielded-vtpm --shielded-integrity-monitoring --labels=goog-ops-agent-policy=v2-template-1-5-0,goog-ec-src=vm_add-gcloud --reservation-affinity=any && printf 'agentsRule:\n  packageState: installed\n  version: latest\ninstanceFilter:\n  inclusionLabels:\n  - labels:\n      goog-ops-agent-policy: v2-template-1-5-0\n' > config.yaml && gcloud compute instances ops-agents policies create goog-ops-agent-v2-template-1-5-0-us-central1-c --project=nishant-learn --zone=us-central1-c --file=config.yaml

---

---
Prev : [03_Cloud_Computing_And_Data_Centers.md](03_Cloud_Computing_And_Data_Centers.md) | Next : [05_DevOps_Basics_Tools_and_Roles.md](05_DevOps_Basics_Tools_and_Roles.md)
---
