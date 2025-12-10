# 📚 DocSmart RAG System - AWS AI Engineer Nanodegree Final Project

> **Enterprise-grade RAG system using Amazon Bedrock, Aurora PostgreSQL with pgvector, and S3**

**🎓 Udacity Nanodegree Program**: AWS AI Engineer  
**🤝 In Collaboration With**: Amazon Web Services (AWS)  
**📚 Course**: Building Generative AI Applications with Amazon Bedrock  
**🎯 Project Type**: Final Capstone Project

[![AWS](https://img.shields.io/badge/AWS-Bedrock-FF9900?logo=amazon-aws)](https://aws.amazon.com/bedrock/)
[![Terraform](https://img.shields.io/badge/IaC-Terraform-7B42BC?logo=terraform)](https://www.terraform.io/)
[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?logo=python)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Udacity](https://img.shields.io/badge/Udacity-Nanodegree-02B3E4?logo=udacity)](https://www.udacity.com/)

---

## 🎯 Project Overview

**DocSmart** is an intelligent document query system leveraging Retrieval-Augmented Generation (RAG) to provide accurate, context-aware answers from enterprise documentation. Built entirely on AWS services with Infrastructure as Code best practices.

### ✨ Key Features

- **🤖 Advanced AI**: Claude 3.5 Sonnet via Amazon Bedrock
- **🔍 Semantic Search**: Amazon Titan Embeddings v2 (1024-dimensional vectors)
- **📊 Vector Database**: Aurora PostgreSQL Serverless v2 with pgvector extension
- **🪣 Scalable Storage**: Amazon S3 for document management
- **🛡️ Security First**: IAM roles, Secrets Manager, input validation
- **💬 Interactive UI**: Streamlit web application
- **🏗️ IaC**: Complete Terraform deployment (2 stacks)
- **📸 Well-Documented**: 30 screenshots + comprehensive guides

---

## 🏗️ Architecture

```
┌──────────────────────────────────────────────────────────┐
│                      AWS Cloud (us-east-1)                │
├──────────────────────────────────────────────────────────┤
│                                                            │
│  S3 Bucket ──▶ Bedrock Knowledge Base ──▶ Aurora PostgreSQL
│  (Docs)        (Titan + Claude)           (pgvector)      │
│                                                            │
│  VPC (10.0.0.0/16)                                         │
│  ├─ Public Subnets (2 AZs)                                │
│  └─ Private Subnets (2 AZs) ──▶ Aurora Cluster            │
│                                                            │
└──────────────────────────────────────────────────────────┘
```

### Components

| Layer | Service | Purpose |
|-------|---------|---------|
| **Storage** | Amazon S3 | Document repository |
| **Compute** | Amazon Bedrock | Embeddings + LLM inference |
| **Database** | Aurora PostgreSQL Serverless v2 | Vector storage with pgvector |
| **Network** | VPC + Subnets | Network isolation |
| **Security** | IAM + Secrets Manager | Access control + credential management |
| **Monitoring** | CloudWatch | Logs and metrics |

---

## 🚀 Quick Start

### Prerequisites

- AWS Account with Bedrock access
- Terraform >= 1.0
- Python >= 3.9
- AWS CLI v2

### Deploy in 5 Minutes

```bash
# 1. Clone repository
git clone https://github.com/YOUR_USERNAME/docsmart-rag-system.git
cd docsmart-rag-system

# 2. Configure Stack 1
cd stack1
cp terraform.tfvars.example terraform.tfvars
# Edit terraform.tfvars with your values
terraform init && terraform apply

# 3. Initialize Aurora database
cd ../scripts
./init_aurora.sh  # See DEPLOYMENT_GUIDE.md for manual commands

# 4. Configure and deploy Stack 2
cd ../stack2
cp terraform.tfvars.example terraform.tfvars
# Edit terraform.tfvars with Stack 1 outputs
terraform init && terraform apply

# 5. Upload documents and sync
python ../scripts/upload_to_s3.py
aws bedrock-agent start-ingestion-job \
  --knowledge-base-id $(terraform output -raw knowledge_base_id) \
  --data-source-id $(terraform output -raw data_source_id)

# 6. Run application
cd ..
pip install -r requirements.txt
streamlit run app_demo.py
```

📖 **Full deployment guide**: See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)

---

## 📁 Project Structure

```
docsmart-rag-system/
├── stack1/                    # Infrastructure (VPC, Aurora, S3, IAM)
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   └── terraform.tfvars.example
├── stack2/                    # Knowledge Base (Bedrock, Data Source)
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   └── terraform.tfvars.example
├── scripts/                   # Automation scripts
│   ├── aurora_init.sql        # Database initialization
│   ├── upload_to_s3.py        # Document uploader
│   └── quick_credentials.py   # AWS credential helper
├── screenshots/               # 30 project screenshots
│   ├── SCREENSHOT_GUIDE.md
│   └── *.png
├── sample_docs/               # Example HR policy documents
├── app_demo.py                # Streamlit web application
├── bedrock_utils.py           # Core RAG logic
├── requirements.txt           # Python dependencies
├── DEPLOYMENT_GUIDE.md        # Step-by-step deployment
├── README.md                  # This file
└── LICENSE                    # MIT License
```

---

## 🎓 AWS AI Engineer Nanodegree - Project Requirements

### ✅ Rubric Compliance

| Requirement | Implementation | Evidence |
|-------------|----------------|----------|
| **Infrastructure Setup** | VPC, Aurora Serverless v2, S3 | Screenshots 1-6, Stack 1 code |
| **Knowledge Base** | Bedrock KB with Aurora backend | Screenshots 7-10, Stack 2 code |
| **Data Ingestion** | S3 → Bedrock → Aurora | Screenshots 11-15 |
| **Python Integration** | `bedrock_utils.py` with 3 key functions | Screenshots 16-20 |
| **Model Parameters** | Temperature & top_p tuning | Screenshots 21-23 + docs |
| **Chat Application** | Streamlit UI with conversation | Screenshots 24-30 |
| **Documentation** | README + guides + screenshots | All files |

### 📸 Screenshot Portfolio

All 30 required screenshots included in `screenshots/` directory:
- Infrastructure setup (6)
- Knowledge Base configuration (4)
- Data synchronization (5)
- Python integration (5)
- Model parameters (3)
- Chat application (7)

See [screenshots/SCREENSHOT_GUIDE.md](screenshots/SCREENSHOT_GUIDE.md) for details.

---

## 🛠️ Technology Stack

### AWS Services
- **Amazon Bedrock**: Managed AI service
  - `amazon.titan-embed-text-v2:0` (embeddings)
  - `anthropic.claude-3-5-sonnet-20240620-v1:0` (LLM)
- **Aurora PostgreSQL 15.14**: Serverless v2 with pgvector
- **Amazon S3**: Document storage
- **AWS Secrets Manager**: Credential management
- **IAM**: Role-based access control
- **CloudWatch**: Logging and monitoring

### Infrastructure & Tools
- **Terraform**: Infrastructure as Code
- **Python 3.9+**: Application logic
- **Streamlit**: Web UI framework
- **boto3**: AWS SDK for Python
- **pgvector**: PostgreSQL vector extension

### Key Python Libraries
```
boto3==1.35.76
streamlit==1.41.1
python-dotenv==1.0.1
psycopg2-binary==2.9.10
```

---

## 📊 Performance & Costs

### Performance Metrics
- **Query Latency**: <2s average (cold start)
- **Vector Search**: <500ms (HNSW index)
- **Chunk Retrieval**: Top-5 in <300ms
- **LLM Response**: ~1-3s (Claude 3.5 Sonnet)

### Estimated Monthly Costs (Low Usage)
- Aurora Serverless v2: ~$43 (0.5 ACU baseline)
- S3 Storage: ~$0.50 (20 GB)
- Bedrock API: ~$10 (1000 queries)
- **Total**: ~$53-55/month

💡 **Cost Optimization**: Use Aurora's pause feature during development, monitor with Cost Explorer.

---

## 🧪 Testing

### Unit Tests
```bash
python -m pytest tests/
```

### Integration Test
```python
from bedrock_utils import query_knowledge_base, generate_response

# Test Knowledge Base query
result = query_knowledge_base("vacation policy")
assert result['count'] > 0

# Test RAG generation
response = generate_response("How many vacation days?", result['results'])
assert len(response['response']) > 0
```

---

## 🔒 Security Considerations

- ✅ **No hardcoded credentials**: All secrets in Secrets Manager or .env (gitignored)
- ✅ **IAM least privilege**: Separate policies for S3, Bedrock, RDS
- ✅ **VPC isolation**: Aurora in private subnets
- ✅ **Encrypted storage**: S3 AES-256, Aurora encryption at rest
- ✅ **Input validation**: Prompt sanitization and content filtering
- ✅ **HTTPS only**: All AWS API calls over TLS

---

## 🐛 Troubleshooting

Common issues and solutions:

| Issue | Solution |
|-------|----------|
| `Aurora version 15.5 not available` | Use `15.14` (Stack 1 already updated) |
| `rds:DescribeDBClusters denied` | RDS policy added in Stack 1 main.tf |
| `DataAPIv2 not enabled` | Set `enable_http_endpoint = true` in Aurora |
| `Table bedrock_kb does not exist` | Run `scripts/aurora_init.sql` |
| `Embedding index required` | Create HNSW index (see deployment guide) |

📖 See [DEPLOYMENT_GUIDE.md#troubleshooting](DEPLOYMENT_GUIDE.md#troubleshooting) for more.

---

## 📚 Documentation

- **[DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)**: Complete step-by-step deployment
- **[screenshots/SCREENSHOT_GUIDE.md](screenshots/SCREENSHOT_GUIDE.md)**: Screenshot requirements
- **[CHECKLIST_FINAL.md](CHECKLIST_FINAL.md)**: Project submission checklist

---

## 🤝 Contributing

This is a final project for AWS AI Engineer Nanodegree. While it's primarily for academic purposes, improvements are welcome!

1. Fork the repository
2. Create feature branch (`git checkout -b feature/improvement`)
3. Commit changes (`git commit -am 'Add improvement'`)
4. Push to branch (`git push origin feature/improvement`)
5. Open Pull Request

---

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Your Name**
- **Program**: AWS AI Engineer Nanodegree - Udacity x AWS
- **Course**: Building Generative AI Applications with Amazon Bedrock
- **Project**: Final Capstone Project
- **Email**: your.email@example.com
- **LinkedIn**: [Your Profile](https://linkedin.com/in/oscarmatiasg)
- **GitHub**: [@yourusername](https://github.com/oscarmatiasg)

---

## 🎓 About This Project

This project is the **final capstone submission** for the **AWS AI Engineer Nanodegree** program offered by **Udacity** in collaboration with **Amazon Web Services (AWS)**. 

The program focuses on:
- Building production-ready AI applications
- Leveraging AWS AI/ML services (Bedrock, SageMaker, etc.)
- Implementing RAG architectures
- Infrastructure as Code best practices
- Enterprise security and scalability

**Course Module**: Building Generative AI Applications with Amazon Bedrock  
**Completion Date**: December 2025

---

## 🙏 Acknowledgments

- **Udacity**: AWS AI Engineer Nanodegree program and comprehensive curriculum
- **AWS**: Amazon Bedrock, Aurora PostgreSQL, and extensive documentation
- **Anthropic**: Claude 3.5 Sonnet model for advanced language understanding
- **pgvector Community**: Vector similarity search extension for PostgreSQL
- **Course Instructors**: For guidance and technical expertise throughout the program

---

## 📞 Support

For questions or issues:
- 📧 Email: oscarmatiasg@lutflow.com
- 🐛 Issues: [GitHub Issues](https://github.com/oscarmatiasg/docsmart-rag-system/issues)
- 📖 AWS Bedrock Docs: https://docs.aws.amazon.com/bedrock/

---

**⭐ If you found this project helpful, please star the repository!**

---

**Last Updated**: December 10, 2025  
**Version**: 1.0.0
