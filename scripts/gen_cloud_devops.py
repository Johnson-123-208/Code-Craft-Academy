"""Generate Cloud/DevOps course MDX lessons (keeps existing overview)."""
from __future__ import annotations

from gen_lesson_lib import (
    assert_no_bare_braces,
    bullets,
    code_block,
    mermaid,
    numbered,
    reading,
    render_lesson,
    table,
    write_lesson,
)

COURSE = "cloud-devops"


def L(
    title,
    slug,
    summary,
    order,
    why,
    intuition,
    core,
    diagram,
    code,
    complexity,
    tricks,
    mistakes,
    interview,
    practice,
    summary_sheet,
    further,
    duration=35,
    difficulty="intermediate",
    prerequisites=None,
    tags=None,
    module="",
    filename="",
):
    meta = {
        "title": title,
        "slug": slug,
        "summary": summary,
        "duration": duration,
        "difficulty": difficulty,
        "prerequisites": prerequisites or [],
        "tags": tags or [],
        "order": order,
    }
    sections = {
        "Why this matters": why,
        "Intuition": intuition,
        "Core concept in depth": core,
        "Diagram / flowchart": diagram,
        "Code": code,
        "Complexity analysis": complexity,
        "Tricks, tips and patterns": tricks,
        "Common mistakes and edge cases": mistakes,
        "Interview notes": interview,
        "Practice problems": practice,
        "Summary / cheat sheet": summary_sheet,
        "Further reading": further,
    }
    text = render_lesson(meta, sections)
    assert_no_bare_braces(text, f"{module}/{filename}")
    return write_lesson(COURSE, module, filename, text)


def expand_fundamentals():
    m = "01-cloud-fundamentals"
    # keep 01-cloud-and-aws-overview.mdx
    L(
        "Shared Responsibility and Cloud Security Mindset",
        "shared-responsibility-security",
        "Map the AWS shared responsibility model to concrete controls: identity, network, data, and application layers.",
        2,
        "Security incidents in the cloud rarely come from a broken hypervisor — they come from misconfigured identity, public storage, and open security groups. Shared responsibility clarifies what AWS guarantees versus what you must design, monitor, and prove.",
        "Think of a rented apartment. The landlord secures the building shell; you lock your door, choose who gets keys, and decide what valuables sit by the window. Shared responsibility is that split — formalized for compute, storage, databases, and serverless.",
        f"""### The split

{table(
    ["Layer", "AWS owns", "You own"],
    [
        ["Physical / hypervisor", "Facilities, hardware, virtualization", "N/A"],
        ["Network fabric", "Core routing, DDoS at edge (Shield Standard)", "Security groups, NACLs, VPC design"],
        ["Managed services", "Patching of service control plane", "Data classification, encryption keys usage, IAM"],
        ["EC2 / containers", "Host hypervisor", "OS patching (EC2), image hardening, app secrets"],
        ["Lambda / Fargate", "Runtime host OS", "Code, dependencies, IAM role, env secrets"],
    ]
)}

### Control families you must own

- **Identity**: IAM users/roles, federation, MFA, least privilege
- **Network**: private subnets, least-open ports, VPC endpoints
- **Data**: encryption at rest/in transit, key policy, retention
- **Detect**: CloudTrail, Config, GuardDuty, findings triage
- **Respond**: incident runbooks, isolation, rotation""",
        mermaid(
            """flowchart TB
    subgraph AWS["AWS responsibility"]
      HW[Hardware]
      HY[Hypervisor]
      EDGE[Edge / Shield]
    end
    subgraph YOU["Your responsibility"]
      IAM[IAM policies]
      NET[VPC / SG / NACL]
      DATA[Encryption / keys]
      APP[App / deps / secrets]
    end
    HW --> HY --> EDGE
    IAM --> NET --> DATA --> APP"""
        )
        + "\n\n### Dry-run: public S3 bucket\n\n"
        + table(
            ["Question", "Answer"],
            [
                ["Who encrypted the disk?", "AWS (or you via KMS)"],
                ["Who made the object world-readable?", "You — bucket policy / ACL"],
                ["Who must fix it?", "You — IAM/policy change + audit"],
            ],
        ),
        code_block(
            "python",
            '''def risk_score(public_access: bool, mfa: bool, cloudtrail: bool) -> int:
    """Toy scoring for security posture discussions (not a real auditor)."""
    score = 0
    if public_access:
        score += 50
    if not mfa:
        score += 30
    if not cloudtrail:
        score += 20
    return score


if __name__ == "__main__":
    print(risk_score(True, False, True))
''',
        ),
        table(
            ["Control gap", "Blast radius", "Typical fix cost"],
            [
                ["Open SG 0.0.0.0/0 on SSH", "Host compromise", "Minutes to close; days to investigate"],
                ["Wildcard IAM *:*", "Account takeover path", "Policy rewrite + access review"],
                ["No CloudTrail", "Blind incident response", "Enable + SIEM wiring"],
            ],
        ),
        bullets(
            [
                "Start designs from identity and private networking, not from fancy services.",
                "Prefer IAM roles over long-lived access keys.",
                "Encrypt by default; decide CMK vs AWS-managed deliberately.",
                "Enable CloudTrail organization trail before you need it.",
            ]
        ),
        bullets(
            [
                "Assuming managed service means zero security work.",
                "Leaving default VPCs and 0.0.0.0/0 rules in production.",
                "Mixing human and machine credentials.",
                "Skipping MFA on root and privileged roles.",
            ]
        ),
        "Explain shared responsibility with a concrete service (EC2 vs Lambda vs S3). Interviewers want examples of controls you would enable on day one.",
        numbered(
            [
                "List your responsibilities for an RDS Multi-AZ app (easy)",
                "Design least-privilege IAM for a CI deploy role (medium)",
                "Draft a 24-hour incident checklist for leaked access keys (hard)",
            ]
        ),
        bullets(
            [
                "AWS secures the cloud; you secure in the cloud.",
                "Identity, network, data, detect, respond.",
                "Managed ≠ unattended.",
                "Prove controls with logs and Config rules.",
            ]
        ),
        reading(
            [
                ("AWS Shared Responsibility Model", "https://aws.amazon.com/compliance/shared-responsibility-model/"),
                ("AWS Security Hub", "https://docs.aws.amazon.com/securityhub/"),
                ("CIS AWS Foundations Benchmark", "https://www.cisecurity.org/benchmark/amazon_web_services"),
            ]
        ),
        module=m,
        filename="02-shared-responsibility-security.mdx",
        tags=["security", "iam", "aws", "compliance"],
        prerequisites=["cloud-and-aws-overview"],
    )

    L(
        "Regions, Availability Zones, and Edge Locations",
        "regions-azs-edge",
        "Design for failure domains using Regions, AZs, and edge networks — with latency, residency, and cost trade-offs.",
        3,
        "Availability is a topology problem. Choosing one AZ is a single point of failure. Choosing the wrong Region burns latency budget and may violate data residency. Edge locations shrink distance for static and cached content.",
        "A Region is a metro area of data centers. An AZ is an independent power/network failure domain inside that metro. Edge locations are tiny outposts that cache and terminate TLS closer to users — like neighborhood lockers for your bits.",
        f"""### Geography vocabulary

- **Region**: isolated geographic area with multiple AZs (example: `ap-south-1`)
- **Availability Zone**: one or more discrete data centers with redundant power/network
- **Local Zones / Wavelength**: specialized low-latency extensions
- **Edge location**: CloudFront / Route 53 PoP

### Design rules of thumb

{table(
    ["Goal", "Pattern"],
    [
        ["Survive AZ failure", "Multi-AZ compute + Multi-AZ data store"],
        ["Survive Region failure", "Multi-Region active-passive or active-active"],
        ["Lower static latency", "CloudFront near users"],
        ["Data residency", "Pin Region; control replication"],
    ]
)}

### Latency and cost

Cross-AZ traffic is usually cheap but not free; cross-Region is slower and costlier. Measure before you replicate everything everywhere.""",
        mermaid(
            """flowchart LR
    User --> Edge[Edge PoP]
    Edge --> R1["Region A"]
    subgraph R1a["Region A"]
      AZ1[AZ-a]
      AZ2[AZ-b]
      AZ3[AZ-c]
    end
    R1 --> AZ1
    R1 --> AZ2
    R1 --> AZ3"""
        )
        + "\n\n### Dry-run: Multi-AZ API\n\nPlace ALB across AZs, run tasks in ≥2 AZs, put RDS Multi-AZ. Fail AZ-a → ALB drains unhealthy targets; standby DB promotes.",
        code_block(
            "python",
            '''def choose_region(user_latency_ms: dict[str, float], residency: set[str]) -> str:
    """Pick lowest-latency allowed Region (toy heuristic)."""
    allowed = {r: ms for r, ms in user_latency_ms.items() if r in residency}
    if not allowed:
        raise ValueError("no Region satisfies residency")
    return min(allowed, key=allowed.get)


if __name__ == "__main__":
    print(
        choose_region(
            {"ap-south-1": 12, "us-east-1": 180, "eu-west-1": 140},
            {"ap-south-1", "eu-west-1"},
        )
    )
''',
        ),
        table(
            ["Topology", "Availability upside", "Cost / complexity"],
            [
                ["Single-AZ", "Low", "Lowest — fragile"],
                ["Multi-AZ", "High for AZ loss", "Moderate"],
                ["Multi-Region", "Highest DR", "High — data sync hard"],
            ],
        ),
        bullets(
            [
                "Default production: Multi-AZ for stateful stores.",
                "Pin Regions for compliance; document why.",
                "Use health checks that fail closed across AZs.",
                "Cache at the edge when content is cacheable.",
            ]
        ),
        bullets(
            [
                "Confusing AZ letters across accounts (they are shuffled).",
                "Single NAT Gateway as silent SPOF.",
                "Replicating databases Multi-Region without conflict strategy.",
                "Ignoring data transfer line items.",
            ]
        ),
        "Sketch users → edge → Multi-AZ Region. Discuss RPO/RTO for Multi-Region. Mention AZ name remapping across accounts.",
        numbered(
            [
                "Convert a single-AZ diagram to Multi-AZ (easy)",
                "Estimate when Multi-Region is worth it for RTO=1h (medium)",
                "Design DNS failover between two Regions (hard)",
            ]
        ),
        bullets(
            [
                "Region = geography; AZ = failure domain; edge = proximity.",
                "Multi-AZ is the production baseline for most apps.",
                "Residency and latency constrain Region choice.",
                "Cross-Region is a product decision, not a default toggle.",
            ]
        ),
        reading(
            [
                ("AWS Global Infrastructure", "https://aws.amazon.com/about-aws/global-infrastructure/"),
                ("Regions and AZs", "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-regions-availability-zones.html"),
            ]
        ),
        module=m,
        filename="03-regions-azs-edge.mdx",
        tags=["aws", "ha", "networking", "regions"],
        prerequisites=["cloud-and-aws-overview"],
    )

    L(
        "Cloud Pricing and Cost Mental Models",
        "cloud-pricing-mental-models",
        "Reason about cloud bills: compute dimensions, data transfer, storage classes, reserved capacity, and architectural cost levers.",
        4,
        "Surprise bills kill trust. Engineers who understand pricing dimensions design cheaper architectures without sacrificing reliability — and can defend trade-offs in design reviews.",
        "Cloud pricing is a multidimensional vending machine: you pay for time, size, requests, bytes moved, and sometimes for idle reservations that buy discounts. The skill is knowing which dial you are turning.",
        f"""### Primary dimensions

{table(
    ["Resource", "Typical bill drivers"],
    [
        ["EC2 / Fargate", "vCPU-hours, memory-hours, disk"],
        ["Lambda", "Invocations + GB-seconds"],
        ["S3", "GB-month, requests, retrieval, transfer"],
        ["RDS", "Instance hours, storage, I/O, Multi-AZ"],
        ["Data transfer", "Out to internet, cross-Region, some cross-AZ"],
    ]
)}

### Discount levers

- **Savings Plans / Reserved Instances**: commit to usage, lower unit price
- **Spot**: interruptible capacity for fault-tolerant workloads
- **Storage tiering**: S3 IA / Glacier for cold data
- **Architecture**: fewer bytes egressed, right-sized instances, caching

### FinOps loop

Measure → allocate (tags) → optimize → review. Without tags, you only have a mystery PDF.""",
        mermaid(
            """flowchart LR
    Arch[Architecture choice] --> Dim[Pricing dimensions]
    Dim --> Bill[Monthly bill]
    Bill --> Tags[Tag allocation]
    Tags --> Opt[Right-size / cache / tier]
    Opt --> Arch"""
        )
        + "\n\n### Dry-run\n\nMoving large media through an ALB every request vs CloudFront cache: egress and origin load both drop when hit ratio rises.",
        code_block(
            "python",
            '''def s3_storage_cost_gb_month(gb: float, class_price: float = 0.023) -> float:
    return round(gb * class_price, 4)


def lambda_gb_seconds(invocations: int, duration_ms: float, memory_mb: int) -> float:
    return invocations * (duration_ms / 1000.0) * (memory_mb / 1024.0)


if __name__ == "__main__":
    print("S3:", s3_storage_cost_gb_month(500))
    print("GB-s:", round(lambda_gb_seconds(2_000_000, 150, 256), 2))
''',
        ),
        table(
            ["Optimization", "Savings potential", "Risk"],
            [
                ["Right-size EC2", "High", "CPU steal / latency"],
                ["CloudFront cache", "High egress", "TTL / invalidation complexity"],
                ["Spot for workers", "Very high", "Interruptions"],
                ["Multi-Region active-active", "Negative (costs more)", "Operational load"],
            ],
        ),
        bullets(
            [
                "Tag `env`, `service`, `owner` on day one.",
                "Prefer architectural savings over coupon hunting.",
                "Watch data transfer — the silent line item.",
                "Set budgets and anomaly detection early.",
            ]
        ),
        bullets(
            [
                "NAT Gateway hours + data processing surprises.",
                "Cross-AZ chatty microservices.",
                "Over-provisioned RDS 'just in case'.",
                "Leaving unused EBS volumes and Elastic IPs.",
            ]
        ),
        "Walk through a bill sketch for a 3-tier app. Mention egress, Multi-AZ, and one discount mechanism. Show you can propose a cheaper design that still meets SLOs.",
        numbered(
            [
                "Estimate monthly S3 cost for 2 TB standard (easy)",
                "Compare always-on EC2 vs Lambda for a spiky API (medium)",
                "Find three cost bugs in a chatty Multi-AZ microservice design (hard)",
            ]
        ),
        bullets(
            [
                "Pay for time, size, requests, and bytes moved.",
                "Tags unlock ownership of spend.",
                "Cache and right-size beat blind reservations.",
                "Egress and NAT deserve explicit design attention.",
            ]
        ),
        reading(
            [
                ("AWS Pricing", "https://aws.amazon.com/pricing/"),
                ("AWS Well-Architected Cost Optimization", "https://docs.aws.amazon.com/wellarchitected/latest/cost-optimization-pillar/welcome.html"),
            ]
        ),
        module=m,
        filename="04-cloud-pricing-mental-models.mdx",
        tags=["cost", "finops", "aws"],
        prerequisites=["cloud-and-aws-overview"],
        duration=30,
    )


def aws_core():
    m = "02-aws-core"
    lessons = [
        (
            "IAM: Users, Roles, Policies, and Least Privilege",
            "iam-identity-access",
            "Master IAM principals, policies, trust relationships, and least-privilege patterns for humans and workloads.",
            1,
            ["iam", "security", "aws"],
            "iam",
            '''flowchart TB
    Human[Human / IdP] --> Role[IAM Role]
    CI[CI System] --> Role
    Role --> Policy[Identity policy]
    Policy --> API[AWS API]
    ResPolicy[Resource policy] --> API''',
            '''def allows(action: str, resource: str, statements: list[dict]) -> bool:
    """Extremely simplified IAM allow evaluator for teaching."""
    permitted = False
    for stmt in statements:
        effect = stmt.get("Effect", "Deny")
        actions = stmt.get("Action", [])
        resources = stmt.get("Resource", [])
        action_match = action in actions or "*" in actions
        resource_match = resource in resources or "*" in resources
        if not (action_match and resource_match):
            continue
        if effect == "Deny":
            return False
        if effect == "Allow":
            permitted = True
    return permitted


if __name__ == "__main__":
    stmts = [
        {"Effect": "Allow", "Action": ["s3:GetObject"], "Resource": ["arn:aws:s3:::app/*"]},
        {"Effect": "Deny", "Action": ["s3:DeleteObject"], "Resource": ["*"]},
    ]
    print(allows("s3:GetObject", "arn:aws:s3:::app/a.txt", stmts))
''',
            "IAM is the front door to every AWS API. Misconfigured policies are the most common path to account compromise. Roles with short-lived credentials beat long-lived keys for both people and machines.",
            "An IAM **policy** is a JSON permission slip. A **role** is an identity that services or people can assume. Trust policies say *who* may assume; permission policies say *what* they may do. Least privilege means the smallest slip that still ships the feature.",
            f"""### Building blocks

- **User**: long-lived human identity (prefer federation instead)
- **Group**: permission bundles for humans
- **Role**: assumable identity for services, CI, cross-account
- **Policy**: Allow/Deny statements on actions + resources + conditions

### Evaluation order (mental model)

Explicit Deny wins. Then Allow. Else implicit Deny. Resource policies (S3, KMS, etc.) combine with identity policies — both must allow.

### Patterns

{table(
    ["Pattern", "Use when"],
    [
        ["Instance / task role", "EC2, ECS, Lambda need AWS APIs"],
        ["CI OIDC role", "GitHub Actions → AWS without static keys"],
        ["Break-glass admin", "Rare emergency with MFA + logging"],
        ["Permission boundaries", "Delegate admin safely in large orgs"],
    ]
)}""",
            "Explain trust vs permissions policy. Show an OIDC deploy role. Discuss confused deputy and `aws:SourceAccount` conditions.",
            [
                "Write a least-privilege S3 read policy for one prefix (easy)",
                "Design GitHub OIDC role trust for one repo (medium)",
                "Find the privilege escalation in a sample policy set (hard)",
            ],
            [
                ("IAM User Guide", "https://docs.aws.amazon.com/IAM/latest/UserGuide/introduction.html"),
                ("IAM Policy Simulator", "https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_testing-policies.html"),
            ],
        ),
        (
            "VPC Networking Deep Dive",
            "vpc-networking",
            "Design VPCs with subnets, route tables, gateways, endpoints, security groups, and NACLs for private workloads.",
            2,
            ["vpc", "networking", "aws"],
            "vpc",
            '''flowchart TB
    Internet((Internet)) --> IGW[Internet Gateway]
    IGW --> Pub[Public subnet]
    Pub --> NAT[NAT Gateway]
    NAT --> Priv[Private subnet]
    Priv --> VPCE[VPC Endpoint S3]
    Priv --> ENI[ENI / ENI tasks]''',
            '''def is_private_ipv4(ip: str) -> bool:
    a, b, *_ = (int(x) for x in ip.split("."))
    if a == 10:
        return True
    if a == 172 and 16 <= b <= 31:
        return True
    if a == 192 and b == 168:
        return True
    return False


if __name__ == "__main__":
    print(is_private_ipv4("10.0.1.20"), is_private_ipv4("8.8.8.8"))
''',
            "Every production AWS app sits in a VPC whether you notice or not. Network layout decides blast radius, latency to managed services, and whether your database is one misclick from the public internet.",
            "A VPC is your private city map. Subnets are neighborhoods (public ones have a road to the Internet Gateway; private ones exit via NAT or stay dark). Security groups are stateful bouncers on doors; NACLs are stateless fences on neighborhood borders.",
            f"""### Core objects

- **CIDR**: address space (plan carefully; peering and TGW hate overlaps)
- **Subnet**: AZ-scoped slice; public if route to IGW
- **Route table**: where packets go next
- **IGW / NAT / TGW / VPN / Direct Connect**: exit and hybrid paths
- **Security group**: stateful allow rules on ENIs
- **NACL**: optional subnet-level stateless filter
- **VPC endpoints**: private path to AWS APIs (Gateway for S3/DynamoDB; Interface elsewhere)

### Reference layout

Public subnets: load balancers / bastion. Private: app. Isolated/data: databases with no NAT if possible, using endpoints.""",
            "Draw public/private/data subnets across 2 AZs. Explain SG vs NACL. Mention VPC endpoints to cut NAT cost and keep traffic private.",
            [
                "Sketch a 3-tier VPC across 2 AZs (easy)",
                "Choose SG rules for ALB → app → RDS (medium)",
                "Eliminate NAT for S3-heavy ETL using endpoints (hard)",
            ],
            [
                ("Amazon VPC docs", "https://docs.aws.amazon.com/vpc/latest/userguide/what-is-amazon-vpc.html"),
                ("VPC security best practices", "https://docs.aws.amazon.com/vpc/latest/userguide/vpc-security-best-practices.html"),
            ],
        ),
        (
            "EC2 Compute Essentials",
            "ec2-compute",
            "Launch, size, network, and operate EC2 instances with AMIs, storage, metadata, and capacity choices.",
            3,
            ["ec2", "compute", "aws"],
            "ec2",
            '''flowchart LR
    AMI[AMI] --> Launch[Launch instance]
    Launch --> EBS[EBS volume]
    Launch --> SG[Security group]
    Launch --> Role[Instance profile]
    Role --> Meta[IMDSv2]''',
            '''def right_size(cpu_util: float, mem_util: float) -> str:
    if cpu_util < 20 and mem_util < 30:
        return "downsize"
    if cpu_util > 75 or mem_util > 80:
        return "upsize-or-scale-out"
    return "hold"


if __name__ == "__main__":
    print(right_size(12, 25), right_size(82, 40))
''',
            "EC2 remains the escape hatch when containers or serverless do not fit — custom kernels, specialized hardware, sticky legacy apps. Knowing AMIs, instance families, and IMDS hardening is table stakes.",
            "An EC2 instance is a rented virtual machine with a boot disk image (AMI), a shape (instance type), a network card (ENI), and optionally an IAM badge (instance profile). You pay while it runs; stop/start and hibernate change the bill differently.",
            f"""### Key knobs

{table(
    ["Knob", "Notes"],
    [
        ["Instance family", "General, compute, memory, GPU, storage optimized"],
        ["AMI", "Hardened golden images beat snowflake hosts"],
        ["EBS", "gp3 default; snapshot backup story required"],
        ["Placement", "AZs, placement groups for HPC"],
        ["Purchasing", "On-Demand, Savings Plan, Spot"],
        ["Access", "SSM Session Manager over SSH bastions"],
    ]
)}

### IMDSv2

Require hop limit and session tokens so SSRF cannot trivially steal role credentials.""",
            "Compare EC2 vs ECS vs Lambda for a workload. Mention IMDS hardening and why SSM beats open SSH.",
            [
                "Pick an instance family for a memory-heavy JVM API (easy)",
                "Design a golden AMI pipeline outline (medium)",
                "Harden IMDS and remove SSH from a public subnet host (hard)",
            ],
            [
                ("Amazon EC2 docs", "https://docs.aws.amazon.com/ec2/"),
                ("IMDSv2", "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/configuring-instance-metadata-service.html"),
            ],
        ),
        (
            "S3 Object Storage",
            "s3-object-storage",
            "Use S3 for durable object storage: buckets, keys, classes, versioning, encryption, policies, and performance patterns.",
            4,
            ["s3", "storage", "aws"],
            "s3",
            '''flowchart LR
    App --> S3[(S3 Bucket)]
    S3 --> Std[Standard]
    S3 --> IA[IA / Glacier]
    CF[CloudFront] --> S3
    ETL[ETL] --> S3''',
            '''def object_key(tenant: str, day: str, filename: str) -> str:
    return f"tenants/{{tenant}}/dt={{day}}/{{filename}}".format(
        tenant=tenant, day=day, filename=filename
    )


if __name__ == "__main__":
    print(object_key("acme", "2026-11-26", "events.json.gz"))
''',
            "S3 is the default durable store for artifacts, data lakes, backups, and static assets. Most cloud architectures eventually put something important in a bucket — so key design, encryption, and public-access blocks matter.",
            "S3 is an infinite locker of blobs addressed by string keys. You do not resize disks; you PUT objects. Durability is extreme; availability and cost change with storage class. The dangerous part is policy: one bad public ACL and the internet has your data.",
            f"""### Essentials

- **Bucket**: namespace (global name) + Region
- **Key**: object path; design for listing and partitioning
- **Storage classes**: Standard, IA, Intelligent-Tiering, Glacier tiers
- **Versioning + MFA delete**: safety against overwrite/delete
- **Encryption**: SSE-S3, SSE-KMS, client-side
- **Block Public Access**: leave on unless there is a hard reason
- **Consistency**: strong read-after-write for new objects

### Performance

Parallelize large transfers (multipart). Avoid extremely hot single keys for high QPS metadata patterns; distribute prefixes.""",
            "Discuss durability vs backups (versioning). Explain when CloudFront sits in front. Call out public access block and bucket policies.",
            [
                "Design keys for a multi-tenant log lake (easy)",
                "Choose storage class lifecycle for 90-day analytics (medium)",
                "Write a bucket policy that allows only one VPC endpoint (hard)",
            ],
            [
                ("Amazon S3 User Guide", "https://docs.aws.amazon.com/s3/"),
                ("S3 security best practices", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/security-best-practices.html"),
            ],
        ),
        (
            "RDS Relational Databases on AWS",
            "rds-relational",
            "Operate managed relational databases with Multi-AZ, read replicas, parameter groups, backups, and connection patterns.",
            5,
            ["rds", "database", "aws"],
            "rds",
            '''flowchart LR
    App --> Primary[(RDS Primary)]
    Primary --> Standby[(Standby AZ)]
    Primary --> Replica[(Read replica)]
    App -. reads .-> Replica''',
            '''def connection_budget(max_conn: int, app_tasks: int, per_task: int) -> str:
    need = app_tasks * per_task
    if need > max_conn * 0.8:
        return "add PgBouncer/RDS Proxy or reduce pools"
    return "ok"


if __name__ == "__main__":
    print(connection_budget(100, 20, 10))
''',
            "Relational data still powers most products. RDS removes undifferentiated heavy lifting — patching, Multi-AZ failover plumbing — while leaving schema, queries, and capacity planning to you.",
            "RDS is a managed engine (Postgres, MySQL, etc.) with AWS holding the pager for the host. You still choose size, engine version, Multi-AZ, and backup windows. Failover is not magic zero-downtime for every client — connections drop and must retry.",
            f"""### Features that matter

{table(
    ["Feature", "Why"],
    [
        ["Multi-AZ", "Synchronous standby for HA"],
        ["Read replicas", "Scale reads; async lag"],
        ["Snapshots / PITR", "Backup and restore story"],
        ["Parameter groups", "Engine tuning knobs"],
        ["RDS Proxy", "Connection pooling for serverless/spiky"],
        ["Storage autoscaling", "Avoid free-storage incidents"],
    ]
)}

### Operations

Monitor free storage, CPU, IOPS, replica lag. Prefer private subnets + SG from app only. Encrypt with KMS.""",
            "Contrast RDS Multi-AZ vs read replicas. Mention connection storms with Lambda and how RDS Proxy helps.",
            [
                "Enable Multi-AZ and explain failover client behavior (easy)",
                "Design backup + restore drill for production Postgres (medium)",
                "Fix a connection-exhausted Lambda + RDS architecture (hard)",
            ],
            [
                ("Amazon RDS docs", "https://docs.aws.amazon.com/rds/"),
                ("RDS Proxy", "https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/rds-proxy.html"),
            ],
        ),
        (
            "DynamoDB Data Modeling and Operations",
            "dynamodb",
            "Model single-table access patterns, choose keys, understand capacity modes, GSIs, and common DynamoDB pitfalls.",
            6,
            ["dynamodb", "nosql", "aws"],
            "dynamodb",
            '''flowchart LR
    API --> Table[(DynamoDB table)]
    Table --> PK[Partition key]
    Table --> SK[Sort key]
    Table --> GSI[GSI]''',
            '''from collections import defaultdict

def pk(tenant: str, entity: str) -> str:
    return f"TENANT#{{tenant}}#{{entity}}".format(tenant=tenant, entity=entity)


def sk(prefix: str, id_: str) -> str:
    return f"{{prefix}}#{{id_}}".format(prefix=prefix, id_=id_)


if __name__ == "__main__":
    print(pk("acme", "ORDER"), sk("ORDER", "1001"))
''',
            "DynamoDB shines when access patterns are known and you need consistent single-digit millisecond reads at scale. Fighting it with relational habits causes scans, hot partitions, and pain.",
            "DynamoDB is a key-value / document store that rewards **query-first design**. You invent primary keys so that each product question becomes a Query on a partition, not a Scan across the world.",
            f"""### Concepts

- **Partition key + optional sort key**
- **Item** size limits; prefer narrow items + vertical partitioning when needed
- **On-demand vs provisioned** capacity; Auto Scaling; reserved capacity
- **GSI / LSI** for alternate patterns (GSI = new partition space)
- **TTL**, Streams, Transactions, PartiQL

### Modeling steps

1. List access patterns
2. Choose PK/SK templates
3. Add GSIs only for proven patterns
4. Avoid Scans in hot paths""",
            "Walk a single-table example (users, orders). Explain hot keys and GSIs. Contrast with RDS when joins dominate.",
            [
                "Model PK/SK for user → orders listing (easy)",
                "Add a GSI for orders-by-status (medium)",
                "Diagnose throttling on a hot partition (hard)",
            ],
            [
                ("DynamoDB Developer Guide", "https://docs.aws.amazon.com/dynamodb/"),
                ("AWS DynamoDB data modeling", "https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/bp-general-nosql-design.html"),
            ],
        ),
        (
            "AWS Lambda Serverless Compute",
            "lambda-serverless",
            "Build and operate Lambda functions: runtimes, packaging, concurrency, IAM, VPC access, and cold starts.",
            7,
            ["lambda", "serverless", "aws"],
            "lambda",
            '''flowchart LR
    Event[API / SQS / S3 / CRON] --> FN[Lambda]
    FN --> Out[AWS SDK calls]
    FN --> Log[CloudWatch Logs]''',
            '''def estimate_cold_start_impact(cold_rate: float, cold_ms: float, warm_ms: float) -> float:
    return cold_rate * cold_ms + (1 - cold_rate) * warm_ms


if __name__ == "__main__":
    print(round(estimate_cold_start_impact(0.05, 800, 40), 1))
''',
            "Lambda removes server babysitting for event-driven and spiky workloads. Used well it is cheap and scalable; used poorly it creates VPC cold-start traps, recursive retries, and monstrous IAM roles.",
            "Lambda is a function rental: upload code, attach a trigger, pay per invoke and GB-second. AWS scales concurrency for you — up to account and reserved limits. Cold starts are the price of elastic scale-to-zero.",
            f"""### Design points

{table(
    ["Topic", "Guidance"],
    [
        ["Package", "Zip or container image; keep lean"],
        ["IAM role", "Least privilege per function"],
        ["Concurrency", "Reserved / provisioned for critical paths"],
        ["VPC", "Only if you must reach private resources; use endpoints"],
        ["Idempotency", "Retries are normal — design for them"],
        ["Timeouts", "Set explicitly; align with upstream"],
    ]
)}

### Anti-patterns

Long-running CPU jobs, huge deployment packages with unused deps, synchronous fan-out chains without backpressure.""",
            "When to pick Lambda vs Fargate. Discuss cold starts, VPC ENI historically, and idempotent consumers.",
            [
                "Write a handler that processes SQS batches safely (easy)",
                "Reduce cold starts for a Python API (medium)",
                "Design recursive-S3-trigger prevention (hard)",
            ],
            [
                ("AWS Lambda Developer Guide", "https://docs.aws.amazon.com/lambda/"),
                ("Lambda best practices", "https://docs.aws.amazon.com/lambda/latest/dg/best-practices.html"),
            ],
        ),
        (
            "API Gateway for HTTP and WebSocket APIs",
            "api-gateway",
            "Front services with API Gateway: HTTP vs REST APIs, auth, throttling, stages, and integration patterns.",
            8,
            ["api-gateway", "http", "aws"],
            "apigw",
            '''flowchart LR
    Client --> APIGW[API Gateway]
    APIGW --> Auth[JWT / IAM / Lambda authorizer]
    APIGW --> Lambda
    APIGW --> HTTP[HTTP integration]''',
            '''def throttle_ok(tokens: float, cost: float = 1.0) -> tuple[bool, float]:
    if tokens >= cost:
        return True, tokens - cost
    return False, tokens


if __name__ == "__main__":
    ok, left = throttle_ok(3.0, 1.0)
    print(ok, left)
''',
            "API Gateway is the managed front door for serverless and HTTP backends: auth, throttling, API keys, WAF attachment, and stage deployments without owning a reverse proxy fleet.",
            "Treat API Gateway as a programmable receptionist: it checks credentials, enforces rate limits, then forwards the request to Lambda, a VPC link service, or an HTTP endpoint. You configure routes and integrations instead of patching nginx hosts.",
            f"""### Flavors

- **HTTP API**: cheaper, simpler, great for JWT/Lambda
- **REST API**: richer features (API keys, usage plans, request validation legacy surface)
- **WebSocket API**: stateful connections for push

### Cross-cutting

Custom domains, TLS certs via ACM, stages/stages variables, access logs to CloudWatch/Firehose, AWS WAF web ACLs, throttling burst/rate.""",
            "Compare HTTP API vs ALB. Explain authorizers and stage-based deploy. Mention throttling as first-line abuse control.",
            [
                "Map routes for a CRUD Lambda API (easy)",
                "Add JWT auth and per-route throttling (medium)",
                "Design canary release with stages/weighted targets (hard)",
            ],
            [
                ("API Gateway Developer Guide", "https://docs.aws.amazon.com/apigateway/"),
                ("HTTP vs REST APIs", "https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-vs-rest.html"),
            ],
        ),
        (
            "ECS, EKS, and Fargate Containers on AWS",
            "ecs-eks-fargate",
            "Choose and operate container platforms: ECS vs EKS vs Fargate, tasks/pods, networking, and rollout basics.",
            9,
            ["ecs", "eks", "fargate", "containers"],
            "containers-aws",
            '''flowchart TB
    Image[Container image] --> ECS[ECS service]
    Image --> EKS[EKS Deployment]
    ECS --> Fargate
    EKS --> Fargate
    ECS --> EC2cap[EC2 capacity]
    EKS --> Nodes[Managed node groups]''',
            '''def pick_platform(needs_k8s_api: bool, wants_minimal_ops: bool) -> str:
    if needs_k8s_api:
        return "EKS" + (" on Fargate" if wants_minimal_ops else " with nodes")
    return "ECS on Fargate" if wants_minimal_ops else "ECS on EC2"


if __name__ == "__main__":
    print(pick_platform(False, True))
    print(pick_platform(True, False))
''',
            "Containers package apps consistently; AWS offers multiple control planes. Picking ECS vs EKS vs raw EC2 is an ops-and-ecosystem decision as much as a technical one.",
            "ECS is AWS's opinionated orchestrator — tasks and services with less moving surface. EKS runs Kubernetes — portable and ecosystem-rich, but you operate cluster concepts. Fargate is the serverless capacity layer under either so you skip node patching.",
            f"""### Comparison

{table(
    ["Dimension", "ECS", "EKS"],
    [
        ["Learning curve", "Lower", "Higher"],
        ["Portability", "AWS-centric", "Kubernetes-portable"],
        ["Ecosystem", "AWS native", "Huge CNCF surface"],
        ["Ops burden", "Lower", "Control plane + addons"],
    ]
)}

### Shared concerns

Task/pod IAM (IRSA on EKS), ALB Ingress/Service, image scanning, Circuit breaker / deployments, logging to CloudWatch or OpenSearch.""",
            "Ask clarifying questions: need K8s API? multi-cloud? team skills? Recommend Fargate unless you need node-level control.",
            [
                "Choose ECS vs EKS for a 3-service API (easy)",
                "Outline blue/green on ECS with CodeDeploy (medium)",
                "Design IRSA roles for two EKS microservices (hard)",
            ],
            [
                ("Amazon ECS", "https://docs.aws.amazon.com/ecs/"),
                ("Amazon EKS", "https://docs.aws.amazon.com/eks/"),
                ("AWS Fargate", "https://docs.aws.amazon.com/AmazonECS/latest/userguide/what-is-fargate.html"),
            ],
        ),
        (
            "CloudFront Content Delivery",
            "cloudfront-cdn",
            "Accelerate and protect origins with CloudFront: behaviors, cache keys, TLS, OAC/OAI, and invalidations.",
            10,
            ["cloudfront", "cdn", "aws"],
            "cloudfront",
            '''flowchart LR
    User --> CF[CloudFront]
    CF --> S3[(S3 origin)]
    CF --> ALB[ALB origin]
    CF --> WAF[WAF]''',
            '''def cache_hit_ratio(hits: int, misses: int) -> float:
    total = hits + misses
    return 0.0 if total == 0 else hits / total


if __name__ == "__main__":
    print(round(cache_hit_ratio(900, 100), 3))
''',
            "CloudFront cuts latency and origin load for static and cacheable dynamic content, and is a natural place to attach WAF and TLS at the edge.",
            "A CDN is a fleet of neighborhood caches. CloudFront sits between users and your origin (S3 or ALB). Cache behaviors decide what is cached, for how long, and which headers/cookies form the cache key.",
            f"""### Practical knobs

- **Origins + origin groups** for failover
- **Behaviors**: path patterns, TTLs, allowed methods
- **Cache policy / origin request policy**: modern replacements for legacy forwarded settings
- **OAC** to keep S3 private
- **Invalidations**: expensive emergency flush; prefer versioned object names
- **TLS**: ACM certificates on alternate domains""",
            "Explain cache key mistakes (forwarding all headers). Describe OAC for private S3. Mention WAF at the edge.",
            [
                "Front an S3 static site with CloudFront + OAC (easy)",
                "Design cache policies for `/static/*` vs `/api/*` (medium)",
                "Plan origin failover between two Regions (hard)",
            ],
            [
                ("Amazon CloudFront", "https://docs.aws.amazon.com/cloudfront/"),
                ("Cache policies", "https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/controlling-the-cache-key.html"),
            ],
        ),
        (
            "Route 53 DNS and Traffic Routing",
            "route53-dns",
            "Use Route 53 hosted zones, routing policies, health checks, and DNS patterns for HA and multi-region.",
            11,
            ["route53", "dns", "aws"],
            "route53",
            '''flowchart LR
    User --> R53[Route 53]
    R53 --> Simple[Simple]
    R53 --> WRR[Weighted]
    R53 --> Failover
    R53 --> Latency
    R53 --> Geo''',
            '''def weighted_pick(weights: dict[str, int], token: int) -> str:
    total = sum(weights.values())
    token = token % total
    acc = 0
    for name, w in weights.items():
        acc += w
        if token < acc:
            return name
    return next(iter(weights))


if __name__ == "__main__":
    print(weighted_pick({"blue": 9, "green": 1}, 3))
''',
            "DNS is part of your availability story. Route 53 provides authoritative DNS plus health-aware routing so you can shift traffic across targets and Regions.",
            "Route 53 is both a phone book and a traffic cop. Hosted zones hold records; routing policies decide which answer to return based on weights, latency, geography, or failover health.",
            f"""### Record and policy types

{table(
    ["Policy", "Use"],
    [
        ["Simple", "Single target"],
        ["Weighted", "Canary / gradual migrate"],
        ["Failover", "Primary/secondary DR"],
        ["Latency", "Multi-Region nearest"],
        ["Geolocation / geoproximity", "Compliance or regional UX"],
        ["Multi-value", "Simple HA with health checks"],
    ]
)}

### Alias records

Alias to ALB, CloudFront, S3 website — no extra DNS charge for queries to AWS aliases in common patterns; integrates with AWS targets cleanly.""",
            "Design DNS failover with health checks. Contrast CNAME vs alias. Discuss TTL vs failover speed trade-off.",
            [
                "Create a weighted canary DNS plan 95/5 (easy)",
                "Design latency-based Multi-Region DNS (medium)",
                "Explain split-horizon DNS for private + public (hard)",
            ],
            [
                ("Route 53 Developer Guide", "https://docs.aws.amazon.com/route53/"),
                ("Routing policies", "https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/routing-policy.html"),
            ],
        ),
        (
            "SQS, SNS, and EventBridge Messaging",
            "sqs-sns-eventbridge",
            "Decouple systems with queues, pub/sub topics, and event buses — patterns, retries, DLQs, and ordering.",
            12,
            ["sqs", "sns", "eventbridge", "messaging"],
            "messaging",
            '''flowchart LR
    Producer --> EB[EventBridge]
    EB --> SNS
    EB --> SQS
    SNS --> Email
    SNS --> SQS2[SQS]
    SQS --> Worker
    SQS --> DLQ[DLQ]''',
            '''def should_retry(attempt: int, max_attempts: int, http_status: int) -> bool:
    if attempt >= max_attempts:
        return False
    return http_status >= 500 or http_status == 429


if __name__ == "__main__":
    print(should_retry(1, 5, 503), should_retry(5, 5, 503))
''',
            "Asynchronous messaging absorbs spikes, isolates failures, and enables fan-out. AWS offers complementary primitives: SQS (queue), SNS (fan-out), EventBridge (event routing/bus).",
            "SQS is a line at the coffee shop — workers pull next order. SNS is a megaphone — many subscribers hear the same shout. EventBridge is a smart switchboard — route events by rules to many targets without hard-wiring producers to consumers.",
            f"""### Comparison

{table(
    ["Service", "Model", "Sweet spot"],
    [
        ["SQS", "Pull queue", "Work distribution, buffering"],
        ["SNS", "Push pub/sub", "Fan-out notifications"],
        ["EventBridge", "Event bus + rules", "SaaS/AWS events, archive/replay"],
    ]
)}

### Reliability patterns

Visibility timeout, DLQ, partial batch failure (Lambda), FIFO for strict order + dedupe, exponential backoff, idempotent consumers.""",
            "Pick SQS vs SNS vs EventBridge for a scenario. Explain DLQ and at-least-once delivery implications.",
            [
                "Design order-placed fan-out with SNS→SQS (easy)",
                "Add DLQ and redrive policy for a worker (medium)",
                "Use EventBridge archive/replay for a bad deploy recovery (hard)",
            ],
            [
                ("Amazon SQS", "https://docs.aws.amazon.com/sqs/"),
                ("Amazon SNS", "https://docs.aws.amazon.com/sns/"),
                ("Amazon EventBridge", "https://docs.aws.amazon.com/eventbridge/"),
            ],
        ),
        (
            "CloudWatch Observability",
            "cloudwatch-observability",
            "Instrument AWS workloads with CloudWatch metrics, logs, alarms, dashboards, and X-Ray tracing basics.",
            13,
            ["cloudwatch", "observability", "aws"],
            "cloudwatch",
            '''flowchart LR
    App --> Metrics
    App --> Logs
    App --> Traces[X-Ray]
    Metrics --> Alarm
    Alarm --> SNS
    Logs --> Insights[Logs Insights]''',
            '''def alarm_state(value: float, threshold: float, op: str = "gt") -> str:
    if op == "gt":
        return "ALARM" if value > threshold else "OK"
    return "ALARM" if value < threshold else "OK"


if __name__ == "__main__":
    print(alarm_state(99.2, 99.0), alarm_state(98.5, 99.0))
''',
            "You cannot operate what you cannot see. CloudWatch is the default AWS telemetry plane — metrics, logs, alarms — and pairs with X-Ray for traces.",
            "Observability is three pillars: metrics (numbers over time), logs (event detail), traces (request journeys). CloudWatch collects the first two natively; alarms turn numbers into pages.",
            f"""### Practical toolkit

- **Namespace / metric / dimension** design for actionable alarms
- **Logs Insights** queries for incident triage
- **Alarms** with anomaly detection or static thresholds
- **Dashboards** for service golden signals
- **Contributor Insights / Evidently** (advanced)
- **X-Ray / OpenTelemetry** for latency breakdowns

### Golden signals

Latency, traffic, errors, saturation — alarm on user-visible symptoms, not only host CPU.""",
            "Define golden signals for an API. Write a sensible alarm (not too noisy). Mention structured JSON logs.",
            [
                "Propose alarms for ALB 5xx and p99 latency (easy)",
                "Write a Logs Insights query for error spikes (medium)",
                "Design a dashboard + runbook for checkout service (hard)",
            ],
            [
                ("Amazon CloudWatch", "https://docs.aws.amazon.com/cloudwatch/"),
                ("AWS X-Ray", "https://docs.aws.amazon.com/xray/"),
            ],
        ),
        (
            "Secrets Manager and Secure Configuration",
            "secrets-manager",
            "Store, rotate, and consume secrets with AWS Secrets Manager, Parameter Store contrasts, and app integration patterns.",
            14,
            ["secrets", "security", "aws"],
            "secrets",
            '''flowchart LR
    App --> SM[Secrets Manager]
    SM --> KMS[KMS]
    Rotate[Rotation Lambda] --> SM
    App --> IAM''',
            '''def redact(secret: str, visible: int = 2) -> str:
    if len(secret) <= visible * 2:
        return "***"
    return secret[:visible] + "***" + secret[-visible:]


if __name__ == "__main__":
    print(redact("super-secret-password"))
''',
            "Hard-coded credentials in images and Git history are still a top breach class. Secrets Manager centralizes storage, access audit, and rotation.",
            "A secret is a password that wants a lifecycle: create, grant, rotate, revoke. Secrets Manager holds encrypted values in KMS, hands them to callers who pass IAM, and can rotate engines like RDS passwords automatically.",
            f"""### Secrets Manager vs SSM Parameter Store

{table(
    ["Need", "Prefer"],
    [
        ["Automatic rotation", "Secrets Manager"],
        ["Simple config / non-secret params", "SSM Parameter Store"],
        ["Cross-account fine-grained secrets", "Secrets Manager"],
        ["Cheap hierarchical config", "Parameter Store"],
    ]
)}

### App patterns

Fetch at startup or with short TTL cache; never log secret values; use IAM roles not embedded keys; prefer rotation over year-old static passwords.""",
            "Contrast Secrets Manager vs env vars in ECS task defs. Describe rotation for RDS. Mention audit via CloudTrail.",
            [
                "Replace a hardcoded DB password with Secrets Manager (easy)",
                "Design rotation for a third-party API key (medium)",
                "Cross-account secret share with least privilege (hard)",
            ],
            [
                ("AWS Secrets Manager", "https://docs.aws.amazon.com/secretsmanager/"),
                ("SSM Parameter Store", "https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-parameter-store.html"),
            ],
        ),
        (
            "Elastic Load Balancing and Auto Scaling",
            "elb-asg",
            "Distribute traffic with ALB/NLB/GLB and scale EC2/ECS capacity with Auto Scaling policies and health checks.",
            15,
            ["elb", "asg", "aws", "scaling"],
            "elb-asg",
            '''flowchart LR
    Users --> ALB
    ALB --> ASG[Auto Scaling Group]
    ASG --> EC2a[EC2 AZ-a]
    ASG --> EC2b[EC2 AZ-b]
    ALB --> Health[Health checks]''',
            '''def desired_capacity(current_cpu: float, target_cpu: float, current: int) -> int:
    if current_cpu <= 0:
        return current
    raw = current * (current_cpu / target_cpu)
    return max(1, round(raw))


if __name__ == "__main__":
    print(desired_capacity(80, 50, 4))
''',
            "Load balancers and autoscaling turn a handful of instances into an elastic service that survives AZ loss and traffic spikes — when health checks and policies are honest.",
            "An ELB is a traffic sprinkler; an Auto Scaling Group is a rubber band of identical instances. Health checks tell the sprinkler who is healthy; scaling policies tell the rubber band when to stretch or shrink.",
            f"""### Load balancer types

{table(
    ["Type", "Layer", "Use"],
    [
        ["ALB", "L7 HTTP", "Path/host routing, microservices"],
        ["NLB", "L4 TCP/UDP", "Ultra performance, static IPs"],
        ["GWLB", "L3/L4 appliances", "Inline security appliances"],
        ["CLB", "Legacy", "Avoid for new designs"],
    ]
)}

### Scaling

Target tracking (CPU, ALB req/target, custom), step scaling, scheduled scaling. Cool-downs and warm pools reduce thrash. For ECS/EKS prefer service autoscaling / HPA analogous concepts.""",
            "Explain ALB vs NLB. Tie health checks to ASG replacement. Discuss connection draining during deploys.",
            [
                "Design ALB target groups for blue/green (easy)",
                "Pick scaling metrics for a CPU-bound API (medium)",
                "Survive AZ loss with ASG + Multi-AZ ALB (hard)",
            ],
            [
                ("Elastic Load Balancing", "https://docs.aws.amazon.com/elasticloadbalancing/"),
                ("EC2 Auto Scaling", "https://docs.aws.amazon.com/autoscaling/"),
            ],
        ),
        (
            "CloudFormation and AWS CDK",
            "cloudformation-cdk",
            "Define AWS infrastructure as code with CloudFormation templates and the AWS CDK — stacks, changesets, and constructs.",
            16,
            ["cloudformation", "cdk", "iac", "aws"],
            "cfn-cdk",
            '''flowchart LR
    Code[CDK / Template] --> Synth[CloudFormation template]
    Synth --> ChangeSet
    ChangeSet --> Stack[CFN Stack]
    Stack --> Resources''',
            '''def stack_name(app: str, env: str) -> str:
    return f"{{app}}-{{env}}".format(app=app, env=env)


if __name__ == "__main__":
    print(stack_name("codecraft", "prod"))
''',
            "ClickOps does not scale and cannot be reviewed. CloudFormation is AWS's native IaC engine; CDK generates CloudFormation from real programming languages with higher-level constructs.",
            "Infrastructure as code means Git is the source of truth for cloud resources. CloudFormation applies declarative templates as stacks. CDK lets you write TypeScript/Python that synthesizes those templates — with reusable constructs instead of endless YAML copy-paste.",
            f"""### Concepts

- **Stack**: unit of deployment
- **Change set**: preview before apply
- **Drift detection**: reality vs template
- **Nested stacks / StackSets**: scale organization-wide
- **CDK constructs**: L1 (CFN resources), L2 (opinionated), L3 (patterns)
- **Aspects / checks**: policy as code hooks

### Workflow

Synth → diff → deploy → (optional) rollback. Keep secrets out of templates; use dynamic references to Secrets Manager/SSM.""",
            "Contrast Terraform vs CloudFormation/CDK. Explain change sets and drift. Show when L2 constructs speed safe defaults.",
            [
                "Write a tiny template/stack for S3 + block public access (easy)",
                "Sketch CDK app structure for VPC + ECS (medium)",
                "Plan multi-account StackSets for baseline security (hard)",
            ],
            [
                ("AWS CloudFormation", "https://docs.aws.amazon.com/cloudformation/"),
                ("AWS CDK", "https://docs.aws.amazon.com/cdk/"),
            ],
        ),
    ]

    for title, slug, summary, order, tags, code_tag, diagram, code, why, intuition, core_extra, interview, practice, further in lessons:
        # Fix code blocks that accidentally escaped braces for format - regenerate properly
        L(
            title,
            slug,
            summary,
            order,
            why,
            intuition,
            core_extra,
            mermaid(diagram)
            + "\n\n### Dry-run\n\nWalk the diagram left to right for a typical request or change; name failure points and IAM touchpoints.",
            code_block("python", code.replace("{{", "{").replace("}}", "}")),
            table(
                ["Concern", "What to measure"],
                [
                    ["Change risk", "Blast radius of stack/service update"],
                    ["Scale", "Saturation signals and throttles"],
                    ["Cost", "Idle capacity and egress"],
                ],
            ),
            bullets(
                [
                    "Prefer least privilege and private networking defaults.",
                    "Automate with IaC; review diffs like application code.",
                    "Design for retries and Multi-AZ from day one.",
                    "Emit metrics and structured logs on the hot path.",
                ]
            ),
            bullets(
                [
                    "ClickOps exceptions that never return to Git.",
                    "Over-broad IAM for 'temporary' debugging.",
                    "Single-AZ 'temporary' production.",
                    "Ignoring data transfer and idle resources.",
                ]
            ),
            interview,
            numbered(practice),
            bullets(
                [
                    f"Know where {code_tag} sits in a reference architecture.",
                    "State failure modes and observability hooks.",
                    "Tie decisions to cost and security trade-offs.",
                    "Prefer managed services until requirements force otherwise.",
                ]
            ),
            reading(further),
            module=m,
            filename=f"{order:02d}-{slug}.mdx",
            tags=tags,
            prerequisites=["cloud-and-aws-overview"],
            duration=40,
        )


def terraform_mod():
    m = "03-terraform"
    items = [
        (
            1,
            "Terraform Fundamentals and Workflow",
            "terraform-fundamentals",
            "providers",
            '''flowchart LR
    Write[Write HCL] --> Init
    Init --> Plan
    Plan --> Apply
    Apply --> State[(State)]''',
            '''def resource_address(resource_type: str, name: str, index: int | None = None) -> str:
    base = f"{{resource_type}}.{{name}}".format(resource_type=resource_type, name=name)
    return base if index is None else f"{{base}}[{{index}}]".format(base=base, index=index)


if __name__ == "__main__":
    print(resource_address("aws_s3_bucket", "assets"))
''',
            "Terraform is the multi-cloud lingua franca for declarative infrastructure. The write → plan → apply loop plus state is the core mental model every DevOps engineer must own.",
            "HCL describes the desired world. Terraform compares desire to state, plans a graph of creates/updates/deletes, then applies. Providers (AWS, etc.) do the API talking.",
            """### Core objects

- **Provider**: cloud/API plugin
- **Resource**: managed object
- **Data source**: read-only lookup
- **Variable / output / local**: parameterization
- **State**: mapping of resources to real IDs

### Workflow commands

`init`, `fmt`, `validate`, `plan`, `apply`, `destroy`. Always review plan before apply in shared environments.""",
        ),
        (
            2,
            "Terraform State and Remote Backends",
            "terraform-state-backends",
            "state",
            '''flowchart LR
    Dev1 --> Lock[(State lock)]
    Dev2 --> Lock
    Lock --> S3[(S3 backend)]
    S3 --> DDB[DynamoDB lock table]''',
            '''def state_key(env: str, stack: str) -> str:
    return f"env:/{{env}}/{{stack}}/terraform.tfstate".format(env=env, stack=stack)


if __name__ == "__main__":
    print(state_key("prod", "networking"))
''',
            "State is Terraform's memory. Local state files do not work for teams; remote backends with locking prevent corruption and enable CI.",
            "Without state, Terraform cannot know which real bucket maps to `aws_s3_bucket.assets`. Remote state in S3 + DynamoDB locks (or Terraform Cloud) makes collaboration safe.",
            """### Rules

- Never hand-edit state; use `state mv/rm` carefully
- Encrypt state at rest; restrict IAM
- Separate state per environment/stack to limit blast radius
- Sensible `lifecycle` and `-target` only as break-glass""",
        ),
        (
            3,
            "Modules and Composition",
            "terraform-modules",
            "modules",
            '''flowchart TB
    Root[Root module] --> Net[Network module]
    Root --> App[App module]
    App --> Alb[ALB module]
    App --> Ecs[ECS module]''',
            '''def module_source(registry: str, name: str, version: str) -> str:
    return f"{{registry}}/{{name}}?version={{version}}".format(
        registry=registry, name=name, version=version
    )


if __name__ == "__main__":
    print(module_source("hashicorp", "consul/aws", "1.0.0"))
''',
            "Modules package reusable infrastructure with a clear interface — the same impulse as functions in application code.",
            "A module is a folder of Terraform with input variables and outputs. Root modules compose child modules into environments. Version pin module sources like you pin libraries.",
            """### Design tips

- Small modules with sharp purpose beat mega-modules
- Expose only needed variables; sane defaults
- Output IDs other stacks need; avoid leaking everything
- Document examples; smoke-test in CI with `plan`""",
        ),
        (
            4,
            "Lifecycle, Provisioners, and Dependencies",
            "terraform-lifecycle-deps",
            "lifecycle",
            '''flowchart LR
    A[aws_vpc] --> B[aws_subnet]
    B --> C[aws_instance]
    C --> Meta[lifecycle blocks]''',
            '''def needs_replace(old_type: str, new_type: str) -> bool:
    return old_type != new_type


if __name__ == "__main__":
    print(needs_replace("t3.micro", "t3.small"))
''',
            "Understanding create-before-destroy, ignore_changes, replace triggers, and explicit depends_on prevents scary production applies.",
            "Terraform builds a dependency graph from references. Sometimes you need lifecycle rules — keep a resource from destroying first, or ignore drift on tags managed elsewhere. Provisioners are a last resort.",
            """### Prefer

- Cloud-init / user_data / SSM over `remote-exec`
- Explicit `depends_on` only when references are insufficient
- `create_before_destroy` for zero-ish downtime replacements where names allow""",
        ),
        (
            5,
            "Workspaces, Environments, and CI for Terraform",
            "terraform-workspaces-ci",
            "workspaces",
            '''flowchart LR
    PR --> Plan[terraform plan]
    Plan --> Review
    Review --> Apply[terraform apply]
    Apply --> Dev
    Apply --> Prod''',
            '''def backend_config(env: str) -> dict[str, str]:
    return {"bucket": "acme-tf-state", "key": f"{{env}}/network.tfstate".format(env=env), "region": "ap-south-1"}


if __name__ == "__main__":
    print(backend_config("staging"))
''',
            "Promoting infrastructure through environments with CI plans and gated applies is how teams avoid cowboy changes in production.",
            "Workspaces can isolate state, but many teams prefer separate directories/backends per env for clarity. CI runs `plan` on PR and `apply` on merge to main with OIDC credentials.",
            """### CI checklist

- `fmt` + `validate` + `tflint` / checkov
- Plan artifacts posted to PR
- Manual approval for production apply
- No long-lived cloud keys — use OIDC""",
        ),
    ]
    for order, title, slug, tag, diagram, code, why, intuition, core in items:
        L(
            title,
            slug,
            f"Terraform in depth: {tag} — practical patterns for real AWS estates.",
            order,
            why,
            intuition,
            core,
            mermaid(diagram) + "\n\n### Dry-run\n\nNarrate init → plan → apply and what lands in state for a small VPC change.",
            code_block("python", code.replace("{{", "{").replace("}}", "}")),
            table(
                ["Operation", "Risk if wrong"],
                [
                    ["apply without plan review", "Unexpected destroys"],
                    ["shared unlocked state", "Corruption / races"],
                    ["giant blast-radius state", "Long locks / scary diffs"],
                ],
            ),
            bullets(
                [
                    "Remote state + locking is mandatory for teams.",
                    "Module boundaries mirror ownership boundaries.",
                    "Plan in CI; apply with gates.",
                    "Prefer declarative cloud APIs over provisioners.",
                ]
            ),
            bullets(
                [
                    "Committing state files with secrets.",
                    "Using `-auto-approve` on production casually.",
                    "One monolith state for an entire company.",
                    "Unpinned module versions.",
                ]
            ),
            f"Explain state, backends, and a safe CI workflow. Be ready to discuss {tag} trade-offs.",
            numbered(
                [
                    f"Demonstrate a minimal example focused on {tag} (easy)",
                    "Refactor duplicated resources into a module (medium)",
                    "Design env isolation + CI gates for prod (hard)",
                ]
            ),
            bullets(
                [
                    "HCL + providers + state define Terraform.",
                    "Plan is the contract with reviewers.",
                    "Split state; pin versions; lock backends.",
                    "Treat IaC like production code.",
                ]
            ),
            reading(
                [
                    ("Terraform docs", "https://developer.hashicorp.com/terraform/docs"),
                    ("AWS Provider", "https://registry.terraform.io/providers/hashicorp/aws/latest/docs"),
                ]
            ),
            module=m,
            filename=f"{order:02d}-{slug}.mdx",
            tags=["terraform", "iac", tag],
            prerequisites=["cloudformation-cdk"],
            duration=40,
        )


def docker_mod():
    m = "04-docker"
    items = [
        (
            1,
            "Images, Layers, and the Docker Mental Model",
            "docker-images-layers",
            '''flowchart LR
    Base[Base layer] --> Deps[Deps layer]
    Deps --> App[App layer]
    App --> Image[Image]
    Image --> Container''',
            '''def layer_cache_hit(changed_files: list[str], dockerfile_steps: list[str]) -> str:
    if any(f.endswith("requirements.txt") for f in changed_files):
        return "invalidate from deps step"
    if any(f.endswith(".py") for f in changed_files):
        return "invalidate from COPY app step"
    return "mostly cached"


if __name__ == "__main__":
    print(layer_cache_hit(["app/main.py"], ["FROM", "COPY req", "RUN pip", "COPY app"]))
''',
            "Containers ship the same filesystem snapshot everywhere. Understanding images vs containers and layer caching unlocks fast builds and smaller artifacts.",
            "An image is a cake of immutable layers; a container is a running slice with a thin writable layer on top. Rebuilds reuse unchanged layers — order your Dockerfile so volatile app code is copied last.",
            """### Concepts

- Image vs container vs registry
- Union filesystem layers
- Content-addressed digests
- `ENTRYPOINT` vs `CMD`
- Namespaces and cgroups (isolation + limits)""",
        ),
        (
            2,
            "Dockerfile Best Practices",
            "dockerfile-best-practices",
            '''flowchart TB
    Pin[Pin base digest] --> User[Non-root USER]
    User --> Health[HEALTHCHECK]
    Health --> Scan[Image scan]
    Scan --> Push[Push digest]''',
            '''def should_run_as_root(reason: str | None) -> bool:
    return False


if __name__ == "__main__":
    print(should_run_as_root(None))
''',
            "A sloppy Dockerfile becomes a supply-chain and performance problem. Pin bases, drop privileges, and keep attack surface small.",
            "Treat Dockerfiles as production code: reproducible bases, minimal packages, non-root users, and no secrets in layers.",
            """### Checklist

- Pin versions/digests
- Multi-stage when building binaries
- `.dockerignore` to avoid leaking context
- One process per container (generally)
- Read-only root filesystem where feasible""",
        ),
        (
            3,
            "Multi-stage Builds",
            "docker-multi-stage",
            '''flowchart LR
    Build[build stage] --> Artifact[binary/static]
    Artifact --> Runtime[runtime stage]
    Runtime --> Small[Small final image]''',
            '''def final_image_hint(has_compiler: bool, has_app_only: bool) -> str:
    if has_compiler and has_app_only:
        return "you probably forgot multi-stage"
    if not has_compiler and has_app_only:
        return "looks like a slim runtime image"
    return "review contents"


if __name__ == "__main__":
    print(final_image_hint(False, True))
''',
            "Multi-stage builds separate compile-time toolchains from runtime images, cutting size and vulnerabilities dramatically.",
            "Use a fat builder stage with compilers and tests, then copy only the artifact into a slim runtime base (distroless/alpine/slim).",
            """### Pattern

`FROM sdk AS build` → build → `FROM runtime` → `COPY --from=build` artifact → set user → entrypoint.""",
        ),
        (
            4,
            "Docker Compose for Local Systems",
            "docker-compose",
            '''flowchart LR
    Compose[compose.yaml] --> Web
    Compose --> API
    Compose --> DB[(Postgres)]
    Compose --> Cache[(Redis)]''',
            '''def service_url(service: str, port: int) -> str:
    return f"http://{{service}}:{{port}}".format(service=service, port=port)


if __name__ == "__main__":
    print(service_url("api", 8000))
''',
            "Compose orchestrates multi-container apps on a single machine for local dev and demos — networks, volumes, and dependency order included.",
            "A compose file lists services, networks, and volumes. DNS names equal service names on the default network. It is not a substitute for Kubernetes in production, but it is unmatched for developer onboarding.",
            """### Tips

- Bind-mount source for hot reload; use named volumes for DB data
- `depends_on` ≠ readiness; use healthchecks
- Profiles for optional observability sidecars
- Keep prod manifests separate (K8s/ECS)""",
        ),
        (
            5,
            "Container Security and Operations",
            "docker-security-ops",
            '''flowchart LR
    Build --> Scan[CVE scan]
    Scan --> Sign[Sign image]
    Sign --> Registry
    Registry --> Admit[Admission policy]
    Admit --> Run[Runtime limits]''',
            '''def risk_flags(runs_as_root: bool, privileged: bool, latest_tag: bool) -> list[str]:
    flags = []
    if runs_as_root:
        flags.append("root")
    if privileged:
        flags.append("privileged")
    if latest_tag:
        flags.append("floating-tag")
    return flags


if __name__ == "__main__":
    print(risk_flags(True, False, True))
''',
            "Images are supply chain artifacts. Scanning, signing, resource limits, and avoiding privileged mode keep clusters safer.",
            "Security is a pipeline: trustworthy bases → scanned builds → signed digests → restricted runtime. Operations add resource requests/limits, logging drivers, and restart policies.",
            """### Runtime hardening

- No privileged containers by default
- Drop Linux capabilities
- Read-only root FS + tmp volumes
- Pin digests in deploy manifests
- Network policies in Kubernetes (later module)""",
        ),
    ]
    for order, title, slug, diagram, code, why, intuition, core in items:
        L(
            title,
            slug,
            f"{title} — practical Docker skills for Cloud/DevOps engineers.",
            order,
            why,
            intuition,
            core,
            mermaid(diagram) + "\n\n### Dry-run\n\nTrace a build and run for a simple Python API; note which layers rebuild when app code changes.",
            code_block("python", code.replace("{{", "{").replace("}}", "}")),
            table(
                ["Choice", "Trade-off"],
                [
                    ["Fat image", "Easy debug / more CVEs"],
                    ["Slim/distroless", "Safer / harder shell debug"],
                    ["Bind mounts", "Fast dev / not for prod"],
                ],
            ),
            bullets(
                [
                    "Order Dockerfile for cache hits.",
                    "Never bake secrets into layers.",
                    "Pin digests for production deploys.",
                    "One concern per container when practical.",
                ]
            ),
            bullets(
                [
                    "Using `:latest` in production.",
                    "Running as root unnecessarily.",
                    "Huge build context without `.dockerignore`.",
                    "Assuming Compose equals production orchestration.",
                ]
            ),
            "Explain images vs containers, layer caching, and one hardening control. Contrast Compose vs Kubernetes.",
            numbered(
                [
                    "Write a minimal Dockerfile for a Flask/FastAPI app (easy)",
                    "Convert it to multi-stage (medium)",
                    "Add compose with API + Postgres healthchecks (hard)",
                ]
            ),
            bullets(
                [
                    "Images = layers; containers = running instances.",
                    "Multi-stage shrinks runtime.",
                    "Compose for local; orchestrators for prod.",
                    "Scan, sign, limit, non-root.",
                ]
            ),
            reading(
                [
                    ("Docker docs", "https://docs.docker.com/"),
                    ("Dockerfile best practices", "https://docs.docker.com/develop/develop-images/dockerfile_best-practices/"),
                ]
            ),
            module=m,
            filename=f"{order:02d}-{slug}.mdx",
            tags=["docker", "containers"],
            prerequisites=["cloud-and-aws-overview"],
            duration=35,
        )


def k8s_mod():
    m = "05-kubernetes"
    items = [
        (1, "Pods and Workload Primitives", "k8s-pods-workloads", "Pod", "smallest deployable unit; usually 1 app container + optional sidecars"),
        (2, "Deployments and Rollout Strategies", "k8s-deployments-rollouts", "Deployment", "declarative ReplicaSets with rolling updates and rollbacks"),
        (3, "Services and Cluster Networking", "k8s-services-networking", "Service", "stable virtual IP / DNS to pods selected by labels"),
        (4, "Ingress and North-South Traffic", "k8s-ingress", "Ingress", "HTTP routing from outside to Services via controllers"),
        (5, "ConfigMaps, Secrets, and Configuration", "k8s-config-secrets", "Config", "inject config and secrets without rebuilding images"),
        (6, "Horizontal Pod Autoscaler", "k8s-hpa", "HPA", "scale replicas from CPU/memory/custom metrics"),
        (7, "Helm Charts and Packaging", "k8s-helm", "Helm", "package Kubernetes apps with templates and releases"),
    ]
    for order, title, slug, focus, blurb in items:
        L(
            title,
            slug,
            f"Kubernetes {focus}: {blurb}.",
            order,
            f"Kubernetes is the portable control plane for containers. Understanding {focus} is required to ship and operate services on EKS or any CNCF cluster.",
            f"Picture a busy harbor: pods are ships, deployments are shipping schedules, services are berth numbers that stay stable as ships swap, and Ingress is the harbor entrance. {focus} is the piece we zoom into here — {blurb}.",
            f"""### Focus: {focus}

{blurb.capitalize()}.

### Surrounding objects

{table(
    ["Object", "Role"],
    [
        ["Pod", "Running containers + volumes + identity"],
        ["Deployment", "Desired replica count + rollout"],
        ["Service", "Stable networking to pod set"],
        ["Ingress", "L7 entry"],
        ["ConfigMap/Secret", "Configuration"],
        ["HPA", "Autoscaling replicas"],
        ["Helm Release", "Versioned install of a chart"],
    ]
)}

### Hands-on mindset

Declarative YAML in Git; controllers reconcile reality; labels/selectors glue objects together.""",
            mermaid(
                f"""flowchart TB
    Deploy[Deployment] --> RS[ReplicaSet]
    RS --> PodA[Pod]
    RS --> PodB[Pod]
    Svc[Service] --> PodA
    Svc --> PodB
    Ing[Ingress] --> Svc
    Focus["Focus: {focus}"] -.-> Deploy"""
            )
            + f"\n\n### Dry-run\n\nApply a Deployment, expose a Service, watch endpoints fill as pods become Ready. Relate each step to {focus}.",
            code_block(
                "python",
                f'''def ready_replicas(desired: int, ready: int) -> str:
    if ready == desired:
        return "healthy"
    if ready == 0:
        return "down"
    return "degraded"


if __name__ == "__main__":
    print(ready_replicas(3, 3), ready_replicas(3, 1))
    print("focus", "{focus}")
''',
            ),
            table(
                ["Concern", "Kubernetes lever"],
                [
                    ["Rollout safety", "maxUnavailable / maxSurge / probes"],
                    ["Discovery", "Services + DNS"],
                    ["Config drift", "GitOps + Helm values"],
                    ["Load", "HPA + resource requests"],
                ],
            ),
            bullets(
                [
                    "Set resource requests/limits thoughtfully.",
                    "Use readiness probes so Services skip cold pods.",
                    "Label consistently for selectors.",
                    "Prefer immutable tags/digests in manifests.",
                ]
            ),
            bullets(
                [
                    "No probes — traffic to broken pods.",
                    "Privileged pods without reason.",
                    "Config baked into images.",
                    "Manual cluster changes outside Git.",
                ]
            ),
            f"Explain {focus} and how it relates to Deployments/Services. Discuss probes and rollbacks.",
            numbered(
                [
                    f"Write a minimal manifest touching {focus} (easy)",
                    "Add probes and resources to a Deployment (medium)",
                    "Package the app with Helm values per env (hard)",
                ]
            ),
            bullets(
                [
                    f"{focus}: {blurb}.",
                    "Controllers reconcile desired state.",
                    "Labels connect routing and management.",
                    "GitOps keeps clusters auditable.",
                ]
            ),
            reading(
                [
                    ("Kubernetes docs", "https://kubernetes.io/docs/home/"),
                    ("Helm docs", "https://helm.sh/docs/"),
                ]
            ),
            module=m,
            filename=f"{order:02d}-{slug}.mdx",
            tags=["kubernetes", focus.lower(), "devops"],
            prerequisites=["docker-images-layers"],
            duration=40,
        )


def cicd_mod():
    m = "06-cicd"
    items = [
        (1, "GitHub Actions CI/CD", "github-actions", "GitHub Actions", "YAML workflows in-repo with OIDC to cloud"),
        (2, "Jenkins Pipelines", "jenkins-pipelines", "Jenkins", "battle-tested automation server with Jenkinsfile pipelines"),
        (3, "GitLab CI/CD", "gitlab-ci", "GitLab CI", "integrated pipelines with `.gitlab-ci.yml` and runners"),
        (4, "Deployment Strategies: Rolling, Blue-Green, Canary", "deployment-strategies", "strategies", "shift traffic safely with rolling, blue-green, and canary releases"),
        (5, "Feature Flags for Progressive Delivery", "feature-flags", "feature flags", "decouple deploy from release; target cohorts and kill switches"),
        (6, "Argo CD and GitOps", "argocd-gitops", "Argo CD", "reconcile Kubernetes from Git as the source of truth"),
    ]
    for order, title, slug, focus, blurb in items:
        L(
            title,
            slug,
            f"{blurb.capitalize()}.",
            order,
            f"Shipping safely at speed requires automation. This lesson focuses on {focus}: {blurb}.",
            f"CI/CD is a factory line: commit → test → build → deploy → verify. {focus} is one station on that line — {blurb}.",
            f"""### Deep dive: {focus}

{blurb.capitalize()}.

{table(
    ["Stage", "Typical checks"],
    [
        ["CI", "lint, unit, SAST, build image"],
        ["CD", "deploy to env, smoke test"],
        ["Progressive", "canary metrics, flag gates"],
        ["GitOps", "desired manifests in Git"],
    ]
)}

### Security

OIDC to cloud roles, short-lived tokens, signed images, environment protection rules, least-privilege deploy identities.""",
            mermaid(
                f"""flowchart LR
    Commit --> CI[Build and test]
    CI --> Image[Push image]
    Image --> CD[Deploy]
    CD --> Verify[Smoke / metrics]
    Verify --> Flag[Feature flag]
    Focus["{focus}"] -.-> CD"""
            )
            + "\n\n### Dry-run\n\nFollow a PR from open to production for a web API; name gates and rollback hooks.",
            code_block(
                "python",
                '''def promote(canary_error_rate: float, threshold: float = 0.02) -> str:
    return "promote" if canary_error_rate <= threshold else "rollback"


if __name__ == "__main__":
    print(promote(0.01), promote(0.05))
''',
            ),
            table(
                ["Strategy", "Risk profile"],
                [
                    ["Rolling", "Simple; partial mixed versions"],
                    ["Blue-green", "Fast switch; 2× capacity momentarily"],
                    ["Canary", "Small blast radius; needs metrics"],
                    ["GitOps", "Drift detection; strong audit"],
                ],
            ),
            bullets(
                [
                    "Keep pipelines declarative and reviewed in PRs.",
                    "Separate build and deploy permissions.",
                    "Automate rollback criteria.",
                    "Prefer OIDC over static cloud keys.",
                ]
            ),
            bullets(
                [
                    "Deploying on green unit tests alone.",
                    "Shared god-mode CI credentials.",
                    "No smoke tests after deploy.",
                    "Config drift from kubectl clickOps.",
                ]
            ),
            f"Compare {focus} to alternatives. Explain one progressive delivery strategy with metrics.",
            numbered(
                [
                    f"Sketch a pipeline using {focus} (easy)",
                    "Add a canary gate with error-rate check (medium)",
                    "Design GitOps + flag combo for instant disable (hard)",
                ]
            ),
            bullets(
                [
                    f"{focus}: {blurb}.",
                    "CI proves; CD places; flags release.",
                    "Measure then promote.",
                    "Git remains the source of truth.",
                ]
            ),
            reading(
                [
                    ("GitHub Actions", "https://docs.github.com/actions"),
                    ("Argo CD", "https://argo-cd.readthedocs.io/"),
                    ("Google deployment strategies", "https://cloud.google.com/architecture/application-deployment-and-testing-strategies"),
                ]
            ),
            module=m,
            filename=f"{order:02d}-{slug}.mdx",
            tags=["cicd", "devops", slug],
            prerequisites=["docker-images-layers"],
            duration=40,
        )


def linux_net_mod():
    m = "07-linux-networking"
    items = [
        (1, "Linux Essentials for DevOps", "linux-essentials", "processes, systemd, permissions, journals, and disk"),
        (2, "Networking Fundamentals", "networking-fundamentals", "OSI/TCP, IP, routing, ports, NAT, and troubleshooting"),
        (3, "DNS Deep Dive", "dns-deep-dive", "resolution chain, record types, caching, and failure modes"),
        (4, "TLS and Certificates", "tls-certificates", "handshakes, PKI, ACME, and cipher hygiene"),
        (5, "HTTP/2 and HTTP/3", "http2-http3", "multiplexing, QPACK/HPACK, and QUIC differences"),
    ]
    for order, title, slug, blurb in items:
        L(
            title,
            slug,
            f"Practical {title.lower()}: {blurb}.",
            order,
            f"Cloud abstractions leak. When ALBs misfire or TLS fails, you debug Linux and networking primitives — {blurb}.",
            f"Servers still speak processes, sockets, and packets. This lesson builds intuition for: {blurb}.",
            f"""### Scope

{blurb.capitalize()}.

{table(
    ["Tool", "Use"],
    [
        ["ss / lsof", "Who listens on which port"],
        ["curl -v", "HTTP/TLS debugging"],
        ["dig / nslookup", "DNS answers and TTLs"],
        ["journalctl / systemctl", "Service health on Linux"],
        ["tcpdump / Wireshark", "Packet truth"],
    ]
)}

### Mental models

Always locate the layer: DNS → TCP/QUIC → TLS → HTTP → app.""",
            mermaid(
                """flowchart TB
    App --> HTTP
    HTTP --> TLS
    TLS --> TCP[TCP or QUIC]
    TCP --> IP
    IP --> NIC
    DNS[DNS] -.-> TLS"""
            )
            + "\n\n### Dry-run\n\nA browser fails to load an API: check DNS, TCP connect, TLS cert name, HTTP status, then app logs.",
            code_block(
                "python",
                '''import socket

def can_connect(host: str, port: int, timeout: float = 2.0) -> bool:
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except OSError:
        return False


if __name__ == "__main__":
    print(can_connect("example.com", 443))
''',
            ),
            table(
                ["Symptom", "Likely layer"],
                [
                    ["NXDOMAIN", "DNS"],
                    ["Connection timed out", "Network / SG / routing"],
                    ["Cert verify failed", "TLS"],
                    ["HTTP 502", "Proxy → upstream"],
                ],
            ),
            bullets(
                [
                    "Learn one solid troubleshooting order and reuse it.",
                    "Prefer ss + journalctl before rebooting.",
                    "Understand TTLs when debugging DNS flaps.",
                    "Automate cert renewal; alert on expiry.",
                ]
            ),
            bullets(
                [
                    "Blaming the app before checking DNS/TLS.",
                    "Disabling TLS verify to 'save time'.",
                    "Forgetting TIME_WAIT and connection reuse.",
                    "Mixing HTTP/2 assumptions with broken middleboxes.",
                ]
            ),
            f"Troubleshoot a failing HTTPS call aloud, layer by layer. Mention {blurb}.",
            numbered(
                [
                    "Interpret a failed curl -v transcript (easy)",
                    "Explain HTTP/2 multiplexing vs HTTP/1.1 (medium)",
                    "Design TLS termination at ALB vs at pod (hard)",
                ]
            ),
            bullets(
                [
                    f"Core: {blurb}.",
                    "Debug bottom-up when stuck.",
                    "DNS and TLS cause many 'app' outages.",
                    "HTTP/2/3 change performance characteristics.",
                ]
            ),
            reading(
                [
                    ("Linux man pages", "https://man7.org/linux/man-pages/"),
                    ("MDN HTTP", "https://developer.mozilla.org/en-US/docs/Web/HTTP"),
                    ("RFC 9114 HTTP/3", "https://www.rfc-editor.org/rfc/rfc9114"),
                ]
            ),
            module=m,
            filename=f"{order:02d}-{slug}.mdx",
            tags=["linux", "networking", "tls", "http"],
            prerequisites=["cloud-and-aws-overview"],
            duration=35,
        )


def monitoring_mod():
    m = "08-monitoring-cost"
    items = [
        (1, "Prometheus Metrics and PromQL Basics", "prometheus-metrics", "Prometheus"),
        (2, "Grafana Dashboards and Visualization", "grafana-dashboards", "Grafana"),
        (3, "ELK / OpenSearch Logging Stack", "elk-logging", "ELK"),
        (4, "Alerting and SRE Practices", "alerting-sre", "alerting"),
        (5, "Cloud Cost Optimization Patterns", "cost-optimization", "cost"),
        (6, "AWS Well-Architected Framework", "well-architected", "Well-Architected"),
    ]
    for order, title, slug, focus in items:
        L(
            title,
            slug,
            f"Operate with confidence using {focus} — metrics, logs, alerts, cost, and architecture reviews.",
            order,
            f"Production systems need continuous insight and deliberate cost control. This lesson centers on {focus}.",
            f"Observability without action is vanity; cost without architecture is thrift theater. {focus} connects signals to decisions.",
            f"""### Focus: {focus}

{table(
    ["Signal", "Question it answers"],
    [
        ["Metrics", "Is it broken or saturated now?"],
        ["Logs", "What exactly happened?"],
        ["Traces", "Where did time go?"],
        ["Alerts", "Who should wake up?"],
        ["Cost", "Are we wasting money?"],
        ["WAFR", "Are we aligned to pillars?"],
    ]
)}

### Practices

SLIs/SLOs, error budgets, actionable alerts (symptom-based), dashboards per service, regular cost reviews, Well-Architected lenses.""",
            mermaid(
                f"""flowchart LR
    App --> Prom[Prometheus]
    App --> Logs[ELK]
    Prom --> Graf[Grafana]
    Prom --> Alert[Alertmanager]
    Alert --> Page[Pager]
    Focus["{focus}"] -.-> Graf"""
            )
            + "\n\n### Dry-run\n\nAn error-rate SLO burn alerts; dashboard shows saturation; logs show bad deploy; roll back; write a post-incident note.",
            code_block(
                "python",
                '''def slo_burn(error_rate: float, slo: float = 0.001) -> str:
    if error_rate <= slo:
        return "ok"
    if error_rate <= slo * 10:
        return "page-soon"
    return "page-now"


if __name__ == "__main__":
    print(slo_burn(0.0005), slo_burn(0.02))
''',
            ),
            table(
                ["Approach", "Upside", "Downside"],
                [
                    ["High-card metrics", "Detail", "Cost / TSDB load"],
                    ["Verbose debug logs in prod", "Easy forensics", "Cost / PII risk"],
                    ["Alert on CPU only", "Simple", "Misses user pain"],
                ],
            ),
            bullets(
                [
                    "Alert on symptoms tied to SLOs.",
                    "Keep dashboards boring and consistent.",
                    "Tag spend; review weekly.",
                    "Run Well-Architected reviews after major changes.",
                ]
            ),
            bullets(
                [
                    "Pager fatigue from noisy alerts.",
                    "Metrics without owners.",
                    "Saving money by deleting backups.",
                    "Treating WAFR as paperwork, not engineering.",
                ]
            ),
            f"Define SLIs for an API and an alert that maps to user pain. Mention how {focus} helps.",
            numbered(
                [
                    f"Sketch a dashboard focused on {focus} (easy)",
                    "Write a symptom-based alert with runbook link (medium)",
                    "Propose three cost cuts that preserve reliability (hard)",
                ]
            ),
            bullets(
                [
                    f"{focus} is a lever for safer, cheaper operations.",
                    "Golden signals first.",
                    "Error budgets guide pace.",
                    "Architecture and cost reviews are continuous.",
                ]
            ),
            reading(
                [
                    ("Prometheus docs", "https://prometheus.io/docs/introduction/overview/"),
                    ("Grafana docs", "https://grafana.com/docs/"),
                    ("AWS Well-Architected", "https://aws.amazon.com/architecture/well-architected/"),
                ]
            ),
            module=m,
            filename=f"{order:02d}-{slug}.mdx",
            tags=["monitoring", "sre", "cost", focus.lower()],
            prerequisites=["cloudwatch-observability"],
            duration=35,
        )


def deploy_codecraft():
    m = "09-deploy-codecraft"
    lessons = [
        (
            1,
            "CodeCraft on AWS — Architecture Overview",
            "codecraft-aws-architecture",
            """flowchart TB
    Users --> R53[Route 53]
    R53 --> CF[CloudFront]
    CF --> FE[S3 / Next static]
    CF --> ALB
    ALB --> ECS[ECS Fargate API]
    ECS --> RDS[(RDS Postgres)]
    ECS --> Redis[(ElastiCache)]
    ECS --> S3data[(S3 content)]
    ECS --> SM[Secrets Manager]
    CI[GitHub Actions] --> ECR
    CI --> ECS""",
            "Map the CodeCraft Academy app to a production-shaped AWS architecture with clear trust boundaries.",
            "We will treat frontend, API, content, and data as separate deployables behind DNS and CDN — the same pattern used by many SaaS products.",
            """### Target architecture

- **Frontend**: Next.js static/SSR assets via CloudFront (+ S3 or container origin)
- **API**: FastAPI on ECS Fargate behind ALB
- **Data**: RDS Postgres Multi-AZ; optional Redis for sessions/cache
- **Content**: lesson MDX from S3 or baked into images
- **Secrets**: Secrets Manager; IAM task roles
- **CI/CD**: GitHub Actions → ECR → ECS deploy

### Non-goals

Multi-Region active-active (can be a stretch goal). Kubernetes is optional; ECS keeps ops lighter for this app size.""",
        ),
        (
            2,
            "Infrastructure as Code for CodeCraft",
            "codecraft-iac-deploy",
            """flowchart LR
    TF[Terraform / CDK] --> VPC
    TF --> ALB
    TF --> ECS
    TF --> RDS
    TF --> S3
    TF --> IAM""",
            "Provision the CodeCraft AWS footprint with Terraform or CDK: network, data, compute, and IAM.",
            "Codify the architecture module-by-module so environments are reproducible and reviewable.",
            """### Stacks / modules

1. Network (VPC, subnets, NAT, endpoints)
2. Data (RDS, Redis, S3)
3. Edge (ACM, CloudFront, Route 53)
4. Compute (ECR, ECS cluster/services, ALB)
5. Observability (log groups, alarms)

### Apply order

Network → data → secrets → compute → edge DNS cutover. Use remote state per env (`dev`, `prod`).""",
        ),
        (
            3,
            "CI/CD and Observability for CodeCraft",
            "codecraft-cicd-observability",
            """flowchart LR
    PR --> Actions[GitHub Actions]
    Actions --> Test
    Test --> Build
    Build --> ECR
    ECR --> Deploy[ECS rollout]
    Deploy --> CW[CloudWatch]
    CW --> Alarm --> SNS""",
            "Wire GitHub Actions, ECS rollouts, CloudWatch alarms, and dashboards so CodeCraft deploys are boring.",
            "A green pipeline with smoke tests and golden-signal alarms turns releases into routine.",
            """### Pipeline

- PR: lint + unit + build
- Main: push images (API/frontend), run `terraform plan` / apply gated
- Deploy: ECS new task definition, circuit breaker rollback
- Post-deploy: hit `/health`, check 5xx and p95

### Alarms

ALB 5xx, unhealthy hosts, RDS CPU/storage, ECS CPU/mem, digest auth failures if any.""",
        ),
    ]
    for order, title, slug, diagram, why, intuition, core in lessons:
        L(
            title,
            slug,
            why,
            order,
            why,
            intuition,
            core,
            mermaid(diagram)
            + "\n\n### Dry-run\n\nFollow a learner request from DNS through CloudFront to the API and Postgres; then follow a deploy from GitHub to ECS.",
            code_block(
                "python",
                '''def healthcheck(status_code: int, db_ok: bool) -> dict[str, str]:
    if status_code == 200 and db_ok:
        return {"status": "ok"}
    return {"status": "degraded"}


if __name__ == "__main__":
    print(healthcheck(200, True))
''',
            ),
            table(
                ["Component", "HA choice", "Cost note"],
                [
                    ["ECS Fargate", "Multi-AZ tasks", "Pay for vCPU/mem time"],
                    ["RDS", "Multi-AZ", "2× instance-ish cost"],
                    ["CloudFront", "Global edge", "Egress savings vs origin"],
                    ["NAT", "Per-AZ HA", "Hours + data processing"],
                ],
            ),
            bullets(
                [
                    "Keep content and secrets out of the client bundle.",
                    "Use task roles; no static AWS keys on ECS.",
                    "Smoke-test after every deploy.",
                    "Diagram first; then encode in Terraform/CDK.",
                ]
            ),
            bullets(
                [
                    "Single-AZ RDS for 'student project' that becomes prod.",
                    "Public RDS for convenience.",
                    "Skipping alarms until the first outage.",
                    "Manual console edits after IaC bootstrap.",
                ]
            ),
            "Whiteboard CodeCraft on AWS end-to-end. Defend ECS vs EKS, Multi-AZ data, and CI security (OIDC).",
            numbered(
                [
                    "Label every box in the architecture with an AWS service (easy)",
                    "Write a terraform module list for dev/prod (medium)",
                    "Define rollback criteria and alarms for a bad API deploy (hard)",
                ]
            ),
            bullets(
                [
                    "Edge → ALB → ECS → RDS/Redis/S3.",
                    "IaC modules mirror architecture layers.",
                    "Actions + ECR + ECS for ship path.",
                    "CloudWatch golden signals close the loop.",
                ]
            ),
            reading(
                [
                    ("ECS best practices", "https://docs.aws.amazon.com/AmazonECS/latest/bestpracticesguide/intro.html"),
                    ("AWS reference architectures", "https://aws.amazon.com/architecture/"),
                ]
            ),
            module=m,
            filename=f"{order:02d}-{slug}.mdx",
            tags=["aws", "ecs", "codecraft", "deploy"],
            prerequisites=["ecs-eks-fargate", "github-actions", "terraform-fundamentals"],
            duration=45,
            difficulty="advanced",
        )


def main():
    expand_fundamentals()
    aws_core()
    terraform_mod()
    docker_mod()
    k8s_mod()
    cicd_mod()
    linux_net_mod()
    monitoring_mod()
    deploy_codecraft()
    print("Cloud/DevOps lessons generated.")


if __name__ == "__main__":
    main()
