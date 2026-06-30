from src.job_parser.job_parser import parse_job_description

with open("data/job_description.txt", encoding="utf-8") as f:
    jd = f.read()

result = parse_job_description(jd)

print(result)