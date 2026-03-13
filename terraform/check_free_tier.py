import json
import sys

DISALLOWED_TYPES = {
    "aws_nat_gateway",
    "aws_lb",
    "aws_alb",
    "aws_elb",
    "aws_elasticache_cluster",
    "aws_eks_cluster",
    "aws_redshift_cluster",
}

ALLOWED_EC2 = {"t2.micro", "t3.micro"}
ALLOWED_RDS = {"db.t2.micro", "db.t3.micro", "db.t4g.micro"}


def fail(message: str) -> None:
    print(f"FREE_TIER_CHECK_FAILED: {message}")
    sys.exit(1)


with open("tfplan.json", "r", encoding="utf-8") as file:
    plan = json.load(file)

changes = plan.get("resource_changes", [])
for change in changes:
    actions = change.get("change", {}).get("actions", [])
    if not any(action in {"create", "update"} for action in actions):
        continue

    resource_type = change.get("type")
    if resource_type in DISALLOWED_TYPES:
        fail(f"Resource type {resource_type} is blocked for free-tier-focused deployments.")

    after = change.get("change", {}).get("after", {}) or {}

    if resource_type == "aws_instance":
        instance_type = after.get("instance_type")
        if instance_type not in ALLOWED_EC2:
            fail(f"EC2 instance_type {instance_type} is not in allowed list {sorted(ALLOWED_EC2)}")

    if resource_type == "aws_db_instance":
        instance_class = after.get("instance_class")
        if instance_class not in ALLOWED_RDS:
            fail(f"RDS instance_class {instance_class} is not in allowed list {sorted(ALLOWED_RDS)}")

print("FREE_TIER_CHECK_PASSED")
