
# 🪨 MINERALCO Deployment Guide v1.0.0
## Mineral Intelligence Network for Equation-of-state Research, Atomic Lattice COmputation

**DOI**: 10.5281/zenodo.19009597  
**Repository**: github.com/gitedeeper9/mineralco  
**Web**: mineralco.netlify.app

---

## 📋 Deployment Overview

### Deployment Architectures

| Architecture | Use Case | Resources | Data Processing |
|-------------|----------|-----------|-----------------|
| **Single Node** | Local analysis | 1 server (8GB RAM, 4 CPU) | On-demand |
| **Research Cluster** | Regional center | 4-8 nodes (32GB RAM, 16 CPU) | Batch processing |
| **Cloud-Based** | Global access | Auto-scaling | API endpoints |
| **Edge** | Field stations | Raspberry Pi 4 | Real-time EOS |

---

## 🏗️ Architecture Components

```

┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Data Sources   │────▶│  Data Loaders   │────▶│  Local Storage  │
│  (MINERAL DB,   │     │  (MineralDB,    │     │  (HDF5/NetCDF)  │
│   Synchrotron)  │     │   DAC, RRUFF)   │     │                 │
└─────────────────┘     └─────────────────┘     └─────────────────┘
│                       │                       │
└───────────────────────┼───────────────────────┘
▼
┌─────────────────┐
│  EOSFitter      │
│  (Core Engine)  │
└─────────────────┘
│
┌───────────────────────┼───────────────────────┐
▼                       ▼                       ▼
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│ ThermalCorrector│     │ LatticeAnalyzer │     │  PhaseMapper    │
│ (Mie-Grüneisen) │     │  (Symmetry,     │     │  (CSI, Phase    │
│                 │     │   Lattice Energy│     │   Boundaries)   │
└─────────────────┘     └─────────────────┘     └─────────────────┘
│                       │                       │
└───────────────────────┼───────────────────────┘
▼
┌─────────────────┐
│  CSI Composite  │
│  (0-1)          │
└─────────────────┘
│
┌───────────────────────┼───────────────────────┐
▼                       ▼                       ▼
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Reports       │     │  Dashboard      │     │  API/REST       │
│ (PDF/CSV/JSON)  │     │  (Netlify)      │     │  (Optional)     │
└─────────────────┘     └─────────────────┘     └─────────────────┘

```

---

## 🔧 Local Deployment (Single Node)

### 1. Hardware Requirements

```yaml
Minimum Specifications:
  CPU: 4+ cores (Intel i5/AMD Ryzen 5)
  RAM: 8GB
  Storage: 50GB SSD
  Network: Internet connection for data downloads
  
Recommended Specifications:
  CPU: 8+ cores (Intel i7/AMD Ryzen 7)
  RAM: 16GB
  Storage: 200GB SSD
  Network: 100 Mbps+
  
Data Requirements:
  - MINERAL Database: ~10 MB
  - Synchrotron DAC Data: ~5 GB
  - RRUFF Database: ~2 GB
  - NIST Crystal Data: ~500 MB
  - Total: ~30-50 GB
```

2. Installation Steps

```bash
# 1. Prepare the system
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3-pip docker.io docker-compose git \
  libhdf5-dev libnetcdf-dev libopenblas-dev

# 2. Clone repository
git clone https://github.com/gitedeeper9/mineralco.git
cd mineralco

# 3. Configure environment
cp .env.example .env
nano .env  # Edit with your settings

# 4. Install Python package
pip install --upgrade pip
pip install mineralco

# Or install from source
pip install -e .[all]

# 5. Create data directories
mkdir -p data/{raw,processed,cache}
mkdir -p logs
mkdir -p output/{reports,figures}

# 6. Download MINERAL database
mineralco-download --source mineral_db --output ./data/raw

# 7. Initialize database (if using PostgreSQL)
mineralco-db init

# 8. Run test processing
mineralco-process --mineral bridgmanite --output ./output

# 9. Verify deployment
mineralco-validate --mineral bridgmanite --experimental ./data/raw/bridgmanite.csv
```

3. Configuration File Example

```yaml
# config/config.yaml
project:
  name: "MINERALCO"
  version: "1.0.0"
  data_dir: "./data"
  output_dir: "./output"
  log_dir: "./logs"

data_sources:
  mineral_db:
    enabled: true
    source: "stixrude_2011"
    local_path: "./data/raw/mineral_db.json"
    update_frequency: "yearly"
  
  synchrotron:
    enabled: true
    sources: ["aps", "esrf", "spring8"]
    local_path: "./data/raw/synchrotron"
    update_frequency: "monthly"
  
  rruff:
    enabled: true
    local_path: "./data/raw/rruff"
    update_frequency: "quarterly"
  
  nist:
    enabled: true
    local_path: "./data/raw/nist_crystal"
    update_frequency: "yearly"

minerals:
  benchmark: 47
  primary_focus: ["bridgmanite", "forsterite", "periclase", "ringwoodite", "ε-iron"]
  
  bridgmanite:
    formula: "MgSiO3"
    system: "orthorhombic"
    space_group: "Pbnm"
    K0: 260.7
    Kprime: 3.97
    V0: 24.45
    alpha: 2.0e-5
    gamma: 1.57

processing:
  eos_fitter:
    method: "BM3"
    fitting_algorithm: "levenberg_marquardt"
    uncertainty_propagation: true
    confidence_level: 0.95
  
  thermal_corrector:
    enabled: true
    model: "mie_gruneisen"
    debye_model: true
    q_exponent: 1.5  # γ(V) = γ₀·(V/V₀)^q
  
  lattice_analyzer:
    symmetry_tolerance: 0.005  # 0.5%
    born_lande: true
    anisotropy_calculation: true
  
  phase_mapper:
    csi_thresholds:
      stable: 0.65
      metastable: 0.85
      transition: 0.85
    clapeyron_calculation: true
    phase_diagram_resolution: 0.1  # GPa

csi:
  weights:
    K0: 0.28
    Vs: 0.19
    Kprime: 0.17
    Sy: 0.13
    alpha: 0.10
    gamma: 0.09
    U_lattice: 0.04
  
  output_formats: ["csv", "json", "netcdf"]

api:
  enabled: false
  host: "0.0.0.0"
  port: 8000
  workers: 4
  rate_limit: 100  # requests per minute

dashboard:
  enabled: true
  host: "127.0.0.1"
  port: 5000
  debug: false
  update_interval: 3600  # seconds

database:
  enabled: false
  type: "postgresql"
  host: "localhost"
  port: 5432
  name: "mineralco"
  user: "mineralco_user"
  password: "${DB_PASSWORD}"

logging:
  level: "INFO"
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
  file: "./logs/mineralco.log"
  max_size: 100  # MB
  backup_count: 5
```

---

🌐 Multi-Node Deployment (Research Cluster)

Cluster Architecture

```
                    ┌─────────────────────────────────────┐
                    │         Master Node                  │
                    │    (Orchestration + Database)        │
                    └─────────────────────────────────────┘
                                      │
              ┌───────────────────────┼───────────────────────┐
              ▼                       ▼                       ▼
    ┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
    │   Worker 1      │     │   Worker 2      │     │   Worker 3      │
    │   (BM3 EOS)     │     │ (Thermal + CSI) │     │ (Phase Mapping) │
    └─────────────────┘     └─────────────────┘     └─────────────────┘
              │                       │                       │
              ▼                       ▼                       ▼
    ┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
    │   Bridgmanite   │     │   Olivine       │     │   Ringwoodite   │
    │   Calculations  │     │   Calculations  │     │   Calculations  │
    └─────────────────┘     └─────────────────┘     └─────────────────┘
```

Cluster Configuration

```yaml
# config/cluster.yaml
cluster:
  name: "mineralco-cluster"
  master_node: "192.168.1.100"
  nodes:
    - id: "worker-01"
      ip: "192.168.1.101"
      role: "bm3_eos"
      minerals: ["bridgmanite", "post-perovskite", "ferropericlase"]
      cpu: 16
      ram: 32
      storage: 200
    - id: "worker-02"
      ip: "192.168.1.102"
      role: "thermal_csi"
      minerals: ["forsterite", "wadsleyite", "ringwoodite"]
      cpu: 16
      ram: 32
      storage: 200
    - id: "worker-03"
      ip: "192.168.1.103"
      role: "phase_mapper"
      minerals: ["all_transitions"]
      cpu: 16
      ram: 64
      storage: 500

scheduling:
  method: "round_robin"
  max_jobs_per_node: 8
  retry_failed: 3

distributed_storage:
  type: "glusterfs"
  mount_point: "/mnt/mineralco-data"
  replica_count: 2
  
database:
  type: "timescaledb"
  host: "192.168.1.100"
  port: 5432
  replication: true
```

Deployment Script

```bash
#!/bin/bash
# deploy_cluster.sh

echo "🪨 Deploying MINERALCO on research cluster..."

MASTER_NODE="192.168.1.100"
WORKER_NODES=("192.168.1.101" "192.168.1.102" "192.168.1.103")

# Deploy on master node
ssh user@$MASTER_NODE << 'EOF'
  cd ~/mineralco
  git pull
  pip install -e .[all]
  
  # Initialize database
  docker-compose -f docker-compose.cluster.yml up -d timescaledb
  
  # Start master services
  docker-compose -f docker-compose.cluster.yml up -d master
  
  # Initialize distributed storage
  sudo glusterfs volume create mineralco-volume replica 2 \
    transport tcp \
    192.168.1.100:/data/mineralco \
    192.168.1.101:/data/mineralco \
    192.168.1.102:/data/mineralco
EOF

# Deploy on worker nodes
for NODE in "${WORKER_NODES[@]}"; do
  ssh user@$NODE << 'EOF'
    cd ~/mineralco
    git pull
    pip install -e .[all]
    
    # Mount distributed storage
    sudo mount -t glusterfs 192.168.1.100:/mineralco-volume /mnt/mineralco-data
    
    # Start worker service
    docker-compose -f docker-compose.cluster.yml up -d worker
EOF
done

echo "✅ Cluster deployment complete!"
```

---

☁️ Cloud Deployment

AWS Deployment

```bash
# 1. Launch EC2 instance (Ubuntu 22.04, t2.large or better)
# 2. SSH into instance
ssh -i your-key.pem ubuntu@ec2-instance-ip

# 3. Install dependencies
sudo apt update
sudo apt install -y python3-pip docker.io docker-compose git
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker ubuntu

# 4. Clone and deploy
git clone https://github.com/gitedeeper9/mineralco.git
cd mineralco
pip install -e .[all]

# 5. Set up environment
cp .env.example .env
nano .env  # Configure database, API keys

# 6. Run with Docker Compose
docker-compose up -d

# 7. Configure security group
# - Allow HTTP (80) from 0.0.0.0/0
# - Allow HTTPS (443) from 0.0.0.0/0
# - Allow SSH (22) from your IP only
```

Netlify Deployment (Dashboard)

```bash
# Build static dashboard
cd dashboard
npm install
npm run build

# Deploy to Netlify
netlify deploy --prod --dir=build --site=mineralco
```

---

🐳 Docker Compose Production Deployment

docker-compose.prod.yml

```yaml
version: '3.8'

services:
  mineralco:
    image: gitedeeper9/mineralco:latest
    container_name: mineralco
    restart: unless-stopped
    ports:
      - "5000:5000"  # Web dashboard
      - "8000:8000"  # API
    volumes:
      - ./data:/data
      - ./config:/app/config
      - ./logs:/app/logs
    environment:
      - MINERALCO_ENV=production
      - DB_HOST=timescaledb
      - DB_PORT=5432
      - DB_NAME=mineralco
      - DB_USER=mineralco_user
      - DB_PASSWORD=${DB_PASSWORD}
      - LOG_LEVEL=INFO
    depends_on:
      - timescaledb
    networks:
      - mineralco-network
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  timescaledb:
    image: timescale/timescaledb:latest-pg15
    container_name: timescaledb
    restart: unless-stopped
    environment:
      - POSTGRES_DB=mineralco
      - POSTGRES_USER=mineralco_user
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    volumes:
      - timescaledb-data:/var/lib/postgresql/data
      - ./init-db.sql:/docker-entrypoint-initdb.d/init-db.sql
    networks:
      - mineralco-network

  nginx:
    image: nginx:alpine
    container_name: nginx
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf
      - ./nginx/ssl:/etc/nginx/ssl
      - ./dashboard/build:/usr/share/nginx/html
    depends_on:
      - mineralco
    networks:
      - mineralco-network

networks:
  mineralco-network:
    driver: bridge

volumes:
  timescaledb-data:
    driver: local
```

---

📊 Performance Optimization

Parallel Processing

```bash
# Set number of cores
export MINERALCO_NUM_CORES=$(nproc)

# Enable parallel processing in config
mineralco-config set processing.parallel true
mineralco-config set processing.num_workers 8
```

Caching

```bash
# Enable Redis caching
mineralco-config set cache.enabled true
mineralco-config set cache.host localhost
mineralco-config set cache.port 6379
```

Database Indexing

```sql
-- Create indexes for faster queries
CREATE INDEX idx_mineral_name ON mineral_data (mineral);
CREATE INDEX idx_pressure ON experimental_data (pressure);
CREATE INDEX idx_temperature ON experimental_data (temperature);
CREATE INDEX idx_csi ON phase_predictions (csi);
```

---

🔍 Monitoring

Prometheus Metrics

```yaml
# prometheus/prometheus.yml
scrape_configs:
  - job_name: 'mineralco'
    static_configs:
      - targets: ['localhost:9090']
    metrics_path: '/metrics'
    scrape_interval: 15s
```

Grafana Dashboard

Import the MINERALCO dashboard template from grafana/dashboards/mineralco.json

Health Checks

```bash
# API health check
curl http://localhost:5000/health
# Response: {"status": "healthy", "version": "1.0.0", "timestamp": "2026-03-14T12:00:00Z"}

# Database check
mineralco-db status

# Data integrity check
mineralco-validate --all
```

---

📈 Scaling Guidelines

Concurrent Users RAM CPU Instances
1-10 8GB 2 1
10-50 16GB 4 1-2
50-200 32GB 8 2-4
200-1000 64GB+ 16+ 4-8

---

🚨 Backup and Recovery

Automated Backup

```bash
#!/bin/bash
# backup.sh

BACKUP_DIR="/backup/mineralco"
DATE=$(date +%Y%m%d)

# Backup database
pg_dump -U mineralco_user mineralco > $BACKUP_DIR/db_$DATE.sql

# Backup data directory
tar -czf $BACKUP_DIR/data_$DATE.tar.gz /data/mineralco

# Backup configurations
cp /config/* $BACKUP_DIR/config/

# Keep only last 30 days
find $BACKUP_DIR -type f -mtime +30 -delete
```

Recovery

```bash
# Restore database
psql -U mineralco_user mineralco < $BACKUP_DIR/db_20260314.sql

# Restore data
tar -xzf $BACKUP_DIR/data_20260314.tar.gz -C /
```

---

📚 Deployment Checklist

· System requirements verified
· Dependencies installed
· Configuration files updated
· Database initialized
· Data downloaded
· Test calculations passed
· Security measures implemented
· Backup strategy configured
· Monitoring set up
· Documentation deployed
· SSL certificates installed
· Load testing completed

---

📞 Support

For deployment assistance:

· Email: gitdeeper@gmail.com
· GitHub Issues: https://github.com/gitedeeper9/mineralco/issues
· ORCID: 0009-0003-8903-0029

---

Version: 1.0.0
Last Updated: 2026-03-14
